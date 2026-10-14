class ValidationEngine:
    @staticmethod
    def compare_fields(form_data, ocr_data):
        results = []
        
        for key, form_value in form_data.items():
            ocr_value = ocr_data.get(key)
            if not ocr_value:
                continue
                
            form_val_clean = str(form_value).strip().lower()
            ocr_val_clean = str(ocr_value).strip().lower()
            
            if form_val_clean == ocr_val_clean:
                status = 'Match'
                msg = 'Verified'
            else:
                status = 'Mismatch'
                msg = f'Form: {form_value} | Doc: {ocr_value}'
                
            results.append({
                'field': key,
                'form_value': form_value,
                'ocr_value': ocr_value,
                'status': status,
                'message': msg
            })
            
        return results

