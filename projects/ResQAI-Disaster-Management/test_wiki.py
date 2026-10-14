import wikipedia
try:
    print(wikipedia.summary("9/11 attacks", sentences=3))
except Exception as e:
    print("Error:", type(e), e)
