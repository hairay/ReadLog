# ReadLog — printer log analysis tools

## How to run

All Python scripts read from **stdin** (pipe a `.txt` log file):

```batch
type logfile.txt | python readlog.py
type logfile.txt | python vm3_temprature.py   :: generates curve.png
type logfile.txt | python vm3_sensor.py       :: generates curve.png
```

Batch wrappers (`Auto*.bat`, `KeyWord.bat`) iterate over all `*.txt` in `.` and `./log/`, pipe each through a script, and write output alongside the input. Run from the repo root:

```batch
.\Auto.bat          :: readlog.py  → *-time.log
.\AutoSensor.bat    :: vm3_sensor.py → MCU_*.log + *-sensor.png
.\AutoTemp.bat      :: vm3_temprature.py → *.csv + *-temp.png
.\auto_mem.bat      :: memory.py → *-mem.log
.\AutoMcuInOut.bat  :: mcu_in_out.py → MCU_IO_*.log + *-inout.png
.\AutoIoCtrlTable.bat :: IO_CtrlTable.py → MCU_Output_*.csv
.\auto_m3_band.bat  :: qbitScanBand.py → *-band.log
.\KeyWord.bat       :: read_key_word.py → *-keyword.log
```

`start_forward.bat` / `stop_forward.bat` manage the Outlook auto-forwarding service (`outlook_forward_service.py`). `stop_forward.bat` only kills processes whose command line contains `outlook_forward_service` — never use `taskkill /f /im python.exe`.

## Dependencies

- **stdlib only:** `readlog.py`, `memory.py`, `IO_CtrlTable.py`, `qbitScanBand.py`, `read_key_word.py`
- **matplotlib + numpy:** `vm3_sensor.py`, `mcu_in_out.py`, `vm3_temprature.py`
- **win32com + python-docx:** `find_word_doc.py`, `find_word_docx.py`
- **win32com:** `outlook_forward_service.py`

Install as needed: `pip install -r requirements.log`

## Scripts that generate PNGs

`vm3_sensor.py`, `mcu_in_out.py`, and `vm3_temprature.py` write `curve.png` in the **current working directory**. Running them in parallel or sequentially without renaming will overwrite. The batch wrappers rename after each run (`.bat` files show the rename pattern).

## Shared patterns

- **`SearchLog(f, patterns)`** dispatches lines through `[(compiled_regex, handler_func), ...]` tuples and stops at the **first matching pattern** (all scripts `break` after dispatch). Put specific patterns before generic catch-alls. Global `_lineNum` is incremented per line.
- **`GetMsTimeFromStart(cur, start)`** handles 32-bit timer wraparound (`0xFFFFFFFF`).
- No tests, no linting, no type checking, no CI.

## Platform terminology in log files

| Term | Meaning |
|------|---------|
| M3/M3P | Main printer SoC |
| VM3 | Printer firmware variant |
| Mice | Printer platform variant |
| TwinColor | Color printer variant |
| Panther | Printer engine variant |
| Riscv | RISC-V based variant |

## Working tree state

`cat2.exe`, `micelog.exe`, `twincolor.exe` (and two `.docx` docs) are tracked legacy binaries/docs committed before the `*.exe` ignore rule. `ANLOG.exe`, `Print_Job.exe`, `forward_sent.json`, `Print_Job_config.json` exist locally but are gitignored/untracked — do not add them.

## Output files are gitignored

`*.log`, `*.txt`, `*.png`, `*.csv` are all in `.gitignore`. Log input files (`*.txt`) and all generated output are not tracked. Sample logs placed under `log/` as `*.txt` are deliberately NOT ignored (via `!log/*.txt`) so they can be committed.

## Repo structure

- **1 branch:** `master`
- **2 remotes:** `origin` (GitLab), `github` (GitHub mirror)
- **No package/module hierarchy** — flat scripts, no `pyproject.toml`, dependencies in `requirements.log`
