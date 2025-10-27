#!/usr/bin/env python3
"""
Tax Master - Main Application

This is the main entry point for the Tax Master application.
It orchestrates the tax calculation workflow by loading sales data,
applying tax rules, and generating comprehensive reports.
"""

import csv
import sys
from datetime import datetime
from tax_rules import TaxCalculator, TAX_RATES


def load_sales_data(filename='sales_data.csv'):
    """
    Load sales data from CSV file.
    
    Args:
        filename (str): Path to the CSV file containing sales data
        
    Returns:
        list: List of dictionaries containing sales records
    """
    sales_data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                sales_data.append(row)
        print(f"✓ Successfully loaded {len(sales_data)} sales records from {filename}")
    except FileNotFoundError:
        print(f"✗ Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading sales data: {e}")
        sys.exit(1)
    
    return sales_data


def process_sales(sales_data):
    """
    Process sales data and calculate taxes.
    
    Args:
        sales_data (list): List of sales records
        
    Returns:
        tuple: (processed_records, total_sales, total_tax)
    """
    calculator = TaxCalculator()
    processed_records = []
    total_sales = 0.0
    total_tax = 0.0
    
    print("\n" + "="*80)
    print("Processing Sales Transactions")
    print("="*80)
    
    for record in sales_data:
        try:
            transaction_id = record.get('transaction_id', 'N/A')
            amount = float(record.get('amount', 0))
            category = record.get('category', 'standard')
            
            # Calculate tax for this transaction
            tax_amount = calculator.calculate_tax(amount, category)
            total_amount = amount + tax_amount
            
            # Store processed record
            processed_record = {
                'transaction_id': transaction_id,
                'amount': amount,
                'category': category,
                'tax_rate': TAX_RATES.get(category, TAX_RATES['standard']),
                'tax_amount': tax_amount,
                'total_amount': total_amount
            }
            processed_records.append(processed_record)
            
            # Update totals
            total_sales += amount
            total_tax += tax_amount
            
            # Display transaction details
            print(f"Transaction {transaction_id}: ${amount:.2f} + ${tax_amount:.2f} tax = ${total_amount:.2f}")
            
        except (ValueError, KeyError) as e:
            print(f"✗ Error processing record {record.get('transaction_id', 'unknown')}: {e}")
            continue
    
    return processed_records, total_sales, total_tax


def generate_report(processed_records, total_sales, total_tax):
    """
    Generate and display tax calculation report.
    
    Args:
        processed_records (list): List of processed sales records
        total_sales (float): Total sales amount before tax
        total_tax (float): Total tax amount
    """
    total_revenue = total_sales + total_tax
    
    print("\n" + "="*80)
    print("TAX CALCULATION REPORT")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTotal Transactions: {len(processed_records)}")
    print(f"Total Sales (pre-tax): ${total_sales:,.2f}")
    print(f"Total Tax Collected: ${total_tax:,.2f}")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    
    # Category breakdown
    print("\n" + "-"*80)
    print("Category Breakdown:")
    print("-"*80)
    
    categories = {}
    for record in processed_records:
        cat = record['category']
        if cat not in categories:
            categories[cat] = {'count': 0, 'sales': 0, 'tax': 0}
        categories[cat]['count'] += 1
        categories[cat]['sales'] += record['amount']
        categories[cat]['tax'] += record['tax_amount']
    
    for category, data in sorted(categories.items()):
        print(f"\n{category.upper()}:")
        print(f"  Transactions: {data['count']}")
        print(f"  Sales: ${data['sales']:,.2f}")
        print(f"  Tax: ${data['tax']:,.2f}")
        print(f"  Rate: {TAX_RATES.get(category, 0)*100:.1f}%")
    
    print("\n" + "="*80)


def main():
    """
    Main function to run the Tax Master application.
    """
    print("\n" + "="*80)
    print("TAX MASTER - Tax Calculation System")
    print("="*80)
    print("Version: 1.0.0")
    print("Author: palyam123")
    print("="*80 + "\n")
    
    # Load sales data
    sales_data = load_sales_data('sales_data.csv')
    
    if not sales_data:
        print("\n✗ No sales data to process.")
        return
    
    # Process sales and calculate taxes
    processed_records, total_sales, total_tax = process_sales(sales_data)
    
    # Generate comprehensive report
    generate_report(processed_records, total_sales, total_tax)
    
    print("\n✓ Tax calculation completed successfully!\n")


if __name__ == '__main__':
    main()
