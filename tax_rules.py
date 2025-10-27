#!/usr/bin/env python3
"""
Tax Rules Module

This module contains tax calculation functions based on specific rules:
- For INDIA: Items with rate > 2000 are taxed at 10%, items with rate <= 2000 are tax-exempt
- For other countries: All items are tax-exempt regardless of rate

The module also provides functions to manage tax structures and apply them to sales data.
"""

import csv
import os


# Tax rate constants
INDIA_TAX_RATE = 0.10  # 10% tax rate for items > 2000 in India
INDIA_TAX_THRESHOLD = 2000  # Items with rate <= 2000 are tax-exempt in India


def calculate_tax_amount(item_rate, item_quantity, country_code):
    """
    Calculate tax amount for an item based on country code and item rate.
    
    Tax Rules:
    - INDIA: Items with rate > 2000 are taxed at 10%, otherwise tax-exempt
    - Other countries: All items are tax-exempt
    
    Args:
        item_rate (float): Rate per unit of the item
        item_quantity (int): Quantity of items
        country_code (str): Country code (e.g., 'INDIA', 'USA', 'UK')
    
    Returns:
        float: Calculated tax amount
    """
    item_amount = item_rate * item_quantity
    
    # Check if country is India
    if country_code.upper() == 'INDIA':
        # Apply tax only if item rate exceeds threshold
        if item_rate > INDIA_TAX_THRESHOLD:
            tax_amount = item_amount * INDIA_TAX_RATE
        else:
            tax_amount = 0.0
    else:
        # All items are tax-exempt for countries other than India
        tax_amount = 0.0
    
    return round(tax_amount, 2)


def calculate_total_amount(item_rate, item_quantity, tax_amount):
    """
    Calculate total amount including tax.
    
    Args:
        item_rate (float): Rate per unit of the item
        item_quantity (int): Quantity of items
        tax_amount (float): Calculated tax amount
    
    Returns:
        float: Total amount (item amount + tax amount)
    """
    item_amount = item_rate * item_quantity
    total_amount = item_amount + tax_amount
    return round(total_amount, 2)


def get_tax_status(item_rate, country_code):
    """
    Determine if an item is taxable or tax-exempt.
    
    Args:
        item_rate (float): Rate per unit of the item
        country_code (str): Country code
    
    Returns:
        str: 'Taxable' or 'Tax-Exempt'
    """
    if country_code.upper() == 'INDIA':
        if item_rate > INDIA_TAX_THRESHOLD:
            return 'Taxable'
        else:
            return 'Tax-Exempt'
    else:
        return 'Tax-Exempt'


def update_sales_record_with_tax(record):
    """
    Update a sales record with calculated tax information.
    
    Args:
        record (dict): Sales record dictionary with keys:
                      'Transaction Date', 'Customer Name', 'Country Code',
                      'Item Name', 'Item Rate', 'Item Quantity'
    
    Returns:
        dict: Updated record with tax calculations
    """
    try:
        item_rate = float(record['Item Rate'])
        item_quantity = int(record['Item Quantity'])
        country_code = record['Country Code']
        
        # Calculate amounts
        item_amount = round(item_rate * item_quantity, 2)
        tax_amount = calculate_tax_amount(item_rate, item_quantity, country_code)
        total_amount = calculate_total_amount(item_rate, item_quantity, tax_amount)
        
        # Update record with calculated values
        record['Item Amount'] = item_amount
        record['Tax Amount'] = tax_amount
        record['Total Amount'] = total_amount
        
        return record
    except (KeyError, ValueError) as e:
        print(f"Error processing record: {e}")
        return None


def load_sales_data(filename='sales_data.csv'):
    """
    Load sales data from CSV file.
    
    Args:
        filename (str): Path to the CSV file
    
    Returns:
        list: List of sales records as dictionaries
    """
    sales_data = []
    
    if not os.path.exists(filename):
        print(f"Warning: File '{filename}' not found.")
        return sales_data
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                sales_data.append(row)
        print(f"Successfully loaded {len(sales_data)} records from {filename}")
    except Exception as e:
        print(f"Error loading sales data: {e}")
    
    return sales_data


def save_sales_data(sales_data, filename='sales_data.csv'):
    """
    Save sales data to CSV file.
    
    Args:
        sales_data (list): List of sales records
        filename (str): Path to the CSV file
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not sales_data:
        print("No data to save.")
        return False
    
    try:
        fieldnames = ['Transaction Date', 'Customer Name', 'Country Code', 'Item Name',
                     'Item Rate', 'Item Quantity', 'Item Amount', 'Tax Amount', 'Total Amount']
        
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sales_data)
        
        print(f"Successfully saved {len(sales_data)} records to {filename}")
        return True
    except Exception as e:
        print(f"Error saving sales data: {e}")
        return False


def display_tax_rules():
    """
    Display current tax rules for reference.
    """
    print("\n" + "="*70)
    print("CURRENT TAX RULES")
    print("="*70)
    print(f"\nFor INDIA:")
    print(f"  - Items with rate > {INDIA_TAX_THRESHOLD}: {INDIA_TAX_RATE*100}% tax")
    print(f"  - Items with rate ≤ {INDIA_TAX_THRESHOLD}: Tax-Exempt")
    print(f"\nFor other countries:")
    print(f"  - All items: Tax-Exempt")
    print("="*70 + "\n")


if __name__ == '__main__':
    # Display tax rules when module is run directly
    display_tax_rules()
