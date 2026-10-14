import re

# 1. Update recommendation.html
with open('templates/recommendation.html', 'r', encoding='utf-8') as f:
    rec_content = f.read()

old_fetch = """function fetchLocation(lat, lon) {
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
            .then(r => r.json())
            .then(data => {
                const name = data.address.city || data.address.town || data.address.village || data.address.county || "Selected Area";
                document.getElementById('locationText').innerHTML = `dY"? ${name}`;
            }).catch(() => {
                document.getElementById('locationText').innerHTML = `dY"? Coordinates (${lat.toFixed(2)}, ${lon.toFixed(2)})`;
            });
    }"""

new_fetch = """function fetchLocation(lat, lon) {
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
            .then(r => r.json())
            .then(data => {
                const name = data.address.city || data.address.town || data.address.village || data.address.county || "Selected Area";
                document.getElementById('locationText').innerHTML = `📍 ${name}`;
                sessionStorage.setItem('farmAddress', name + ` (${lat.toFixed(4)}, ${lon.toFixed(4)})`);
            }).catch(() => {
                const fallback = `Coordinates (${lat.toFixed(2)}, ${lon.toFixed(2)})`;
                document.getElementById('locationText').innerHTML = `📍 ${fallback}`;
                sessionStorage.setItem('farmAddress', fallback);
            });
    }"""

# The text contains `dY"?`, which is a botched emoji (📍). I'll replace it with the emoji.
# I'll just use regex to insert the sessionStorage line dynamically to avoid copy-paste errors on the weird characters.
def replace_fetch(match):
    return match.group(0).replace(
        "document.getElementById('locationText').innerHTML = `dY\"? ${name}`;", 
        "document.getElementById('locationText').innerHTML = `dY\"? ${name}`;\n                sessionStorage.setItem('farmAddress', name + ` (${lat.toFixed(4)}, ${lon.toFixed(4)})`);"
    ).replace(
        "document.getElementById('locationText').innerHTML = `dY\"? Coordinates (${lat.toFixed(2)}, ${lon.toFixed(2)})`;",
        "document.getElementById('locationText').innerHTML = `dY\"? Coordinates (${lat.toFixed(2)}, ${lon.toFixed(2)})`;\n                sessionStorage.setItem('farmAddress', `Coordinates (${lat.toFixed(4)}, ${lon.toFixed(4)})`);"
    )

rec_content = re.sub(r'function fetchLocation\(lat, lon\) \{.*?\n\s*\}', replace_fetch, rec_content, flags=re.DOTALL)

with open('templates/recommendation.html', 'w', encoding='utf-8') as f:
    f.write(rec_content)
print("Updated recommendation.html with sessionStorage.")

# 2. Update common.js checkoutCart
with open('static/js/common.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace the prompt line:
# const address = prompt("Please enter your delivery location/address:");
# if (!address) { ... }
old_checkout = """    const address = prompt("Please enter your delivery location/address:");
    if (!address) {
        alert("Checkout cancelled: Delivery location is required.");
        return;
    }"""

new_checkout = """    let address = sessionStorage.getItem('farmAddress');
    if (!address) {
        address = prompt("We couldn't detect your map location. Please enter your delivery address:");
        if (!address) {
            alert("Checkout cancelled: Delivery location is required.");
            return;
        }
    }"""

js_content = js_content.replace(old_checkout, new_checkout)

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated common.js checkoutCart.")
