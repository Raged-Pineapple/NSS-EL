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

class EnhancedBankStatementProcessor:
    """Enhanced PDF processor with better pattern matching and support for various formats."""
    
    def __init__(self):
        # Enhanced bank patterns with multiple regex variations
        self.bank_patterns = {
            'hdfc': {
                'name': 'HDFC Bank Ltd.',
                'patterns': {
                    'customer_name': [
                        r'Customer Name[:\s]*([^\n\r]+)',
                        r'Name[:\s]*([^\n\r]+)',
                        r'Account Holder[:\s]*([^\n\r]+)'
                    ],
                    'account_number': [
                        r'Account Number[:\s]*([^\n\r]+)',
                        r'Account No[:\s]*([^\n\r]+)',
                        r'Acc\. No[:\s]*([^\n\r]+)'
                    ],
                    'account_type': [
                        r'Account Type[:\s]*([^\n\r]+)',
                        r'Type of Account[:\s]*([^\n\r]+)'
                    ],
                    'statement_period': [
                        r'Statement Period[:\s]*([^\n\r]+)',
                        r'Period[:\s]*([^\n\r]+)',
                        r'From[:\s]*([^\n\r]+)\s*To[:\s]*([^\n\r]+)'
                    ],
                    'opening_balance': [
                        r'Opening Balance[:\s]*₹?([\d,]+\.?\d*)',
                        r'Opening Bal[:\s]*₹?([\d,]+\.?\d*)',
                        r'Balance B/F[:\s]*₹?([\d,]+\.?\d*)'
                    ],
                    'closing_balance': [
                        r'Closing Balance[:\s]*₹?([\d,]+\.?\d*)',
                        r'Closing Bal[:\s]*₹?([\d,]+\.?\d*)',
                        r'Balance C/F[:\s]*₹?([\d,]+\.?\d*)'
                    ]
                }
            },
            'sbi': {
                'name': 'State Bank of India',
                'patterns': {
                    'customer_name': [
                        r'Customer Name[:\s]*([^\n\r]+)',
                        r'Name[:\s]*([^\n\r]+)',
                        r'Account Holder[:\s]*([^\n\r]+)'
                    ],
                    'account_number': [
                        r'Account Number[:\s]*([^\n\r]+)',
                        r'Account No[:\s]*([^\n\r]+)',
                        r'Acc\. No[:\s]*([^\n\r]+)'
                    ],
                    'account_type': [
                        r'Account Type[:\s]*([^\n\r]+)',
                        r'Type of Account[:\s]*([^\n\r]+)'
                    ],
                    'statement_period': [
                        r'Statement Period[:\s]*([^\n\r]+)',
                        r'Period[:\s]*([^\n\r]+)',
                        r'From[:\s]*([^\n\r]+)\s*To[:\s]*([^\n\r]+)'
                    ],
                    'opening_balance': [
                        r'Opening Balance[:\s]*₹?([\d,]+\.?\d*)',
                        r'Opening Bal[:\s]*₹?([\d,]+\.?\d*)',
                        r'Balance B/F[:\s]*₹?([\d,]+\.?\d*)'
                    ],
                    'closing_balance': [
                        r'Closing Balance[:\s]*₹?([\d,]+\.?\d*)',
                        r'Closing Bal[:\s]*₹?([\d,]+\.?\d*)',
                        r'Balance C/F[:\s]*₹?([\d,]+\.?\d*)'
                    ]
                }
            },
            'icici': {
                'name': 'ICICI Bank Ltd.',
                'patterns': {
                    'customer_name': [
                        r'Customer Name[:\s]*([^\n\r]+)',
                        r'Name[:\s]*([^\n\r]+)',
                        r'Account Holder[:\s]*([^\n\r]+)'
                    ],
                    'account_number': [
                        r'Account Number[:\s]*([^\n\r]+)',
                        r'Account No[:\s]*([^\n\r]+)',
                        r'Acc\. No[:\s]*([^\n\r]+)'
                    ],
                    'account_type': [
                        r'Account Type[:\s]*([^\n\r]+)',
                        r'Type of Account[:\s]*([^\n\r]+)'
                    ],
                    'statement_period': [
                        r'Statement Period[:\s]*([^\n\r]+)',
                        r'Period[:\s]*([^\n\r]+)',
                        r'From[:\s]*([^\n\r]+)\s*To[:\s]*([^\n\r]+)'
                    ],
                    'opening_balance': [
                        r'Opening Balance[:\s]*₹?([\d,]+\.?\d*)',
                        r'Opening Bal[:\s]*₹?([\d,]+\.?\d*)',
                        r'Balance B/F[:\s]*₹?([\d,]+\.?\d*)'
                    ],
                    'closing_balance': [
                        r'Closing Balance[:\s]*₹?([\d,]+\.?\d*)',
                        r'Closing Bal[:\s]*₹?([\d,]+\.?\d*)',
                        r'Balance C/F[:\s]*₹?([\d,]+\.?\d*)'
                    ]
                }
            }
        }
        
        # Enhanced transaction patterns with multiple variations
        self.transaction_patterns = {
            'hdfc': [
                r'(\d{2}-[A-Za-z]{3}-\d{4})\s+([^\n\r]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'(\d{2}/\d{2}/\d{4})\s+([^\n\r]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'(\d{2}\.\d{2}\.\d{4})\s+([^\n\r]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)'
            ],
            'sbi': [
                r'(\d{2}-[A-Za-z]{3}-\d{4})\s+([^\n\r]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'(\d{2}/\d{2}/\d{4})\s+([^\n\r]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)'
            ],
            'icici': [
                r'(\d{2}-[A-Za-z]{3}-\d{4})\s+([^\n\r]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)',
                r'(\d{2}/\d{2}/\d{4})\s+([^\n\r]+?)\s+([A-Z0-9]*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)\s+([\d,]+\.?\d*)'
            ]
        }
    
    def detect_bank_type(self, text: str) -> str:
        """Enhanced bank type detection with confidence scoring."""
        text_lower = text.lower()
        
        bank_scores = {
            'hdfc': 0,
            'sbi': 0,
            'icici': 0
        }
        
        # Score based on bank name mentions
        if 'hdfc' in text_lower:
            bank_scores['hdfc'] += 3
        if 'state bank' in text_lower or 'sbi' in text_lower:
            bank_scores['sbi'] += 3
        if 'icici' in text_lower:
            bank_scores['icici'] += 3
        
        # Score based on specific patterns
        if re.search(r'HDFC\s+Bank', text, re.IGNORECASE):
            bank_scores['hdfc'] += 2
        if re.search(r'State\s+Bank\s+of\s+India', text, re.IGNORECASE):
            bank_scores['sbi'] += 2
        if re.search(r'ICICI\s+Bank', text, re.IGNORECASE):
            bank_scores['icici'] += 2
        
        # Return the bank with highest score
        detected_bank = max(bank_scores, key=bank_scores.get)
        logger.info(f"Bank detection scores: {bank_scores}")
        logger.info(f"Detected bank: {detected_bank}")
        
        return detected_bank
    
    def extract_account_info(self, text: str, bank_type: str) -> Dict:
        """Enhanced account information extraction with multiple pattern matching."""
        patterns = self.bank_patterns[bank_type]['patterns']
        account_info = {}
        
        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    if field == 'statement_period' and len(match.groups()) > 1:
                        # Handle "From X To Y" format
                        value = f"{match.group(1)} to {match.group(2)}"
                    else:
                        value = match.group(1).strip()
                    
                    # Clean up the value
                    if field in ['opening_balance', 'closing_balance']:
                        try:
                            value = float(value.replace(',', ''))
                        except ValueError:
                            continue
                    
                    account_info[field] = value
                    logger.info(f"Extracted {field}: {value}")
                    break  # Use first successful match
        
        return account_info
    
    def extract_transactions(self, text: str, bank_type: str) -> List[Dict]:
        """Enhanced transaction extraction with multiple pattern support."""
        transactions = []
        patterns = self.transaction_patterns[bank_type]
        
        for pattern in patterns:
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
                    
                    # Validate transaction data
                    if not particulars or (debit == 0.0 and credit == 0.0):
                        continue
                    
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
            
            # If we found transactions with this pattern, use it
            if transactions:
                logger.info(f"Found {len(transactions)} transactions using pattern")
                break
        
        return transactions
    
    def clean_text(self, text: str) -> str:
        """Enhanced text cleaning with better normalization."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
        text = re.sub(r'\f', '\n', text)  # Replace form feeds with newlines
        
        return text.strip()
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """Enhanced PDF processing with better error handling and validation."""
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Extract text from PDF
            full_text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        full_text += f"Page {page_num + 1}:\n{text}\n"
            
            if not full_text.strip():
                raise ValueError("No text could be extracted from the PDF")
            
            # Clean the text
            full_text = self.clean_text(full_text)
            
            # Detect bank type
            bank_type = self.detect_bank_type(full_text)
            
            # Extract account information
            account_info = self.extract_account_info(full_text, bank_type)
            
            # Extract transactions
            transactions = self.extract_transactions(full_text, bank_type)
            
            # Validate extracted data
            if not account_info:
                logger.warning("No account information extracted")
            
            if not transactions:
                logger.warning("No transactions extracted")
            
            # Create the JSON structure
            result = {
                'bank': self.bank_patterns[bank_type]['name'],
                'account_info': account_info,
                'transactions': transactions,
                'processing_info': {
                    'processed_at': datetime.now().isoformat(),
                    'bank_type_detected': bank_type,
                    'pages_processed': len(pdf.pages) if 'pdf' in locals() else 0,
                    'transactions_found': len(transactions)
                }
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