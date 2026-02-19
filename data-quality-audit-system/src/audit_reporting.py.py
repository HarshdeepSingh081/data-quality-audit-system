"""
Audit reporting module for generating comprehensive reports
"""

import json
import csv
import pandas as pd
from datetime import datetime
import os

class AuditReporter:
    def __init__(self, output_dir="data/audit_reports"):
        """Initialize reporter with output directory"""
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_json_report(self, audit_results, filename=None):
        """Generate JSON format report"""
        if filename is None:
            filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(audit_results, f, indent=2, default=str)
        
        print(f"JSON report generated: {filepath}")
        return filepath
    
    def generate_csv_report(self, audit_results, filename=None):
        """Generate CSV format report"""
        if filename is None:
            filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Flatten the results for CSV
        flat_results = []
        for check_name, check_details in audit_results["details"].items():
            row = {
                "Check Name": check_name,
                "Timestamp": audit_results["timestamp"],
                "Status": check_details["status"]
            }
            # Add all other details
            for key, value in check_details.items():
                if key not in ["status"]:
                    row[key.capitalize()] = value
            flat_results.append(row)
        
        # Write to CSV
        if flat_results:
            df = pd.DataFrame(flat_results)
            df.to_csv(filepath, index=False)
        
        print(f"CSV report generated: {filepath}")
        return filepath
    
    def generate_html_report(self, audit_results, filename=None):
        """Generate HTML format report with styling"""
        if filename is None:
            filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # HTML template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Quality Audit Report - GlobalMart Inc.</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; }}
                .summary {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .pass {{ color: green; font-weight: bold; }}
                .fail {{ color: red; font-weight: bold; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .header {{ background-color: #333; color: white; padding: 10px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>GlobalMart Inc. - Data Quality Audit Report</h1>
            </div>
            
            <div class="summary">
                <h2>Executive Summary</h2>
                <p><strong>Report Generated:</strong> {audit_results['timestamp']}</p>
                <p><strong>Total Checks Performed:</strong> {audit_results['total_checks']}</p>
                <p><strong>Checks Passed:</strong> <span class="pass">{audit_results['passed_checks']}</span></p>
                <p><strong>Checks Failed:</strong> <span class="fail">{audit_results['failed_checks']}</span></p>
                <p><strong>Overall Data Quality Status:</strong> 
                    <span class="{audit_results['overall_status'].lower()}">
                        {audit_results['overall_status']}
                    </span>
                </p>
            </div>
            
            <h2>Detailed Quality Check Results</h2>
            <table>
                <tr>
                    <th>Check Name</th>
                    <th>Check Type</th>
                    <th>Details</th>
                    <th>Status</th>
                </tr>
        """
        
        # Add rows for each check
        for check_name, details in audit_results["details"].items():
            # Create details string
            detail_items = []
            for k, v in details.items():
                if k not in ["check_type", "status"]:
                    detail_items.append(f"<strong>{k}:</strong> {v}")
            details_str = "<br>".join(detail_items)
            
            html_content += f"""
                <tr>
                    <td>{check_name}</td>
                    <td>{details.get('check_type', 'N/A')}</td>
                    <td>{details_str}</td>
                    <td class="{details['status'].lower()}">{details['status']}</td>
                </tr>
            """
        
        html_content += """
            </table>
            <br>
            <hr>
            <p><em>This report is auto-generated by GlobalMart Data Quality Audit System</em></p>
        </body>
        </html>
        """
        
        with open(filepath, "w") as f:
            f.write(html_content)
        
        print(f"HTML report generated: {filepath}")
        return filepath
    
    def generate_all_reports(self, audit_results):
        """Generate all report formats"""
        json_file = self.generate_json_report(audit_results)
        csv_file = self.generate_csv_report(audit_results)
        html_file = self.generate_html_report(audit_results)
        
        return {
            "json": json_file,
            "csv": csv_file,
            "html": html_file
        }