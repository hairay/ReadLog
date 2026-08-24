import sys
import os
import time
import json
try:
    import win32com.client
except ImportError:
    win32com = None

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

POLL_INTERVAL = int(os.environ.get("FORWARD_POLL_INTERVAL", "10"))
LOOKBACK_SECONDS = int(os.environ.get("FORWARD_LOOKBACK_SEC", "7200"))  # Default lookback 2 hours
FORWARD_TARGET_EMAIL = os.environ.get("FORWARD_TARGET_EMAIL", "hairay@gmail.com")
FORWARD_KEYWORD = os.environ.get("FORWARD_KEYWORD", "hairay").lower()
MAX_SEND_RETRIES = int(os.environ.get("FORWARD_MAX_RETRIES", "3"))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SENT_FILE = os.path.join(SCRIPT_DIR, "forward_sent.json")

def load_sent():
    try:
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return list(data)
    except Exception:
        return []

def save_sent(id_list):
    try:
        # Keep latest 2000 sent IDs
        with open(SENT_FILE, "w", encoding="utf-8") as f:
            json.dump(id_list[-2000:], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save sent records: {e}", flush=True)

def should_forward(item):
    try:
        if getattr(item, 'Class', None) != 43:  # 43 = olMail
            return False
        to_field = (getattr(item, 'To', '') or "").lower()
        return FORWARD_KEYWORD in to_field and ";" not in to_field
    except Exception:
        return False

def main():
    if win32com is None:
        print("ERROR: pywin32 is not installed (`pip install pywin32`)", flush=True)
        return

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mapi = outlook.GetNamespace("MAPI")
        inbox = mapi.GetDefaultFolder(6)  # 6 = olFolderInbox
    except Exception as e:
        print(f"[ERROR] Failed to initialize Outlook: {e}", flush=True)
        return

    sent_ids_list = load_sent()
    sent_ids_set = set(sent_ids_list)
    fail_counts = {}
    dirty = False

    print(f"Outlook forwarding service started. (Target: {FORWARD_TARGET_EMAIL}, Keyword filter: {FORWARD_KEYWORD})", flush=True)

    while True:
        try:
            items = inbox.Items
            items.Sort("[ReceivedTime]", True)
            item = items.GetFirst()
            cutoff = time.time() - LOOKBACK_SECONDS

            while item:
                try:
                    rt = item.ReceivedTime
                    ts = time.mktime(rt.timetuple())
                    if ts < cutoff:
                        break
                    eid = getattr(item, 'EntryID', None)
                    if eid and eid not in sent_ids_set and should_forward(item):
                        try:
                            fwd = item.Forward()
                            fwd.Recipients.Add(FORWARD_TARGET_EMAIL)
                            if not fwd.Recipients.ResolveAll():
                                raise RuntimeError("could not resolve recipient")
                            fwd.Send()
                            sent_ids_set.add(eid)
                            sent_ids_list.append(eid)
                            fail_counts.pop(eid, None)
                            dirty = True
                            print(f"[FORWARDED] {getattr(item, 'Subject', '(No Subject)')}", flush=True)
                        except Exception as e:
                            fail_counts[eid] = fail_counts.get(eid, 0) + 1
                            if fail_counts[eid] >= MAX_SEND_RETRIES:
                                sent_ids_set.add(eid)
                                sent_ids_list.append(eid)
                                dirty = True
                                print(f"[GAVE UP after {fail_counts[eid]} attempts] {getattr(item, 'Subject', '(No Subject)')}: {e}", flush=True)
                            else:
                                print(f"[SKIPPED attempt {fail_counts[eid]}] {getattr(item, 'Subject', '(No Subject)')}: {e}", flush=True)
                except Exception as e:
                    print(f"[SKIPPED] {e}", flush=True)
                item = items.GetNext()
        except Exception as e:
            print(f"[ERROR] Poll error: {e}", flush=True)

        if dirty:
            save_sent(sent_ids_list)
            dirty = False
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
