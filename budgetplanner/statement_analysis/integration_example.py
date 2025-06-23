#!/usr/bin/env python3
"""
Integration Example for Statement Analysis Module
This script shows how to integrate the PDF processing functionality with the main budget planner application.
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path to import from the main app
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pdf_processor import BankStatementProcessor
from enhanced_processor import EnhancedBankStatementProcessor

def example_basic_processing():
    """Example of basic PDF processing."""
    print("=== Basic PDF Processing Example ===")
    
    # Initialize the processor
    processor = BankStatementProcessor()
    
    # Example PDF path (replace with actual path)
    pdf_path = "sample_statement.pdf"
    
    if os.path.exists(pdf_path):
        try:
            # Process the PDF
            result = processor.process_pdf(pdf_path)
            
            # Display results
            print(f"Bank: {result['bank']}")
            print(f"Customer: {result['account_info'].get('customer_name', 'N/A')}")
            print(f"Account: {result['account_info'].get('account_number', 'N/A')}")
            print(f"Transactions: {len(result['transactions'])}")
            
            # Save to JSON
            output_file = "basic_processed.json"
            processor.save_json(result, output_file)
            print(f"Results saved to: {output_file}")
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
    else:
        print(f"PDF file not found: {pdf_path}")
        print("Please place a sample bank statement PDF in the current directory.")

def example_enhanced_processing():
    """Example of enhanced PDF processing."""
    print("\n=== Enhanced PDF Processing Example ===")
    
    # Initialize the enhanced processor
    processor = EnhancedBankStatementProcessor()
    
    # Example PDF path (replace with actual path)
    pdf_path = "sample_statement.pdf"
    
    if os.path.exists(pdf_path):
        try:
            # Process the PDF
            result = processor.process_pdf(pdf_path)
            
            # Display results with enhanced info
            print(f"Bank: {result['bank']}")
            print(f"Customer: {result['account_info'].get('customer_name', 'N/A')}")
            print(f"Account: {result['account_info'].get('account_number', 'N/A')}")
            print(f"Transactions: {len(result['transactions'])}")
            
            # Display processing info
            if 'processing_info' in result:
                info = result['processing_info']
                print(f"Processed at: {info.get('processed_at', 'N/A')}")
                print(f"Bank type detected: {info.get('bank_type_detected', 'N/A')}")
                print(f"Pages processed: {info.get('pages_processed', 'N/A')}")
            
            # Save to JSON
            output_file = "enhanced_processed.json"
            processor.save_json(result, output_file)
            print(f"Results saved to: {output_file}")
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
    else:
        print(f"PDF file not found: {pdf_path}")
        print("Please place a sample bank statement PDF in the current directory.")

def example_flask_integration():
    """Example of Flask integration."""
    print("\n=== Flask Integration Example ===")
    
    # This shows how to integrate with the main Flask app
    flask_code = '''
# Add this to your main app.py file:

from statement_analysis.upload_handler import handle_pdf_upload

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """Handle PDF uploads and convert to JSON format."""
    return handle_pdf_upload()

# The upload handler will:
# 1. Accept PDF file uploads
# 2. Process the PDF using the statement analysis module
# 3. Convert to the required JSON format
# 4. Save the JSON file to the bank/ folder
# 5. Return success/error response
'''
    
    print("Flask Integration Code:")
    print(flask_code)
    
    # Example HTML form
    html_form = '''
<!-- Add this to your HTML template for file uploads -->
<form action="/upload-pdf" method="post" enctype="multipart/form-data">
    <div class="form-group">
        <label for="pdf_file">Upload Bank Statement (PDF):</label>
        <input type="file" id="pdf_file" name="file" accept=".pdf" required>
    </div>
    <button type="submit" class="btn btn-primary">Upload and Process</button>
</form>

<!-- JavaScript for handling the upload -->
<script>
document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/upload-pdf', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('PDF processed successfully!');
            // Optionally refresh the page or update the UI
            location.reload();
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Upload failed');
    });
});
</script>
'''
    
    print("\nHTML Form Example:")
    print(html_form)

def example_json_structure():
    """Show the expected JSON structure."""
    print("\n=== Expected JSON Structure ===")
    
    sample_structure = {
        "bank": "HDFC Bank Ltd.",
        "account_info": {
            "customer_name": "Mr. Aditya Sharma",
            "account_number": "XXXXXXXX3402",
            "account_type": "Savings Account",
            "statement_period": "01-May-2025 to 31-May-2025",
            "opening_balance": 46970.0,
            "closing_balance": 64016.24
        },
        "transactions": [
            {
                "date": "03-May-2025",
                "particulars": "ATM Withdrawal",
                "cheque_no": "",
                "debit": 9101.33,
                "credit": 0.0,
                "balance": 37868.67
            }
        ],
        "processing_info": {
            "processed_at": "2025-06-23T12:00:00",
            "bank_type_detected": "hdfc",
            "pages_processed": 1,
            "transactions_found": 10
        }
    }
    
    print("The processed JSON will have this structure:")
    print(json.dumps(sample_structure, indent=2))

def main():
    """Main function to run all examples."""
    print("Statement Analysis Module - Integration Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_processing()
    example_enhanced_processing()
    example_flask_integration()
    example_json_structure()
    
    print("\n" + "=" * 50)
    print("Integration Examples Completed!")
    print("\nTo use this module:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Add the upload route to your Flask app")
    print("3. Add a file upload form to your HTML")
    print("4. The processed JSON will be available in the bank/ folder")
    print("5. Users can select the processed statement in the main application")

if __name__ == "__main__":
    main() 