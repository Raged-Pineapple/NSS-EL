# Statement Analysis Module

This module provides functionality to convert bank statement PDFs into the JSON format required by the Smart Budget Planner application.

## Features

- **PDF Processing**: Extract text and data from bank statement PDFs
- **Multi-Bank Support**: Supports HDFC, SBI, and ICICI bank statements
- **JSON Conversion**: Converts extracted data to the required JSON format
- **Flask Integration**: Seamless integration with the main budget planner application
- **Error Handling**: Robust error handling and logging

## File Structure

```
statement_analysis/
├── pdf_processor.py      # Core PDF processing functionality
├── upload_handler.py     # Flask upload handler
├── test_processor.py     # Test script
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic PDF Processing

```python
from pdf_processor import BankStatementProcessor

# Initialize the processor
processor = BankStatementProcessor()

# Process a PDF file
result = processor.process_pdf("path/to/statement.pdf")

# Save to JSON
processor.save_json(result, "output.json")
```

### Flask Integration

The module includes a Flask upload handler that can be integrated into the main application:

```python
from upload_handler import handle_pdf_upload

# Add this route to your Flask app
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    return handle_pdf_upload()
```

## Supported Bank Formats

### HDFC Bank
- Customer Name
- Account Number
- Account Type
- Statement Period
- Opening/Closing Balance
- Transaction details with date, particulars, cheque number, debit, credit, and balance

### State Bank of India (SBI)
- Similar structure to HDFC
- Adapted patterns for SBI-specific formatting

### ICICI Bank
- Similar structure to HDFC
- Adapted patterns for ICICI-specific formatting

## JSON Output Format

The processed PDF is converted to the following JSON structure:

```json
{
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
    ]
}
```

## Testing

Run the test script to verify the functionality:

```bash
python test_processor.py
```

This will:
1. Create a sample JSON file for reference
2. Attempt to process a sample PDF (if available)
3. Display processing results

## Error Handling

The module includes comprehensive error handling for:
- Invalid PDF files
- Unsupported bank formats
- Missing or corrupted data
- File I/O errors
- Network errors (for uploads)

## Logging

The module uses Python's logging module to provide detailed information about:
- Processing steps
- Extracted data
- Errors and warnings
- File operations

## Integration with Main Application

To integrate this module with the main budget planner application:

1. Add the upload route to `app.py`:
```python
from statement_analysis.upload_handler import handle_pdf_upload

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    return handle_pdf_upload()
```

2. Update the frontend to include a file upload form
3. The processed JSON will be automatically saved to the `bank/` folder
4. The JSON file will be available for selection in the main application

## Dependencies

- `pdfplumber`: PDF text extraction
- `flask`: Web framework integration
- `werkzeug`: File upload handling
- `python-dotenv`: Environment variable management
- `typing`: Type hints

## Notes

- The module automatically detects bank type based on PDF content
- Files are securely handled with timestamped names
- Uploaded PDFs are automatically cleaned up after processing
- The module supports multiple PDF formats and layouts
- Error messages are user-friendly and informative 