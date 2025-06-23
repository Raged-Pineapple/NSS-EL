#!/usr/bin/env python3
"""
Test script for the PDF Statement Processor
This script demonstrates how to use the BankStatementProcessor class.
"""

import os
import json
from pdf_processor import BankStatementProcessor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_processor():
    """Test the PDF processor with a sample PDF file."""
    
    # Initialize the processor
    processor = BankStatementProcessor()
    
    # Test PDF path (you would replace this with an actual PDF file)
    test_pdf_path = "sample_statement.pdf"
    
    # Check if test file exists
    if not os.path.exists(test_pdf_path):
        logger.warning(f"Test PDF file not found: {test_pdf_path}")
        logger.info("Please place a sample bank statement PDF in the current directory")
        logger.info("and update the test_pdf_path variable to test the processor.")
        return
    
    try:
        # Process the PDF
        logger.info(f"Processing PDF: {test_pdf_path}")
        result = processor.process_pdf(test_pdf_path)
        
        # Display results
        logger.info("Processing completed successfully!")
        logger.info(f"Bank: {result['bank']}")
        logger.info(f"Customer: {result['account_info'].get('customer_name', 'N/A')}")
        logger.info(f"Account: {result['account_info'].get('account_number', 'N/A')}")
        logger.info(f"Transactions: {len(result['transactions'])}")
        
        # Save to JSON file
        output_file = "test_output.json"
        processor.save_json(result, output_file)
        logger.info(f"Results saved to: {output_file}")
        
        # Display sample transactions
        if result['transactions']:
            logger.info("\nSample transactions:")
            for i, transaction in enumerate(result['transactions'][:3]):
                logger.info(f"  {i+1}. {transaction['date']} - {transaction['particulars']} - ₹{transaction['debit'] or transaction['credit']}")
        
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")

def create_sample_json():
    """Create a sample JSON file for testing purposes."""
    sample_data = {
        "bank": "HDFC Bank Ltd.",
        "account_info": {
            "customer_name": "Mr. Test User",
            "account_number": "XXXXXXXX1234",
            "account_type": "Savings Account",
            "statement_period": "01-Jun-2025 to 30-Jun-2025",
            "opening_balance": 50000.0,
            "closing_balance": 65000.0
        },
        "transactions": [
            {
                "date": "05-Jun-2025",
                "particulars": "Salary Credit",
                "cheque_no": "",
                "debit": 0.0,
                "credit": 50000.0,
                "balance": 100000.0
            },
            {
                "date": "10-Jun-2025",
                "particulars": "ATM Withdrawal",
                "cheque_no": "",
                "debit": 5000.0,
                "credit": 0.0,
                "balance": 95000.0
            },
            {
                "date": "15-Jun-2025",
                "particulars": "Online Payment",
                "cheque_no": "",
                "debit": 30000.0,
                "credit": 0.0,
                "balance": 65000.0
            }
        ]
    }
    
    with open("sample_output.json", "w") as f:
        json.dump(sample_data, f, indent=4)
    
    logger.info("Sample JSON file created: sample_output.json")

if __name__ == "__main__":
    logger.info("PDF Statement Processor Test")
    logger.info("=" * 40)
    
    # Create sample JSON for reference
    create_sample_json()
    
    # Test the processor
    test_processor()
    
    logger.info("\nTest completed!")
    logger.info("Check the generated files for results.") 