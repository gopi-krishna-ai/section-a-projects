import os

def start_loading():
    # No heavy background loading needed for API
    pass

def get_tutor_response(store, user_message):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return (
            "Hello! I am currently running in 'mock' mode because no `GEMINI_API_KEY` was found. "
            "To enable my advanced RAG & LLM capabilities, please get a free API key from Google AI Studio, "
            "set it in your environment (`set GEMINI_API_KEY=your_key`), and restart the server!\n\n"
            f"You asked: {user_message}"
        )
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        # Prepare study context
        subjects = store.get("subjects", {})
        context_lines = []
        for sub, data in subjects.items():
            completed = data.get('completed_topics', 0)
            total = data.get('total_topics', 1)
            exam = data.get('exam_date', 'unknown date')
            context_lines.append(f"- {sub}: {completed}/{total} topics done. Exam on {exam}.")
        
        study_context = "\n".join(context_lines)
        if not study_context:
            study_context = "The student hasn't added any subjects yet."
            
        system_prompt = (
            "You are a helpful, encouraging AI study tutor. You help students plan their studies, "
            "explain concepts, and keep them motivated. Keep answers concise and friendly.\n"
            f"Here is the student's current study context:\n{study_context}"
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"System: {system_prompt}\n\nUser: {user_message}"
        )
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error connecting to the AI: {str(e)}"
