with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

target = '''        from translator import translate_to_english
        english_question = translate_to_english(question)'''

replacement = '''        from translator import translate_to_english
        english_question = translate_to_english(question)
        
        # Intercept specific predefined questions to answer "from memory"
        eq_lower = english_question.lower().strip()
        user = get_logged_in_user()
        memory_reply = None
        
        if user:
            if "which crop" in eq_lower and "soil" in eq_lower:
                last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
                if last_crop_pred:
                    c_inputs = last_crop_pred.crop_inputs or {}
                    n = c_inputs.get("Nitrogen", 0)
                    p = c_inputs.get("Phosphorus", 0)
                    k = c_inputs.get("Potassium", 0)
                    ph = c_inputs.get("pH_Value", 6.5)
                    crop_name = last_crop_pred.predicted_crop
                    memory_reply = f"Based on your latest soil test (N: {n}, P: {p}, K: {k}, pH: {ph}), I recommend growing **{crop_name}**. This crop will thrive in your soil conditions!"
            elif "irrigate" in eq_lower or "water" in eq_lower:
                last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
                if last_crop_pred and last_crop_pred.predicted_crop:
                    crop = last_crop_pred.predicted_crop
                    memory_reply = f"Since you are growing **{crop}**, you should irrigate early in the morning. Make sure to monitor the soil moisture closely, as {crop} requires consistent watering but not waterlogging."
            elif "pest" in eq_lower or "control" in eq_lower:
                last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
                if last_crop_pred and last_crop_pred.predicted_crop:
                    crop = last_crop_pred.predicted_crop
                    memory_reply = f"For your **{crop}** field, inspect the leaves regularly. If you see pests, start with neem-based sprays as an organic first line of defense before using chemical pesticides."

        if memory_reply:
            reply = memory_reply
            source = "memory"
        else:'''

target2 = '''        reply, source = get_assistant_reply(english_question, language)
        # LLM replies already come back in the requested language (when the API
        # key is configured); only translate knowledge-base / fallback replies.
        if source == "llm":
            translated = reply
        else:
            translated = translate_text(reply, language)'''

replacement2 = '''            reply, source = get_assistant_reply(english_question, language)
        
        # LLM replies already come back in the requested language (when the API
        # key is configured); only translate knowledge-base / fallback replies.
        if source == "llm":
            translated = reply
        else:
            translated = translate_text(reply, language)'''

app_py = app_py.replace(target + '\n' + target2, replacement + '\n' + replacement2)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
print("Updated app.py with memory logic")
