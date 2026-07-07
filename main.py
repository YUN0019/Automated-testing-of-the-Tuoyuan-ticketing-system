# main_playwright.py
import os
import time
from playwright.sync_api import sync_playwright
import config
from test_reporter import QAReporter

def main():
    print("🚀 啟動：拓元核心售票流功能測試 (全自動結束無閃退保護版)...")
    reporter = QAReporter("拓元售票核心商務路徑功能回歸測試")
    
    with sync_playwright() as p:
        reporter.start_step()
        print("🌐 正在啟動 Chromium 瀏覽器...")
        
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        try:
            # === 步驟 1：前往拓元網頁首頁 ===
            print(f"🌍 衝向拓元網頁首頁: {config.TARGET_URL}")
            page.goto(config.TARGET_URL)
            time.sleep(2)
            reporter.step_pass("成功載入拓元售票系統首頁")

            # === 步驟 2：在搜尋框輸入 BTS 關鍵字並搜尋 ===
            reporter.start_step()
            print(f"🔍 正在定位 '#txt_search' 並輸入: {config.SEARCH_KEYWORD}")
            
            search_input = page.wait_for_selector("#txt_search", timeout=5000)
            search_input.fill(config.SEARCH_KEYWORD)
            
            print("⌨️ 關鍵字輸入成功，按下 Enter 送出搜尋...")
            search_input.press("Enter")
            
            # === 搜尋後原地狠等 3.5 秒 ===
            print("⏳ 原地等待 3.5 秒，讓搜尋結果與 Cookie 彈窗徹底定型...")
            time.sleep(3.5) 
            reporter.step_pass(f"成功搜尋目標關鍵字：『{config.SEARCH_KEYWORD}』並完成 3.5 秒緩衝等待")

            # === 步驟 3：點擊全部確認 Cookie 框框 ===
            reporter.start_step()
            print("🛡️ 正在精準定位消滅 OneTrust Cookie 彈窗防護罩...")
            cookie_btn = page.locator("#onetrust-accept-btn-handler").first
            
            for i in range(5):
                if cookie_btn.is_visible():
                    print(f"💥 第 {i+1} 次嘗試點擊『接受所有 Cookie』...")
                    cookie_btn.click(force=True) 
                    time.sleep(1) 
                else:
                    print("✅ Cookie 彈窗已完全消失！")
                    break
                    
            reporter.step_pass("成功突破 Cookie 彈窗限制")

            # === 步驟 4：精準戳中 svg 箭頭點擊活動 ===
            reporter.start_step()
            print("🔗 障礙已排除！正在用 F12 結構精準鎖定並點擊 svg.gmoWZn 核心按鈕...")
            
            search_result_svg = page.locator("svg.gmoWZn").first
            search_result_svg.wait_for(state="visible", timeout=5000)
            print("🎯 戳中關鍵 SVG 展開箭頭！正在跳轉至活動詳情頁...")
            search_result_svg.click(force=True) 
            time.sleep(4) 
            reporter.step_pass("成功點擊活動 SVG 元素並跳轉至活動詳情頁")

            # === 步驟 5：點選『立即購票』 ===
            reporter.start_step()
            print("🎯 抵達活動詳情頁！正在點擊『立即購票』...")
            
            buy_button = page.locator("//a[contains(@href, '26_btskns')]//div[contains(text(), '立即購票')] | //a[contains(@href, '26_btskns')]").first
            buy_button.wait_for(state="visible", timeout=5000)
            buy_button.click(force=True)
            
            print("✅ [震撼成功] 成功擊中『立即購票』！已順利進入購票流程")
            time.sleep(3) 
            
            # 拍照存證
            success_img_name = f"playwright_bts_success_{int(time.time())}.png"
            page.screenshot(path=str(config.ARTIFACT_DIR / success_img_name))
            
            reporter.step_pass("成功點擊購票按鈕並進入購票流程頁面", note=f"artifacts/{success_img_name}")
            print(f"\n🎉【大功告成】流程全部跑完，即將全自動關閉程式...")

        except Exception as e:
            print(f"\n❌ 流程中斷！詳細錯誤原因: {e}")
            reporter.step_fail("自動化流程異常中斷", e, driver=None)
            try:
                page.screenshot(path=str(config.ARTIFACT_DIR / f"playwright_error_{int(time.time())}.png"))
            except:
                pass
        finally:
            # 產出網頁版測試報告
            reporter.generate_report("拓元自動化測試報告.html")
            print("\n🔒 測試程序無誤，瀏覽器關閉。")
            # 💡 移除 input 卡點，直接關閉瀏覽器釋放資源
            browser.close()

if __name__ == "__main__":
    main()