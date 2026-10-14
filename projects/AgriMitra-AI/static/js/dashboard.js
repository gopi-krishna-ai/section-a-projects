// =====================================
// AGRIMITRA AI DASHBOARD
// =====================================

// ===============================
// LANGUAGE
// ===============================

const language = document.getElementById("language");

// Default language
let currentLanguage = "en";
let weatherLive = false;
let lastCondition = "Sunny";
let lastConditionTranslated = null;

// ===============================
// CHANGE LANGUAGE
// ===============================

language.addEventListener("change", function () {
    currentLanguage = this.value;
    changeLanguage(currentLanguage);
    if (typeof saveLanguage === "function") saveLanguage(currentLanguage);
});

// =====================================
// INITIAL LOAD
// =====================================

window.onload = function () {
    currentLanguage = (typeof getSavedLanguage === "function") ? getSavedLanguage() : "en";
    if (SUPPORTED.indexOf(currentLanguage) === -1) currentLanguage = "en";
    language.value = currentLanguage;

    updateGreeting();
    getLocation();
    rotateTips();
    rotateNews();
    changeLanguage(currentLanguage);

    // Feature card navigation
    document.querySelectorAll(".feature-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
            const nav = btn.getAttribute("data-nav");
            const pages = {
                crop: "/crop",
                soil: "/soil",
                fertilizer: "/fertilizer",
                recommendation: "/recommendation",
                assistant: "/assistant",
                history: "/history"
            };
            if (pages[nav]) window.location.href = pages[nav];
        });
    });
};

// =====================================
// GREETING
// =====================================

function updateGreeting() {
    const hour = new Date().getHours();
    const key = hour < 12 ? "greetingMorning" : (hour < 17 ? "greetingAfternoon" : "greetingEvening");
    NLP.translate([DASH_STRINGS[key]], language.value).then(function (out) {
        document.getElementById("welcome").innerHTML = out[0];
    });
}

// =====================================
// LIVE LOCATION & MAP
// =====================================

let map;
let marker;

function initMap(lat, lon, zoom) {
    if (!map) {
        map = L.map('map').setView([lat, lon], zoom);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        marker = L.marker([lat, lon]).addTo(map);

        map.on('click', function(e) {
            updateLocation(e.latlng.lat, e.latlng.lng);
        });

        document.getElementById('citySearchBtn').addEventListener('click', function() {
            const query = document.getElementById('citySearchInput').value;
            if (query) {
                fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data && data.length > 0) {
                            updateLocation(data[0].lat, data[0].lon);
                        } else {
                            alert("Location not found!");
                        }
                    });
            }
        });
    } else {
        map.setView([lat, lon], zoom);
        marker.setLatLng([lat, lon]);
    }
}

function updateLocation(lat, lon) {
    initMap(lat, lon, 10);
    // Reverse Geocoding
    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            const city = data.address.city || data.address.town || data.address.village || "";
            const district = data.address.county || "";
            const state = data.address.state || "";
            document.getElementById("location").innerHTML = `<i class="fa-solid fa-location-dot"></i> ${city}, ${district}, ${state}`;
        })
        .catch(() => {
            document.getElementById("location").innerHTML = `<i class="fa-solid fa-location-dot"></i> ${parseFloat(lat).toFixed(2)}, ${parseFloat(lon).toFixed(2)}`;
        });

    getWeather(lat, lon);
}

function getLocation() {
    // Default to a central India location before getting user's position
    initMap(20.5937, 78.9629, 5);

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        document.getElementById("location").innerHTML = "Location not supported.";
        updateLocation(20.5937, 78.9629); // Default India
    }
}

function showPosition(position) {
    updateLocation(position.coords.latitude, position.coords.longitude);
}

function showError() {
    document.getElementById("location").innerHTML = "📍 Location permission denied. Using default.";
    updateLocation(20.5937, 78.9629); // Default India
}

// =====================================
// LIVE WEATHER (server-side proxy)
// =====================================

function getWeather(lat, lon) {
    fetch(`/api/weather?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            const lang = language.value;
            lastCondition = data.condition || lastCondition;
            document.getElementById("temperature").innerHTML = Math.round(data.temperature) + "&deg;C";
            document.getElementById("humidity").innerHTML = data.humidity + "%";
            document.getElementById("wind").innerHTML = data.wind + " km/h";
            document.getElementById("rain").innerHTML = data.rain + " mm";
            document.getElementById("uv").innerHTML = data.uv;
            document.getElementById("pressure").innerHTML = data.pressure + " mb";
            document.getElementById("visibility").innerHTML = data.visibility + " km";
            document.getElementById("feelsLike").innerHTML = Math.round(data.feels_like) + "&deg;C";
            document.getElementById("updated").innerHTML = data.updated;
            
            // Check if icon is our custom real image
            if (data.icon && data.icon.startsWith("/static")) {
                document.getElementById("weatherIcon").src = data.icon;
            } else {
                document.getElementById("weatherIcon").src = "https:" + data.icon;
            }
            
            weatherLive = data.live;
            NLP.translate([lastCondition, DASH_STRINGS.weatherStatus, DASH_STRINGS.demo], lang)
                .then(function (out) {
                    lastConditionTranslated = out[0];
                    document.getElementById("condition").innerHTML = out[0];
                    document.getElementById("weatherStatus").textContent = data.live ? out[1] : out[2];
                });
            generateAdvice(data);
        })
        .catch(error => {
            console.error(error);
            loadDemoWeather();
        });
}

// =========================================
// TRANSLATIONS (dashboard page strings)
// =========================================

const DASH_STRINGS = {
    heroTitle: "Welcome to AgriMitra AI",
    heroDesc: "Smart farming starts with smart decisions.",
    weatherTitle: "🌦 Today's Weather",
    weatherStatus: "Live Weather",
    feelsLikeText: "Feels Like",
    humidityText: "Humidity",
    rainText: "Rain",
    windText: "Wind Speed",
    uvText: "UV Index",
    visibilityText: "Visibility",
    pressureText: "Pressure",
    updatedText: "Updated",
    tipTitle: "💡 Farming Tip",
    newsTitle: "📰 Agriculture News",
    adviceTitle: "🤖 Farming Advice for Today",
    cropTitle: "Crop Recommendation",
    cropDesc: "Get AI based crop suggestions.",
    soilTitle: "Soil Analysis",
    soilDesc: "Check soil nutrients and health.",
    fertTitle: "Fertilizer Recommendation",
    fertDesc: "Find the best fertilizer.",
    combTitle: "Complete Recommendation",
    combDesc: "Crop + fertilizer in one form.",
    chatTitle: "AI Assistant",
    chatDesc: "Ask farming questions anytime.",
    historyTitle: "History",
    historyDesc: "View previous recommendations.",
    greetingMorning: "👋 Good Morning Farmer!",
    greetingAfternoon: "☀️ Good Afternoon Farmer!",
    greetingEvening: "🌙 Good Evening Farmer!",
    demo: "Demo Data",
    cropOpen: "Open",
    soilOpen: "Open",
    fertOpen: "Open",
    combOpen: "Open",
    chatOpen: "Chat",
    historyOpen: "View",
    statCrops: "Crops",
    statSoilTypes: "Soil Types",
    statFertilizers: "Fertilizers",
    statModels: "ML Models"
};

const DASH_TIPS = [
    "Healthy soil grows healthy crops.",
    "Water crops early morning or evening.",
    "Use organic compost whenever possible.",
    "Test your soil before adding fertilizers.",
    "Rotate crops to maintain soil fertility.",
    "Monitor weather before irrigation."
];

const DASH_NEWS = [
    "Government launches new irrigation scheme.",
    "Rain expected in Northern Karnataka.",
    "Organic farming subsidy increased."
];

let currentTips = DASH_TIPS;
let currentNews = DASH_NEWS;

// =========================================
// LANGUAGE CHANGE (NLP engine)
// =========================================

function changeLanguage(lang) {
    const texts = Object.keys(DASH_STRINGS).map(function (k) { return DASH_STRINGS[k]; })
        .concat(DASH_TIPS, DASH_NEWS);
    const count = Object.keys(DASH_STRINGS).length;

    return NLP.translate(texts, lang).then(function (out) {
        const t = {};
        Object.keys(DASH_STRINGS).forEach(function (k, i) { t[k] = out[i]; });
        currentTips = out.slice(count, count + DASH_TIPS.length);
        currentNews = out.slice(count + DASH_TIPS.length);

        document.getElementById("heroTitle").innerHTML = t.heroTitle;
        document.getElementById("heroDesc").innerHTML = t.heroDesc;

        document.getElementById("weatherTitle").innerHTML = t.weatherTitle;
        document.getElementById("weatherStatus").textContent =
            weatherLive ? t.weatherStatus : t.demo;
        document.getElementById("condition").innerHTML = lastConditionTranslated || "Sunny";

        document.getElementById("feelsLikeText").innerHTML = t.feelsLikeText;
        document.getElementById("humidityText").innerHTML = t.humidityText;
        document.getElementById("rainText").innerHTML = t.rainText;
        document.getElementById("windText").innerHTML = t.windText;
        document.getElementById("uvText").innerHTML = t.uvText;
        document.getElementById("visibilityText").innerHTML = t.visibilityText;
        document.getElementById("pressureText").innerHTML = t.pressureText;
        document.getElementById("updatedText").innerHTML = t.updatedText;

        document.getElementById("tipTitle").innerHTML = t.tipTitle;
        document.getElementById("newsTitle").innerHTML = t.newsTitle;
        document.getElementById("adviceTitle").innerHTML = t.adviceTitle;

        document.getElementById("cropTitle").innerHTML = t.cropTitle;
        document.getElementById("cropDesc").innerHTML = t.cropDesc;
        document.getElementById("soilTitle").innerHTML = t.soilTitle;
        document.getElementById("soilDesc").innerHTML = t.soilDesc;
    document.getElementById("fertTitle").innerHTML = t.fertTitle;
    document.getElementById("fertDesc").innerHTML = t.fertDesc;
    document.getElementById("combTitle").innerHTML = t.combTitle;
    document.getElementById("combDesc").innerHTML = t.combDesc;
    document.getElementById("chatTitle").innerHTML = t.chatTitle;
    document.getElementById("chatDesc").innerHTML = t.chatDesc;
    document.getElementById("historyTitle").innerHTML = t.historyTitle;
    document.getElementById("historyDesc").innerHTML = t.historyDesc;

    // Quick stats labels
    document.getElementById("statCrops").innerHTML = t.statCrops;
    document.getElementById("statSoilTypes").innerHTML = t.statSoilTypes;
    document.getElementById("statFertilizers").innerHTML = t.statFertilizers;
    document.getElementById("statModels").innerHTML = t.statModels;

    // Feature card button labels
    const btnLabels = {
        crop: t.cropOpen,
        soil: t.soilOpen,
        fertilizer: t.fertOpen,
        recommendation: t.combOpen,
        assistant: t.chatOpen,
        history: t.historyOpen
    };
    document.querySelectorAll(".feature-btn").forEach(function (btn) {
        const nav = btn.getAttribute("data-nav");
        if (btnLabels[nav]) btn.textContent = btnLabels[nav];
    });

    // Translate tips/news immediately
        document.getElementById("tipText").innerHTML = currentTips[0];
        document.getElementById("news1").innerHTML = currentNews[0];
        document.getElementById("news2").innerHTML = currentNews[1];
        document.getElementById("news3").innerHTML = currentNews[2];
    });
}

// =========================================
// TIPS ROTATION (translated arrays)
// =========================================

let tipIndex = 0;

function rotateTips() {
    setInterval(function () {
        document.getElementById("tipText").innerHTML = currentTips[tipIndex];
        tipIndex++;
        if (tipIndex >= currentTips.length) tipIndex = 0;
    }, 8000);
}

// =========================================
// AGRICULTURE NEWS ROTATION
// =========================================

function rotateNews() {
    setInterval(function () {
        document.getElementById("news1").innerHTML = currentNews[0];
        document.getElementById("news2").innerHTML = currentNews[1];
        document.getElementById("news3").innerHTML = currentNews[2];
    }, 12000);
}

// =========================================
// WEATHER-BASED ADVICE
// (rule-based guidance from live weather data)
// =========================================

function generateAdvice(weatherData) {
    let advice = "";
    const temp = weatherData.temperature;
    const humidity = weatherData.humidity;
    const rain = weatherData.rain;
    const wind = weatherData.wind;

    const advices = [];

    // Rain advice
    if (rain > 15) {
        advices.push("🌧 Heavy rainfall detected. Delay all fertilizer application to prevent runoff. Ensure field drainage is clear.");
    } else if (rain > 5) {
        advices.push("🌧 Moderate rain expected. Good natural irrigation, hold off on manual watering.");
    } else if (rain > 0) {
        advices.push("🌦 Light drizzle expected. May increase humidity, monitor for pests.");
    }

    // Temp advice
    if (temp > 38) {
        advices.push("🔥 Extreme heat! Provide deep irrigation early in the morning and consider shade nets for sensitive crops.");
    } else if (temp > 32) {
        advices.push("☀ High temperatures. Irrigate crops during early morning or evening to minimize evaporation.");
    } else if (temp < 10) {
        advices.push("❄ Very low temperatures. Watch out for frost damage on sensitive plants. Light irrigation can sometimes help prevent frost settling.");
    }

    // Humidity advice
    if (humidity > 85) {
        advices.push("🍃 High humidity detected. This creates ideal conditions for fungal diseases like powdery mildew; consider preventive organic sprays.");
    } else if (humidity < 30) {
        advices.push("🌵 Low humidity and dry air. Crops will lose water faster, ensure adequate soil moisture is maintained.");
    }

    // Wind advice
    if (wind > 35) {
        advices.push("🌪 Strong winds warning! Delay any pesticide spraying as it will drift. Secure tall plants and structures.");
    } else if (wind > 20) {
        advices.push("🌬 Breezy conditions. Be careful if applying foliar sprays.");
    }

    if (advices.length === 0) {
        advices.push("🌱 Weather conditions are highly favorable for most farming activities! Good time for sowing, weeding, or regular maintenance.");
    }

    advice = advices.join(" <br><br> ");

    NLP.translate([advice], language.value).then(function (out) {
        document.getElementById("adviceText").innerHTML = out[0];
    });
}
// =========================================
// DEMO WEATHER FALLB&deg;CK
// (used if the weather API is unavailable)
// =========================================

function loadDemoWeather() {
    lastCondition = "Sunny";
    document.getElementById("temperature").innerHTML = "29&deg;C";
    document.getElementById("humidity").innerHTML = "68%";
    document.getElementById("wind").innerHTML = "12 km/h";
    document.getElementById("rain").innerHTML = "0 mm";
    document.getElementById("uv").innerHTML = "6";
    document.getElementById("pressure").innerHTML = "1012 mb";
    document.getElementById("visibility").innerHTML = "10 km";
    document.getElementById("feelsLike").innerHTML = "31&deg;C";
    document.getElementById("updated").innerHTML = new Date().toLocaleTimeString();
    weatherLive = false;
    NLP.translate([lastCondition, DASH_STRINGS.demo], language.value).then(function (out) {
        lastConditionTranslated = out[0];
        document.getElementById("condition").innerHTML = out[0];
        document.getElementById("weatherStatus").textContent = out[1];
    });
    generateAdvice({ temperature: 29, humidity: 68, rain: 0, wind: 12 });
}

// =========================================
// AUTO REFRESH GREETING
// =========================================

setInterval(updateGreeting, 60000);

// =========================================
// END OF FILE
// =========================================
