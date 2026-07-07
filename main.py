# main_playwright.py
import os
import time
from playwright.sync_api import sync_playwright
import config
from test_reporter import QAReporter

def main():
    print("🚀 啟動：拓元核心售票流功能測試")
    reporter = QAReporter("拓元售票核心商務路徑功能回回歸測試")
    
    with sync_playwright() as p:
        reporter.start_step()
        print(" 正在啟動 Chromium 瀏覽器...")
        
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        try:
            # === 步驟 1：前往拓元網頁首頁 ===
            print(f"前往拓元網頁首頁: {config.TARGET_URL}")
            page.goto(config.TARGET_URL)
            time.sleep(3)
            reporter.step_pass("成功載入拓元售票系統首頁")

            # === 步驟 2：輸入關鍵字並搜尋 ===
            reporter.start_step()
            print(f" 正在定位 '#txt_search' 並打字輸入: {config.SEARCH_KEYWORD}")
            
            search_input = page.wait_for_selector("#txt_search", timeout=5000)
            search_input.fill(config.SEARCH_KEYWORD)
            
            print(" 關鍵字輸入成功，按下 Enter 送出搜尋...")
            search_input.press("Enter")
            time.sleep(4) # 等待搜尋結果與 Cookie 彈窗完全載入
            reporter.step_pass(f"成功搜尋目標關鍵字：『{config.SEARCH_KEYWORD}』")

            # === 步驟 3：點擊接受所有 Cookie 選項 (F12 精準 ID 版) ===
            reporter.start_step()
            print(" 正在點擊 OneTrust Cookie")
            
            # 使用你抓到的絕對精準 ID
            cookie_btn = page.locator("#onetrust-accept-btn-handler").first
            
            if cookie_btn.is_visible():
                cookie_btn.click()
                print(" 已Cookie 彈窗 ! ")
                time.sleep(2) # 給彈窗淡出動畫一點時間，確保卡片回到可點擊狀態
                reporter.step_pass("成功點擊接受所有 Cookie，解鎖畫面點擊權限")
            else:
                print("💡 畫面上未偵測到 Cookie 彈窗，直接進入下一步。")
                reporter.step_pass("未看見 Cookie 彈窗，跳過清除步驟")

            # === 步驟 4：點擊 BTS 場次卡片 ===
            reporter.start_step()
            print("🔗 障礙已除，正在精準點擊 BTS 高雄場卡片...")
            
            search_result_card = page.locator(
                "//div[@class='data' and .//div[contains(text(), 'ARIRANG')]] | "
                "//img[contains(@src, '26_btskns')] | "
                "//div[contains(text(), 'BTS WORLD TOUR')]"
            ).first
            
            search_result_card.wait_for(state="visible", timeout=5000)
            search_result_card.click()
            print("🎯 成功點擊場次卡片！跳轉至活動詳情頁...")
            time.sleep(4) # 確保詳情頁完整載入
            reporter.step_pass("成功點擊場次卡片並跳轉至活動詳情頁")

            # === 步驟 5：點選『立即購票』 ➔ 結束執行 ===
            reporter.start_step()
            print("🎯 抵達活動詳情頁！正在點擊『立即購票』...")
            
            buy_button = page.locator("//a[contains(@href, '26_btskns')]//div[contains(text(), '立即購票')] | //a[contains(@href, '26_btskns')] | //a[contains(text(),'立即購票')]").first
            buy_button.wait_for(state="visible", timeout=5000)
            buy_button.click()
            
            print("✅ [震撼成功] 成功擊中『立即購票』！已成功觸發購票流程")
            time.sleep(3) 
            
            # 拍照存證
            success_img_name = f"playwright_bts_success_{int(time.time())}.png"
            page.screenshot(path=str(config.ARTIFACT_DIR / success_img_name))
            
            reporter.step_pass("成功點擊購票按鈕並進入購票流程頁面", note=f"artifacts/{success_img_name}")
            print(f"\n🎉【大成功】全線精準對齊標籤，順暢通關！")

        except Exception as e:
            print(f"\n❌ 流程中斷！詳細錯誤原因: {e}")
            reporter.step_fail("自動化流程異常中斷", e, driver=None)
            try:
                page.screenshot(path=str(config.ARTIFACT_DIR / f"playwright_error_{int(time.time())}.png"))
            except:
                pass
        finally:
            reporter.generate_report("拓元自動化測試報告.html")
            print("\n🔒 [防閃退保護] 測試程序執行完畢。")
            input("🛑 請確認瀏覽器畫面與報告。確認完畢請按 Enter 關閉瀏覽器...")
            browser.close()

if __name__ == "__main__":
    main()