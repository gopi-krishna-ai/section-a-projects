from g4f.client import Client

client = Client()
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, are you working?"}]
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)
