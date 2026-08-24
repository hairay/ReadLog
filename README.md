# ReadLog — 印表機 Log 分析工具集

這是一組用來解析印表機韌體 Log（VM3 / Mice / TwinColor / Panther / Riscv 等平台）的 Python 腳本與 Windows 批次 wrapper。所有主要分析腳本都從 **stdin** 讀取純文字 Log，輸出整理後的文字、CSV 或 PNG 圖表。

---

## 快速開始

### 1. 直接以 pipe 方式執行

```batch
type logfile.txt | python readlog.py
type logfile.txt | python vm3_temprature.py   :: 產生 curve.png
type logfile.txt | python vm3_sensor.py       :: 產生 curve.png
```

### 2. 使用批次檔一次處理多個 Log

批次檔會掃描目前目錄與 `./log/` 下的所有 `*.txt`，逐一 pipe 給對應的 Python 腳本，並將輸出寫在原始檔案旁邊。請在專案根目錄執行：

```batch
.\Auto.bat          :: readlog.py  → *-time.log
.\KeyWord.bat       :: read_key_word.py → *-keyword.log
.\auto_mem.bat      :: memory.py → *-mem.log
.\auto_m3_band.bat  :: qbitScanBand.py → *-band.log
.\AutoSensor.bat    :: vm3_sensor.py → MCU_*.log + *-sensor.png
.\AutoTemp.bat      :: vm3_temprature.py → *.csv + *-temp.png
.\AutoMcuInOut.bat  :: mcu_in_out.py → MCU_IO_*.log + *-inout.png
.\AutoIoCtrlTable.bat :: IO_CtrlTable.py → MCU_Output_*.csv
.\mice.bat          :: micelog.exe（產生 .log 後自動改名）
.\twin.bat          :: twincolor.exe（產生 .log 後自動改名）
.\start_forward.bat :: 背景啟動 outlook_forward_service.py
```

---

## 腳本說明

| Python 腳本 | 用途 | 批次 wrapper | 輸出檔 |
|-------------|------|--------------|--------|
| `readlog.py` | 解析 Job 起訖、重開機、等待 API 等事件 | `Auto.bat` | `*-time.log` |
| `read_key_word.py` | 過濾錯誤、中斷、assert、timeout 等關鍵字 | `KeyWord.bat` | `*-keyword.log` |
| `memory.py` | 追蹤實體 / 虛擬記憶體配置與釋放 | `auto_mem.bat` | `*-mem.log` |
| `qbitScanBand.py` | 檢查 scan band 的提交與接收是否匹配 | `auto_m3_band.bat` | `*-band.log` |
| `vm3_sensor.py` | 繪製各 sensor 狀態隨時間變化圖 | `AutoSensor.bat` | `MCU_*.log`、`*-sensor.png` |
| `vm3_temprature.py` | 繪製溫度、target、duty、nip 等曲線 | `AutoTemp.bat` | `*.csv`、`*-temp.png` |
| `mcu_in_out.py` | 繪製 MCU IO 狀態圖 | `AutoMcuInOut.bat` | `MCU_IO_*.log`、`*-inout.png` |
| `IO_CtrlTable.py` | 輸出 MCU IO CtrlTable 相關 CSV | `AutoIoCtrlTable.bat` | `MCU_Output_*.csv` |
| `find_word_doc.py` | 將 `.doc` 轉 `.docx` 並搜尋指定字串 | 無 | 終端輸出 |
| `find_word_docx.py` | 搜尋 `.docx` 中的指定字串 | 無 | 終端輸出 |
| `outlook_forward_service.py` | 背景監控 Outlook 收件匣並自動轉寄郵件 | `start_forward.bat` | `forward_log.txt` |
| `test.py` | 簡易 regex 測試片段 | 無 | 終端輸出 |

`mice.bat` 與 `twin.bat` 則分別呼叫同目錄下的 `micelog.exe` 與 `twincolor.exe`，執行後會把產生的 `.log` 重新命名。

---

## 相依套件

| 腳本 | 所需套件 |
|------|----------|
| `readlog.py`、`memory.py`、`IO_CtrlTable.py`、`qbitScanBand.py`、`read_key_word.py` | 僅 Python 標準函式庫 |
| `vm3_sensor.py`、`mcu_in_out.py`、`vm3_temprature.py` | `matplotlib`、`numpy` |
| `find_word_doc.py`、`find_word_docx.py` | `pywin32`、`python-docx` |
| `outlook_forward_service.py` | `pywin32` |

安裝方式：

```batch
pip install -r requirements.log
```

---

## 注意事項

- **PNG 產生與視窗顯示**：`vm3_sensor.py`、`mcu_in_out.py`、`vm3_temprature.py` 預設產生 `curve.png` 並在背景關閉視窗，不會阻斷批次處理。如需開啟圖形介面檢視，可加上 `--show` 參數。
- **輸出檔不納入版本控制**：`*.log`、`*.png`、`*.csv` 皆已在 `.gitignore` 中，只有 `log/` 下已提交的範例外。
- **平台術語**：Log 中常見的 M3/M3P、VM3、Mice、TwinColor、Panther、Riscv 等詞彙，代表不同的印表機平台或韌體分支。

---

## Log 中常見平台術語

| 術語 | 說明 |
|------|------|
| M3 / M3P | 主印表機 SoC |
| VM3 | 印表機韌體分支 |
| Mice | 印表機平台分支 |
| TwinColor | 彩色印表機分支 |
| Panther | 印表機引擎分支 |
| Riscv | RISC-V 架構分支 |

---

## 範例

```batch
type log\test_20260814_113210.txt | python readlog.py > log\test_20260814_113210.txt-time.log
```

或使用批次檔：

```batch
.\Auto.bat
```
