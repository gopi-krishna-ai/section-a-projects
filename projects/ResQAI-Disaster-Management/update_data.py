import pandas as pd
import random

# Load the existing synthetic dataset
df = pd.read_csv('data/disaster_tweets.csv')

# Let's add a bunch of terrorism, attack, and violent disaster examples
new_disasters = [
    "A coordinated terrorist attack just occurred in the city center. Multiple casualties.",
    "The September 11 attacks were a series of four coordinated terrorist attacks against the United States.",
    "Breaking: Bomb explosion near the embassy. Emergency services rushing to the scene.",
    "Active shooter reported on the campus. Please shelter in place immediately.",
    "Gunfire heard downtown, police are heavily armed and cordoning off the street.",
    "Massive terrorist bombing leaves dozens injured. Hospitals are overwhelmed.",
    "Hijacked plane crashed into the building in a horrific terror attack.",
    "Suicide bomber detonated an explosive device at the checkpoint.",
    "Security forces neutralized the extremists during the hostage situation.",
    "Warning: Terrorist threat level raised to critical after recent attacks."
] * 20

# Add some non-disaster posts that use similar words in non-threatening contexts (to prevent overfitting)
new_normals = [
    "I had a heart attack when I saw the price of those shoes!",
    "My cat is a little terrorist, always knocking things off the table.",
    "This new spicy sauce is an absolute explosion of flavor in my mouth.",
    "The team executed a highly coordinated attack on the defense to score a goal.",
    "The marketing campaign was a total bomb, nobody bought the product."
] * 20

data = []
for text in new_disasters:
    data.append({'text': text, 'target': 1})
for text in new_normals:
    data.append({'text': text, 'target': 0})

new_df = pd.DataFrame(data)
combined_df = pd.concat([df, new_df], ignore_index=True)

# Shuffle the dataset
combined_df = combined_df.sample(frac=1).reset_index(drop=True)

# Save back to CSV
combined_df.to_csv('data/disaster_tweets.csv', index=False)
print("Updated dataset with terror/attack terminology.")
