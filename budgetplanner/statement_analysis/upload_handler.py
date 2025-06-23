import os
import json
from datetime import datetime
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from pdf_processor import BankStatementProcessor
import logging

logger = logging.getLogger(__name__)

class PDFUploadHandler:
    """Handle PDF uploads and convert to JSON format for the budget planner."""
    
    def __init__(self, upload_folder='uploads', allowed_extensions={'pdf'}):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self.processor = BankStatementProcessor()
        
        # Create upload folder if it doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
    
    def allowed_file(self, filename):
        """Check if the uploaded file has an allowed extension."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def process_upload(self, file):
        """Process an uploaded PDF file and return JSON data."""
        try:
            if file is None:
                return {'error': 'No file provided'}, 400
            
            if file.filename == '':
                return {'error': 'No file selected'}, 400
            
            if not self.allowed_file(file.filename):
                return {'error': 'Invalid file type. Only PDF files are allowed.'}, 400
            
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(self.upload_folder, safe_filename)
            
            file.save(file_path)
            logger.info(f"File saved to: {file_path}")
            
            # Process the PDF
            try:
                json_data = self.processor.process_pdf(file_path)
                logger.info(f"Successfully processed PDF: {filename}")
                
                # Clean up the uploaded file
                os.remove(file_path)
                
                return {
                    'success': True,
                    'data': json_data,
                    'filename': filename,
                    'message': 'PDF processed successfully'
                }
                
            except Exception as e:
                # Clean up the uploaded file on error
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                logger.error(f"Error processing PDF: {e}")
                return {
                    'error': f'Error processing PDF: {str(e)}'
                }, 500
                
        except Exception as e:
            logger.error(f"Error handling upload: {e}")
            return {'error': f'Upload error: {str(e)}'}, 500
    
    def save_to_bank_folder(self, json_data, filename):
        """Save the processed JSON data to the bank folder."""
        try:
            # Create bank folder if it doesn't exist
            bank_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bank')
            if not os.path.exists(bank_folder):
                os.makedirs(bank_folder)
            
            # Generate a safe filename for the JSON
            base_name = os.path.splitext(filename)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = f"bank_statement_{timestamp}.json"
            json_path = os.path.join(bank_folder, json_filename)
            
            # Save the JSON file
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"JSON saved to bank folder: {json_path}")
            return json_filename
            
        except Exception as e:
            logger.error(f"Error saving to bank folder: {e}")
            raise

# Global upload handler instance
upload_handler = PDFUploadHandler()

def handle_pdf_upload():
    """Flask route handler for PDF uploads."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        # Process the upload
        result = upload_handler.process_upload(file)
        
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        
        # If successful, save to bank folder
        if result.get('success'):
            json_filename = upload_handler.save_to_bank_folder(
                result['data'], 
                result['filename']
            )
            result['json_filename'] = json_filename
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in PDF upload handler: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500 