import pdfplumber
import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BankStatementProcessor:
    """Process bank statement PDFs and convert to JSON format."""
    
    def __init__(self):
        self.bank_patterns = {
            'hdfc': {
                'name': 'HDFC Bank Ltd.',
                'patterns': {
                    'customer_name': r'Customer Name[:\s]*([^\n]+)',
                    'account_number': r'Account Number[:\s]*([^\n]+)',
                    'account_type': r'Account Type[:\s]*([^\n]+)',
                    'statement_period': r'Statement Period[:\s]*([^\n]+)',
                    'opening_balance': r'Opening Balance[:\s]*₹?([\d,]+\.?\d*)',
                    'closing_balance': r'Closing Balance[:\s]*₹?([\d,]+\.?\d*)'
                }
            },
            'sbi': {
                'name': 'State Bank of India',
                'patterns': {
                    'customer_name': r'Customer Name[:\s]*([^\n]+)',
                    'account_number': r'Account Number[:\s]*([^\n]+)',
                    'account_type': r'Account Type[:\s]*([^\n]+)',
                    'statement_period': r'Period[:\s]*([^\n]+)',
                    'opening_balance': r'Opening Balance[:\s]*₹?([\d,]+\.?\d*)',
                    'closing_balance': r'Closing Balance[:\s]*₹?([\d,]+\.?\d*)'
                }
            },
            'icici': {
                'name': 'ICICI Bank Ltd.',
                'patterns': {
                    'customer_name': r'Customer Name[:\s]*([^\n]+)',
                    'account_number': r'Account Number[:\s]*([^\n]+)',
                    'account_type': r'Account Type[:\s]*([^\n]+)',
                    'statement_period': r'Statement Period[:\s]*([^\n]+)',
                    'opening_balance': r'Opening Balance[:\s]*₹?([\d,]+\.?\d*)',
                    'closing_balance': r'Closing Balance[:\s]*₹?([\d,]+\.?\d*)'
                }
            }
        }
        
        # Transaction patterns for different banks
        self.transaction_patterns = {
            'hdfc': r'(\d{2}-[A-Za-z]{3}-\d{4})\s+([^\n]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            'sbi': r'(\d{2}-[A-Za-z]{3}-\d{4})\s+([^\n]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
            'icici': r'(\d{2}-[A-Za-z]{3}-\d{4})\s+([^\n]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)'
        }
    
    def detect_bank_type(self, text: str) -> str:
        """Detect the bank type from the PDF text."""
        text_lower = text.lower()
        
        if 'hdfc' in text_lower:
            return 'hdfc'
        elif 'state bank' in text_lower or 'sbi' in text_lower:
            return 'sbi'
        elif 'icici' in text_lower:
            return 'icici'
        else:
            # Default to HDFC pattern if unknown
            return 'hdfc'
    
    def extract_account_info(self, text: str, bank_type: str) -> Dict:
        """Extract account information from PDF text."""
        patterns = self.bank_patterns[bank_type]['patterns']
        account_info = {}
        
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # Clean up the value
                if field in ['opening_balance', 'closing_balance']:
                    value = float(value.replace(',', ''))
                account_info[field] = value
        
        return account_info
    
    def extract_transactions(self, text: str, bank_type: str) -> List[Dict]:
        """Extract transactions from PDF text."""
        transactions = []
        pattern = self.transaction_patterns[bank_type]
        
        # Find all transaction matches
        matches = re.finditer(pattern, text, re.MULTILINE)
        
        for match in matches:
            try:
                date = match.group(1)
                particulars = match.group(2).strip()
                cheque_no = match.group(3).strip()
                debit_str = match.group(4).replace(',', '')
                credit_str = match.group(5).replace(',', '')
                balance_str = match.group(6).replace(',', '')
                
                # Convert to float, handling empty values
                debit = float(debit_str) if debit_str and debit_str != '0.00' else 0.0
                credit = float(credit_str) if credit_str and credit_str != '0.00' else 0.0
                balance = float(balance_str) if balance_str else 0.0
                
                transaction = {
                    'date': date,
                    'particulars': particulars,
                    'cheque_no': cheque_no if cheque_no else '',
                    'debit': debit,
                    'credit': credit,
                    'balance': balance
                }
                
                transactions.append(transaction)
                
            except (ValueError, IndexError) as e:
                logger.warning(f"Error parsing transaction: {e}")
                continue
        
        return transactions
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text extracted from PDF."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """Process a PDF file and convert to JSON format."""
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Extract text from PDF
            full_text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + "\n"
            
            if not full_text.strip():
                raise ValueError("No text could be extracted from the PDF")
            
            # Clean the text
            full_text = self.clean_text(full_text)
            
            # Detect bank type
            bank_type = self.detect_bank_type(full_text)
            logger.info(f"Detected bank type: {bank_type}")
            
            # Extract account information
            account_info = self.extract_account_info(full_text, bank_type)
            logger.info(f"Extracted account info: {len(account_info)} fields")
            
            # Extract transactions
            transactions = self.extract_transactions(full_text, bank_type)
            logger.info(f"Extracted {len(transactions)} transactions")
            
            # Create the JSON structure
            result = {
                'bank': self.bank_patterns[bank_type]['name'],
                'account_info': account_info,
                'transactions': transactions
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise
    
    def save_json(self, data: Dict, output_path: str) -> str:
        """Save the processed data to a JSON file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"JSON saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            raise
    
    def process_and_save(self, pdf_path: str, output_dir: str = None) -> str:
        """Process PDF and save to JSON file."""
        # Process the PDF
        data = self.process_pdf(pdf_path)
        
        # Generate output filename
        if output_dir is None:
            output_dir = os.path.dirname(pdf_path)
        
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{base_name}_processed_{timestamp}.json"
        output_path = os.path.join(output_dir, output_filename)
        
        # Save the JSON
        return self.save_json(data, output_path) 