# QA Portfolio Demo

這個資料夾現在以根目錄的單入口 QA demo 為主。舊的搶票實驗腳本保留作備份，不再當成主版本。

## 檔案用途

- `main.py`：新的 QA 作品集入口，會開啟示範頁、等待元素、做斷言、存截圖、寫 log。
- `config.py`：集中管理 URL、等待時間、輸出資料夾和測試條件。
- `artifacts/`：每次執行的截圖輸出。
- `logs/`：執行紀錄。
- `main_legacy.py`：保留舊版搶票實驗腳本備份。
- `test.py`：最小測試腳本，只負責啟動 Chrome 並導向 Google。
- `index.py`：舊版 Cookie / OCR 實驗腳本。
- `requirements.txt`：Python 套件版本鎖定清單。
- `downloaded_packages/`：已下載的套件檔，可用來離線安裝。

## 執行方式

```powershell
cd c:\Users\user\Desktop\搶票ROBOT
python -m pip install -r requirements.txt
python main.py
```

如果你只是想確認瀏覽器環境，也可以額外執行：

```powershell
python test.py
```

## 新版 QA 流程

`main.py` 的流程很短，適合作為作品集展示：

1. 開啟 Chrome
2. 前往拓元首頁
3. 等待標題與搜尋框出現
4. 驗證搜尋框 placeholder 是否符合預期
5. 成功時存截圖到 `artifacts/`
6. 失敗時把錯誤截圖也存進 `artifacts/`

## 目前要注意的設定

- `config.py` 內的 `TARGET_URL`、`EXPECTED_TITLE`、`PRIMARY_SELECTOR`、`EXPECTED_PLACEHOLDER` 決定驗證內容。
- `HEADLESS = False` 代表會顯示瀏覽器畫面，方便作品集錄影或展示。
- 這個版本不再依賴帳號、密碼或 Cookie 流程。

## 已知問題與風險

- `main_legacy.py`、`index.py`、`test.py` 都是舊版或實驗版，內容保留作參考。
- 舊版搶票腳本仍然含有硬編碼帳號、Cookie 與網站相依設定，不適合作為作品集主版本。
- 如果 Chrome 更新太多，仍可能需要更新 Selenium 或 ChromeDriver。

## 建議後續

- 把 `config.py` 的設定搬到 `.env`，方便不同機器共用。
- 把 `TARGET_URL` 改成你要展示的合法示範頁面。
- 加入更多 assert，例如按鈕文字、圖片是否載入、區塊是否可見。