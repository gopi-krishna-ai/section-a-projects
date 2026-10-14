/* =============================================
   AGRIMITRA AI - CROP RECOMMENDATION PAGE
   ============================================= */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("cropForm");
    const submitBtn = document.getElementById("submitBtn");
    const errorBox = document.getElementById("errorBox");
    const resultArea = document.getElementById("resultArea");

    const PAGE_STRINGS = {
        pageTitle: "Crop Recommendation",
        pageSubtitle: "Enter your soil and weather values to get a machine-learning crop suggestion.",
        formTitle: "Soil & Weather Values",
        lblNitrogen: "Nitrogen (N)",
        lblPhosphorus: "Phosphorus (P)",
        lblPotassium: "Potassium (K)",
        lblTemperature: "Temperature (°C)",
        lblHumidity: "Humidity (%)",
        lblPh: "Soil pH",
        lblRainfall: "Rainfall (mm)",
        button: "Get Crop Recommendation",
        loading: "Analyzing your soil data...",
        resultTitle: "Recommended Crop",
        resultConf: "Model confidence",
        summaryTitle: "Your Input Summary",
        modelNote: "This suggestion comes from a Random Forest model trained on the Crop Recommendation dataset (22 crops). It is a model-based suggestion, not a guarantee. Verify with your local agriculture officer."
    };

    const labels = {
        nitrogen: PAGE_STRINGS.lblNitrogen,
        phosphorus: PAGE_STRINGS.lblPhosphorus,
        potassium: PAGE_STRINGS.lblPotassium,
        temperature: PAGE_STRINGS.lblTemperature,
        humidity: PAGE_STRINGS.lblHumidity,
        ph: PAGE_STRINGS.lblPh,
        rainfall: PAGE_STRINGS.lblRainfall
    };

    // The model returns dataset column names (Nitrogen, pH_Value, ...).
    // Map them to the label keys used above so the summary stays translated.
    const LABEL_KEY_MAP = {
        Nitrogen: "nitrogen",
        Phosphorus: "phosphorus",
        Potassium: "potassium",
        Temperature: "temperature",
        Humidity: "humidity",
        pH_Value: "ph",
        Rainfall: "rainfall"
    };

    let lastCrop = "";
    let currentT = null;

    function ensureStrings(lang) {
        return NLP.translate(Object.keys(PAGE_STRINGS).map(function (k) { return PAGE_STRINGS[k]; }), lang)
            .then(function (out) {
                const t = {};
                Object.keys(PAGE_STRINGS).forEach(function (k, i) { t[k] = out[i]; });
                currentT = t;
                return t;
            });
    }

    function validate() {
        const checks = [
            ["nitrogen", v => v >= 0, "Nitrogen cannot be negative."],
            ["phosphorus", v => v >= 0, "Phosphorus cannot be negative."],
            ["potassium", v => v >= 0, "Potassium cannot be negative."],
            ["temperature", v => v >= -10 && v <= 60, "Temperature should be between -10 and 60 °C."],
            ["humidity", v => v >= 0 && v <= 100, "Humidity should be between 0 and 100%."],
            ["ph", v => v >= 0 && v <= 14, "pH should be between 0 and 14."],
            ["rainfall", v => v >= 0, "Rainfall cannot be negative."]
        ];

        for (const [id, test, message] of checks) {
            const el = document.getElementById(id);
            const val = parseFloat(el.value);
            if (el.value === "" || isNaN(val) || !test(val)) {
                showError(message);
                el.focus();
                return false;
            }
        }
        return true;
    }

    function showError(message) {
        errorBox.innerHTML = "<i class='fa-solid fa-triangle-exclamation'></i> " + message;
        errorBox.classList.remove("hidden");
        resultArea.classList.add("hidden");
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        errorBox.classList.add("hidden");

        if (!validate()) return;

        const payload = {
            nitrogen: document.getElementById("nitrogen").value,
            phosphorus: document.getElementById("phosphorus").value,
            potassium: document.getElementById("potassium").value,
            temperature: document.getElementById("temperature").value,
            humidity: document.getElementById("humidity").value,
            ph: document.getElementById("ph").value,
            rainfall: document.getElementById("rainfall").value
        };

        submitBtn.disabled = true;
        submitBtn.classList.add("loading");
        submitBtn.querySelector("span").textContent =
            currentT ? currentT.loading : PAGE_STRINGS.loading;

        try {
            const resp = await fetch("/api/crop", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();

            if (!data.success) {
                showError(data.message || "Prediction failed. Please try again.");
                return;
            }

            renderResult(data);
        } catch (err) {
            console.error(err);
            showError("Unable to connect to the server. Please try again.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.classList.remove("loading");
            submitBtn.querySelector("span").textContent =
                currentT ? currentT.button : PAGE_STRINGS.button;
        }
    });

    function renderResult(data) {
        lastCrop = data.crop;
        const lang = getSavedLanguage();
        Promise.all([ensureStrings(lang), NLP.translate([data.crop], lang)])
            .then(function (results) {
                const t = results[0];
                const cropName = results[1][0];
                document.getElementById("resultCrop").textContent = cropName;
                
                
                // Inject new dynamic multi-seller E-cart
                const ecartSection = document.getElementById("ecartSection");
                if (ecartSection) {
                    ecartSection.outerHTML = generateEcartHTML(cropName, 'seed');
                } else {
                    // In case it was already replaced, we can append it or find the new one.
                    // Actually, if it's replaced, its ID is gone. We need a stable container.
                    let container = document.getElementById("ecartContainer");
                    if (!container) {
                        container = document.createElement("div");
                        container.id = "ecartContainer";
                        document.querySelector(".result-card").appendChild(container);
                    }
                    container.innerHTML = generateEcartHTML(cropName, 'seed');
                }


                document.getElementById("resultConf").textContent =
                    t.resultConf + ": " + Math.round(data.confidence * 100) + "%";

                const grid = document.getElementById("summaryGrid");
                grid.innerHTML = "";
                for (const [key, value] of Object.entries(data.input_features)) {
                    const item = document.createElement("div");
                    item.className = "summary-item";
                    const label = document.createElement("span");
                    const labelKey = LABEL_KEY_MAP[key] || key;
                    label.textContent = labels[labelKey] || key;
                    const val = document.createElement("strong");
                    val.textContent = Number(value).toFixed(2);
                    item.appendChild(label);
                    item.appendChild(val);
                    grid.appendChild(item);
                }

                document.getElementById("modelNote").textContent = t.modelNote;

                resultArea.classList.remove("hidden");
                resultArea.scrollIntoView({ behavior: "smooth" });
            });
    }

    /* ---- translations for this page (NLP engine) ---- */
    function applyPageLanguage(lang) {
        return ensureStrings(lang).then(function (t) {
            const set = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
            set("pageTitle", t.pageTitle);
            set("pageSubtitle", t.pageSubtitle);
            set("formTitle", t.formTitle);
            set("lblNitrogen", t.lblNitrogen);
            set("lblPhosphorus", t.lblPhosphorus);
            set("lblPotassium", t.lblPotassium);
            set("lblTemperature", t.lblTemperature);
            set("lblHumidity", t.lblHumidity);
            set("lblPh", t.lblPh);
            set("lblRainfall", t.lblRainfall);
            set("resultTitle", t.resultTitle);
            set("summaryTitle", t.summaryTitle);

            labels.nitrogen = t.lblNitrogen;
            labels.phosphorus = t.lblPhosphorus;
            labels.potassium = t.lblPotassium;
            labels.temperature = t.lblTemperature;
            labels.humidity = t.lblHumidity;
            labels.ph = t.lblPh;
            labels.rainfall = t.lblRainfall;

            const btn = document.getElementById("submitBtn");
            btn.querySelector("span").textContent = t.button;
            const note = document.getElementById("modelNote");
            if (!note.classList.contains("hidden")) note.textContent = t.modelNote;

            const confEl = document.getElementById("resultConf");
            const confMatch = confEl.textContent.match(/\d+%/);
            if (confMatch) confEl.textContent = t.resultConf + ": " + confMatch[0];

            if (lastCrop) {
                return NLP.translate([lastCrop], lang).then(function (out) {
                    document.getElementById("resultCrop").textContent = out[0];
                });
            }
        });
    }

    document.addEventListener("agri:langchange", function (e) { applyPageLanguage(e.detail.lang); });

    applyPageLanguage(getSavedLanguage());
});
