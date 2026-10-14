import json
import os

DISASTER_FILE = 'data/disasters.json'

initial_data = [
    { "year": 2026, "lat": 38.0, "lng": 37.2, "country": "Turkey & Syria", "type": "Earthquake", "deaths": 59259, "desc": "A massive 7.8 magnitude earthquake devastated southern Turkey and northern Syria." },
    { "year": 2023, "lat": 31.4, "lng": -8.4, "country": "Morocco", "type": "Earthquake", "deaths": 2960, "desc": "A 6.8 magnitude earthquake struck the Marrakesh-Safi region." },
    { "year": 2015, "lat": 28.1, "lng": 84.7, "country": "Nepal", "type": "Earthquake", "deaths": 8964, "desc": "A severe 7.8 magnitude earthquake triggered avalanches on Mount Everest." },
    { "year": 2011, "lat": 38.3, "lng": 142.36, "country": "Japan", "type": "Earthquake / Tsunami", "deaths": 19759, "desc": "Tohoku earthquake triggered a massive tsunami and Fukushima nuclear disaster." },
    { "year": 2010, "lat": 18.59, "lng": -72.3, "country": "Haiti", "type": "Earthquake", "deaths": 220000, "desc": "Catastrophic 7.0 magnitude earthquake near the capital Port-au-Prince." },
    { "year": 2010, "lat": 55.75, "lng": 37.61, "country": "Russia", "type": "Heatwave", "deaths": 55000, "desc": "Record-breaking heatwave leading to massive wildfires and smog." },
    { "year": 2008, "lat": 31.0, "lng": 103.3, "country": "China (Sichuan)", "type": "Earthquake", "deaths": 87587, "desc": "Deadly 8.0 magnitude earthquake that leveled hundreds of towns." },
    { "year": 2005, "lat": 29.95, "lng": -89.87, "country": "USA (New Orleans)", "type": "Hurricane Katrina", "deaths": 1836, "desc": "Devastating Category 5 Atlantic hurricane that flooded New Orleans." },
    { "year": 2004, "lat": 3.3, "lng": 95.98, "country": "Indonesia (Sumatra)", "type": "Tsunami", "deaths": 227898, "desc": "Indian Ocean earthquake triggered tsunamis affecting 14 countries." }
]

if not os.path.exists(DISASTER_FILE):
    with open(DISASTER_FILE, 'w') as f:
        json.dump(initial_data, f)
