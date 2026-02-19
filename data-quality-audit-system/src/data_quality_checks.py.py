"""
Data quality check module for performing various quality audits
"""

import pandas as pd
import re
from datetime import datetime

class DataQualityChecker:
    def __init__(self):
        """Initialize the quality checker"""
        self.quality_issues = []
        self.audit_results = {}
    
    def check_completeness(self, df, column_name, threshold=95):
        """Check for missing values in a column"""
        total_rows = len(df)
        missing_count = df[column_name].isna().sum()
        missing_percentage = (missing_count / total_rows) * 100 if total_rows > 0 else 0
        
        result = {
            "check_type": "Completeness",
            "column": column_name,
            "total_records": total_rows,
            "missing_count": missing_count,
            "missing_percentage": round(missing_percentage, 2),
            "status": "PASS" if missing_percentage <= (100 - threshold) else "FAIL"
        }
        
        self.audit_results[f"completeness_{column_name}"] = result
        return result
    
    def check_uniqueness(self, df, column_name):
        """Check for duplicate values in a column"""
        total_rows = len(df)
        unique_count = df[column_name].nunique()
        duplicate_count = total_rows - unique_count
        duplicate_percentage = (duplicate_count / total_rows) * 100 if total_rows > 0 else 0
        
        result = {
            "check_type": "Uniqueness",
            "column": column_name,
            "total_records": total_rows,
            "unique_values": unique_count,
            "duplicate_count": duplicate_count,
            "duplicate_percentage": round(duplicate_percentage, 2),
            "status": "PASS" if duplicate_count == 0 else "FAIL"
        }
        
        self.audit_results[f"uniqueness_{column_name}"] = result
        return result
    
    def check_valid_email(self, df, email_column="email"):
        """Check for valid email formats"""
        def is_valid_email(email):
            if pd.isna(email):
                return False
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            return bool(re.match(pattern, str(email)))
        
        df["valid_email"] = df[email_column].apply(is_valid_email)
        invalid_count = (~df["valid_email"]).sum()
        total_count = len(df)
        invalid_percentage = (invalid_count / total_count) * 100 if total_count > 0 else 0
        
        result = {
            "check_type": "Email Validation",
            "column": email_column,
            "total_records": total_count,
            "invalid_count": invalid_count,
            "invalid_percentage": round(invalid_percentage, 2),
            "status": "PASS" if invalid_count == 0 else "FAIL"
        }
        
        self.audit_results["email_validation"] = result
        return result
    
    def check_date_consistency(self, df, start_date_col, end_date_col):
        """Check if end_date is after start_date"""
        df["date_valid"] = df[end_date_col] >= df[start_date_col]
        invalid_count = (~df["date_valid"]).sum()
        total_count = len(df)
        
        result = {
            "check_type": "Date Consistency",
            "columns": f"{start_date_col} vs {end_date_col}",
            "total_records": total_count,
            "invalid_records": invalid_count,
            "invalid_percentage": round((invalid_count/total_count)*100, 2) if total_count > 0 else 0,
            "status": "PASS" if invalid_count == 0 else "FAIL"
        }
        
        self.audit_results["date_consistency"] = result
        return result
    
    def check_range_validity(self, df, column_name, min_value, max_value):
        """Check if values are within expected range"""
        df["in_range"] = (df[column_name] >= min_value) & (df[column_name] <= max_value)
        out_of_range = (~df["in_range"]).sum()
        total_count = len(df)
        
        result = {
            "check_type": "Range Validity",
            "column": column_name,
            "expected_range": f"{min_value} to {max_value}",
            "total_records": total_count,
            "out_of_range": out_of_range,
            "out_of_range_percentage": round((out_of_range/total_count)*100, 2) if total_count > 0 else 0,
            "status": "PASS" if out_of_range == 0 else "FAIL"
        }
        
        self.audit_results[f"range_{column_name}"] = result
        return result
    
    def get_summary(self):
        """Get summary of all quality checks"""
        total_checks = len(self.audit_results)
        passed_checks = sum(1 for result in self.audit_results.values() 
                          if result["status"] == "PASS")
        failed_checks = total_checks - passed_checks
        
        summary = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "overall_status": "PASS" if failed_checks == 0 else "FAIL",
            "details": self.audit_results
        }
        
        return summary