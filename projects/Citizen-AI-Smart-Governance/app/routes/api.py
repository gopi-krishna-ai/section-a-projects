from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.ai.chatbot import ChatbotEngine
from app.ai.ocr_engine import OCREngine
from app.ai.validation_engine import ValidationEngine
import os

bp = Blueprint('api', __name__, url_prefix='/api')
chatbot = ChatbotEngine()
ocr = OCREngine()

@bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    service = data.get('service', 'PAN')
    field = data.get('field', 'fullname')
    language = data.get('language', 'en')
    
    # Simple intent matching
    if 'explain' in message.lower() or 'what' in message.lower() or 'how' in message.lower():
        response = chatbot.get_guidance(service, field, language)
    elif 'example' in message.lower():
        response = "Here is an example: Ravi Kumar. Make sure it matches your document."
    else:
        response = "I am your Citizen AI assistant. I can explain fields, provide examples, or help validate your entries. What do you need help with?"
        
    return jsonify({'response': response, 'status': 'success'})

@bp.route('/upload', methods=['POST'])
def upload_document():
    if 'document' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Run OCR
        extracted_text = ocr.extract_text(filepath)
        extracted_fields = ocr.parse_fields(extracted_text, 'PAN')
        
        return jsonify({
            'status': 'success',
            'extracted_fields': extracted_fields,
            'message': 'Document processed successfully.'
        })
