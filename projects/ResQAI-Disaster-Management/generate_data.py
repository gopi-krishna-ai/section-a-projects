import pandas as pd
import random

disaster_tweets = [
    "Just felt a massive earthquake in San Francisco! #earthquake",
    "Terrible floods wiping out homes in the valley. We need help ASAP.",
    "Wildfire is spreading rapidly towards the city, please evacuate!",
    "Tsunami warning issued for the coastal areas. Move to higher ground.",
    "The hurricane just tore the roof off our house. #HurricaneAlert",
    "Emergency responders are trapped due to the landslide on Route 66.",
    "Building collapsed after the explosion in downtown.",
    "Severe thunderstorm warning and flash flood watch in effect.",
    "Forest fire is out of control. The smoke is suffocating.",
    "A train derailed near the station causing a massive chemical spill.",
    "Help! We are stuck on the roof, the water is rising fast. #flood",
    "Typhoon expected to make landfall tonight. Stock up on supplies.",
    "Tornado touchdown confirmed. Take cover immediately!",
    "Massive pileup on the highway due to the blizzard.",
    "Volcanic eruption reported, ash cloud spreading over the town."
] * 35

non_disaster_tweets = [
    "What a beautiful sunset today at the beach!",
    "Just ate the biggest burger of my life. I'm going to explode!",
    "This new action movie was a total disaster, terrible acting.",
    "Can't wait for the weekend, going hiking with friends.",
    "The amount of homework I have is a tragedy.",
    "My phone battery died right in the middle of the concert.",
    "Look at this cute puppy playing in the water!",
    "Traffic is a nightmare today, completely gridlocked.",
    "I'm totally blown away by this new album release.",
    "Just finished a great workout at the gym. Feeling strong.",
    "The football game last night was an absolute trainwreck for our team.",
    "Excited for the upcoming tech conference in San Francisco.",
    "Why is it so hot today? It feels like I'm melting.",
    "Enjoying a quiet evening with a good book and coffee.",
    "Happy birthday to my best friend! Let's party tonight!"
] * 35

data = []
for _ in range(500):
    data.append({'text': random.choice(disaster_tweets), 'target': 1})
    data.append({'text': random.choice(non_disaster_tweets), 'target': 0})

random.shuffle(data)

df = pd.DataFrame(data)
df.to_csv('data/disaster_tweets.csv', index=False)
print("Synthetic Disaster Tweets dataset created.")
