import pdfkit
import os
from flask import render_template
from config import Config

class PDFService:
    @staticmethod
    def generate_summary_pdf(application):
        html_content = '<html><body><h1>Citizen AI - Application Summary</h1>'
        html_content += f'<p>Application ID: {application.application_number}</p>'
        html_content += f'<p>Service: {application.service_type}</p>'
        html_content += f'<p>Status: {application.status}</p>'
        html_content += '<p><em>This is a generated prototype receipt.</em></p></body></html>'
        
        filename = f'{application.application_number}_summary.pdf'
        filepath = os.path.join(Config.GENERATED_FOLDER, filename)
        
        try:
            pdfkit.from_string(html_content, filepath)
            return filepath
        except Exception as e:
            print(f'PDF Generation error: {e}')
            return None

