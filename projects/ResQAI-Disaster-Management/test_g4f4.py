import g4f
from g4f.Provider import Blackbox
try:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4o_mini,
        messages=[{"role": "user", "content": "Explain what a double earthquake is in 1 sentence."}],
        provider=Blackbox
    )
    print("Success:", response)
except Exception as e:
    print("Error:", e)
