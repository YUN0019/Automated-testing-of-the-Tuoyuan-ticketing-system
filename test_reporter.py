# test_reporter.py
import time
from datetime import datetime
import config

class QAReporter:
    def __init__(self, report_title="自動化測試分析報告"):
        self.report_title = report_title
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.details = []
        self.summary = {"total": 0, "pass": 0, "fail": 0}
        self.step_start = None

    def start_step(self):
        """標記一個新步驟開始計時"""
        self.step_start = time.time()
        self.summary["total"] += 1

    def step_pass(self, step_name, note="-"):
        """記錄步驟成功"""
        duration = round(time.time() - self.step_start, 2)
        self.details.append({"step": step_name, "status": "PASS", "time": duration, "error": "-", "screenshot": note})
        self.summary["pass"] += 1
        print(f"✅ [PASS] {step_name} ({duration}s)")

    def step_fail(self, step_name, error_exception, driver=None):
        """記錄步驟失敗：自動截圖並分析錯誤名稱"""
        duration = round(time.time() - self.step_start, 2)
        error_type = type(error_exception).__name__
        
        # 失敗自動截圖
        screenshot_name = f"error_{int(time.time())}.png"
        screenshot_path = config.ARTIFACT_DIR / screenshot_name
        if driver is not None:
            try:
                driver.save_screenshot(str(screenshot_path))
                print(f"📸 錯誤快照已保存至 artifacts/{screenshot_name}")
            except Exception as se:
                print(f"⚠️ 截圖失敗: {se}")

        self.details.append({
            "step": step_name, 
            "status": "FAIL", 
            "time": duration, 
            "error": error_type,
            "screenshot": f"artifacts/{screenshot_name}" if driver else "-"
        })
        self.summary["fail"] += 1
        print(f"❌ [FAIL] {step_name} ({duration}s) -> 錯誤類型: {error_type}")

    def generate_report(self, file_name="測試報告.html"):
        """一鍵交卷：將數據渲染成漂亮的 HTML 網頁報告"""
        success_rate = (self.summary["pass"] / self.summary["total"]) * 100 if self.summary["total"] > 0 else 0
        
        html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{self.report_title}</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; margin: 30px; background-color: #f8fafc; color: #334155; }}
                h1 {{ color: #1e3a8a; }}
                .summary {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
                th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
                th {{ background-color: #f1f5f9; color: #1e3a8a; }}
                .badge-PASS {{ background: #dcfce7; color: #166534; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
                .badge-FAIL {{ background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>📊 {self.report_title}</h1>
            <div class="summary">
                <p><strong>執行時間：</strong> {self.start_time}</p>
                <p><strong>數據統計：</strong> 總案例: {self.summary['total']} | 成功: {self.summary['pass']} | 失敗: {self.summary['fail']} | <strong>成功率: {success_rate:.1f}%</strong></p>
            </div>
            <table>
                <thead>
                    <tr><th>測試步驟</th><th>狀態</th><th>耗時</th><th>錯誤分析</th><th>當下快照 / 備註</th></tr>
                </thead>
                <tbody>
        """
        for item in self.details:
            badge = f'<span class="badge-{item["status"]}">{item["status"]}</span>'
            if item["status"] == "FAIL" and item["screenshot"] != "-":
                evidence = f'<a href="{item["screenshot"]}" target="_blank">查看錯誤截圖</a>'
            elif item["status"] == "PASS" and "artifacts" in item["screenshot"]:
                evidence = f'<a href="{item["screenshot"]}" target="_blank">查看成功快照</a>'
            else:
                evidence = item["screenshot"]
            
            html += f"""
                <tr>
                    <td>{item['step']}</td>
                    <td>{badge}</td>
                    <td>{item['time']} 秒</td>
                    <td><code>{item['error']}</code></td>
                    <td>{evidence}</td>
                </tr>
            """
        html += "</tbody></table></body></html>"
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n🎉 [報告完成] 核心分析結果已寫入至：{file_name}")