"""
Main module for GlobalMart Data Quality Audit System
"""

from data_extraction import DataExtractor
from data_quality_checks import DataQualityChecker
from audit_reporting import AuditReporter

def main():
    print("=" * 60)
    print("GlobalMart Inc. - Data Quality Audit System")
    print("=" * 60)
    
    # Initialize components
    extractor = DataExtractor()
    checker = DataQualityChecker()
    reporter = AuditReporter()
    
    try:
        # Extract data from tables
        print("\n1. Extracting data from database...")
        customers_df = extractor.get_table_data("customers")
        orders_df = extractor.get_table_data("orders")
        products_df = extractor.get_table_data("products")
        order_items_df = extractor.get_table_data("order_items")
        
        print(f"   - Customers: {len(customers_df)} records")
        print(f"   - Orders: {len(orders_df)} records")
        print(f"   - Products: {len(products_df)} records")
        print(f"   - Order Items: {len(order_items_df)} records")
        
        # Perform quality checks
        print("\n2. Performing data quality checks...")
        
        # Customer checks
        if len(customers_df) > 0:
            checker.check_completeness(customers_df, "email")
            checker.check_completeness(customers_df, "phone")
            checker.check_valid_email(customers_df, "email")
            checker.check_uniqueness(customers_df, "customer_id")
            print("   - Customer checks completed")
        
        # Order checks
        if len(orders_df) > 0:
            checker.check_date_consistency(orders_df, "order_date", "shipped_date")
            print("   - Order checks completed")
        
        # Product checks
        if len(products_df) > 0:
            checker.check_completeness(products_df, "stock_quantity")
            checker.check_range_validity(products_df, "unit_price", 0, 10000)
            print("   - Product checks completed")
        
        # Order items checks
        if len(order_items_df) > 0:
            checker.check_range_validity(order_items_df, "quantity", 1, 1000)
            print("   - Order items checks completed")
        
        # Generate summary
        summary = checker.get_summary()
        
        print(f"\n3. Audit Summary:")
        print(f"   - Total Checks: {summary['total_checks']}")
        print(f"   - Passed: {summary['passed_checks']}")
        print(f"   - Failed: {summary['failed_checks']}")
        print(f"   - Overall Status: {summary['overall_status']}")
        
        # Generate reports
        print("\n4. Generating reports...")
        report_files = reporter.generate_all_reports(summary)
        
        print("\n" + "=" * 60)
        print("Audit completed successfully!")
        print("=" * 60)
        print(f"\nReports saved in: {reporter.output_dir}")
        
    except Exception as e:
        print(f"\nError during audit process: {e}")
    
    finally:
        # Close database connection
        extractor.close_connection()

if __name__ == "__main__":
    main()