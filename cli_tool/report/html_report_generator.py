from datetime import datetime
from abc import ABC
from typing import List

from report.report_generator import ReportGenerator


class HTMLReportGenerator(ReportGenerator):

    def generate(self, results: List[dict], file_path: str, report_name: str = None):
        data = self.prepare_data(results)
        content = self.render(data, file_path)
        output_path = self.make_outpath(report_name, file_path)
        self.write(content, output_path)

    def render(self, data: List[dict], contract_path: str):
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        safe_contract = len(data) == 0

        html_content = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Security Report - {contract_path}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 2em; background-color: #f7f7f7; }}
                h1 {{ color: #2c3e50; }}
                .section {{ background: white; padding: 1.5em; margin-bottom: 2em; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .code {{ background: #f0f0f0; padding: 1em; border-radius: 5px; white-space: pre-wrap; font-family: monospace; }}
                .safe {{ color: green; font-weight: bold; }}
                .vuln {{ color: red; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>Security Report: {contract_path}</h1>
            <p><strong>Generated on:</strong> {date_str}</p>
        """

        if safe_contract:
            html_content += """
                <div class="section">
                    <p class="safe">✅ No vulnerabilities found in the contract.</p>
                </div>
            </body>
            </html>"""
        else:
            for i, item in enumerate(data, start=1):
                html_content += f"""
                <div class="section">
                    <h2>Vulnerability #{i}: {item.get('vulnerability', 'Unknown')}</h2>
                    <p class="vuln">{item.get('description', 'No description available.')}</p>
                    
                    <h3>Vulnerable Code Snippet</h3>
                    <div class="code">{item.get('vulnerable_code', 'N/A')}</div>
                    
                    <h3>Remediation Snippet</h3>
                    <div class="code">{item.get('secure_code', 'N/A')}</div>
                </div>
                """
            html_content += "\n</body>\n</html>"

        return html_content


