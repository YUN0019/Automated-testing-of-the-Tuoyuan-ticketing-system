# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = BASE_DIR / "artifacts"
LOG_DIR = BASE_DIR / "logs"

# 確保目錄存在
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 測試目標與參數配置
TARGET_URL = "https://tixcraft.com/"
COOKIE_PATH = "cookies.pkl"
CHROME_VERSION_MAIN = 149  # 配合你原本 index.py 的設定

# 精準鎖定搜尋關鍵字
SEARCH_KEYWORD = "BTS WORLD TOUR ’ARIRANG’ IN KAOHSIUNG" 

WAIT_TIMEOUT = 15
DEBUG_MODE = True