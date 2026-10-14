/* =============================================
   AGRIMITRA AI - FERTILIZER RECOMMENDATION PAGE
   ============================================= */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("fertForm");
    const submitBtn = document.getElementById("submitBtn");
    const errorBox = document.getElementById("errorBox");
    const resultArea = document.getElementById("resultArea");

    const MEANINGS = {
        "Urea": "Urea - a nitrogen-rich fertilizer that boosts leaf and stem growth.",
        "DAP": "DAP (Di-Ammonium Phosphate) - supplies nitrogen and phosphorus for root and early growth.",
        "28-28": "28-28 - a balanced fertilizer with equal nitrogen and phosphorus.",
        "14-35-14": "14-35-14 - phosphorus-rich fertilizer for flowering and fruiting.",
        "20-20": "20-20 - a balanced fertilizer for general crop growth.",
        "17-17-17": "17-17-17 - a balanced compound fertilizer for all-purpose use.",
        "10-26-26": "10-26-26 - potassium-rich fertilizer for crop strength and quality."
    };

    const PAGE_STRINGS = {
        pageTitle: "Fertilizer Recommendation",
        pageSubtitle: "Enter your soil test and crop details to find a suitable fertilizer.",
        formTitle: "Soil & Crop Details",
        lblSoilType: "Soil Type",
        lblCropType: "Crop Type",
        lblMoisture: "Soil Moisture (%)",
        lblTemperature: "Temperature (°C)",
        lblHumidity: "Humidity (%)",
        lblNitrogen: "Nitrogen (N)",
        lblPhosphorous: "Phosphorous (P)",
        lblPotassium: "Potassium (K)",
        optSoilPh: "Select soil type",
        optCropPh: "Select crop type",
        button: "Get Fertilizer Recommendation",
        loading: "Analyzing your soil data...",
        resultTitle: "Recommended Fertilizer",
        meaningTitle: "What this fertilizer means",
        resultConf: "Model confidence",
        modelNote: "This suggestion comes from a Random Forest model trained on the Fertilizer Prediction dataset. It is a model-based suggestion, not a guarantee. Adjust dosage as per soil test and crop stage."
    };

    let lastFert = "";
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

    /* Load the categorical values from the trained model */
    async function loadMeta() {
        try {
            const resp = await fetch("/api/fertilizer/meta");
            const data = await resp.json();
            if (!data.success) return;

            const soilSel = document.getElementById("soil_type");
            for (const s of data.soil_types) {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                soilSel.appendChild(opt);
            }

            const cropSel = document.getElementById("crop_type");
            for (const c of data.crop_types) {
                const opt = document.createElement("option");
                opt.value = c;
                opt.textContent = c;
                cropSel.appendChild(opt);
            }

            if (getSavedLanguage() !== "en") {
                NLP.localizeOptions(getSavedLanguage(), soilSel);
                NLP.localizeOptions(getSavedLanguage(), cropSel);
            }
        } catch (err) {
            console.error("Failed to load model meta:", err);
        }
    }

    function validate() {
        if (!document.getElementById("soil_type").value) {
            showError("Please select a soil type.");
            return false;
        }
        if (!document.getElementById("crop_type").value) {
            showError("Please select a crop type.");
            return false;
        }

        const checks = [
            ["temperature", v => v >= -10 && v <= 60, "Temperature should be between -10 and 60 °C."],
            ["humidity", v => v >= 0 && v <= 100, "Humidity should be between 0 and 100%."],
            ["moisture", v => v >= 0 && v <= 100, "Moisture should be between 0 and 100%."],
            ["nitrogen", v => v >= 0, "Nitrogen cannot be negative."],
            ["phosphorous", v => v >= 0, "Phosphorous cannot be negative."],
            ["potassium", v => v >= 0, "Potassium cannot be negative."]
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
            soil_type: document.getElementById("soil_type").value,
            crop_type: document.getElementById("crop_type").value,
            temperature: document.getElementById("temperature").value,
            humidity: document.getElementById("humidity").value,
            moisture: document.getElementById("moisture").value,
            nitrogen: document.getElementById("nitrogen").value,
            phosphorous: document.getElementById("phosphorous").value,
            potassium: document.getElementById("potassium").value
        };

        submitBtn.disabled = true;
        submitBtn.classList.add("loading");
        submitBtn.querySelector("span").textContent =
            currentT ? currentT.loading : PAGE_STRINGS.loading;

        try {
            const resp = await fetch("/api/fertilizer", {
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
        lastFert = data.fertilizer;
        const lang = getSavedLanguage();
        Promise.all([
            ensureStrings(lang),
            NLP.translate([data.fertilizer, MEANINGS[data.fertilizer] || data.fertilizer], lang)
        ]).then(function (results) {
            const t = results[0];
            const fertName = results[1][0];
            const meaning = results[1][1];
            document.getElementById("resultFert").textContent = fertName;
                
                
                // Inject new dynamic multi-seller E-cart
                const ecartSection = document.getElementById("ecartSection");
                if (ecartSection) {
                    ecartSection.outerHTML = generateEcartHTML(fertName, 'fertilizer');
                } else {
                    let container = document.getElementById("ecartContainer");
                    if (!container) {
                        container = document.createElement("div");
                        container.id = "ecartContainer";
                        document.querySelector(".result-card").appendChild(container);
                    }
                    container.innerHTML = generateEcartHTML(fertName, 'fertilizer');
                }


            document.getElementById("resultConf").textContent =
                t.resultConf + ": " + Math.round(data.confidence * 100) + "%";
            document.getElementById("meaningText").textContent = meaning;
            document.getElementById("modelNote").textContent = t.modelNote;
            resultArea.classList.remove("hidden");
            resultArea.scrollIntoView({ behavior: "smooth" });
        });
    }

    function applyPageLanguage(lang) {
        return ensureStrings(lang).then(function (t) {
            const set = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
            set("pageTitle", t.pageTitle);
            set("pageSubtitle", t.pageSubtitle);
            set("formTitle", t.formTitle);
            set("lblSoilType", t.lblSoilType);
            set("lblCropType", t.lblCropType);
            set("lblTemperature", t.lblTemperature);
            set("lblHumidity", t.lblHumidity);
            set("lblMoisture", t.lblMoisture);
            set("lblNitrogen", t.lblNitrogen);
            set("lblPhosphorous", t.lblPhosphorous);
            set("lblPotassium", t.lblPotassium);
            set("resultTitle", t.resultTitle);
            set("meaningTitle", t.meaningTitle);
            document.getElementById("optSoilPh").textContent = t.optSoilPh;
            document.getElementById("optCropPh").textContent = t.optCropPh;
            NLP.localizeOptions(lang, document.getElementById("soil_type"));
            NLP.localizeOptions(lang, document.getElementById("crop_type"));
            submitBtn.querySelector("span").textContent = t.button;
            const note = document.getElementById("modelNote");
            if (!note.classList.contains("hidden")) note.textContent = t.modelNote;
            if (lastFert) {
                return NLP.translate([lastFert, MEANINGS[lastFert] || lastFert], lang)
                    .then(function (out) {
                        document.getElementById("resultFert").textContent = out[0];
                        document.getElementById("meaningText").textContent = out[1];
                        const confEl = document.getElementById("resultConf");
                        const confMatch = confEl.textContent.match(/\d+%/);
                        if (confMatch) confEl.textContent = t.resultConf + ": " + confMatch[0];
                    });
            }
        });
    }

    document.addEventListener("agri:langchange", function (e) { applyPageLanguage(e.detail.lang); });

    loadMeta();

    applyPageLanguage(getSavedLanguage());
});
