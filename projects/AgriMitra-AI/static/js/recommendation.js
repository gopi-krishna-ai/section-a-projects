/* =============================================
   AGRIMITRA AI - COMPLETE RECOMMENDATION PAGE
   Crop model + Fertilizer model in one form.
   ============================================= */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("recForm");
    const submitBtn = document.getElementById("submitBtn");
    const errorBox = document.getElementById("errorBox");
    const resultArea = document.getElementById("resultArea");

    const cropChecks = [
        ["c_nitrogen", v => v >= 0, "Nitrogen cannot be negative."],
        ["c_phosphorus", v => v >= 0, "Phosphorus cannot be negative."],
        ["c_potassium", v => v >= 0, "Potassium cannot be negative."],
        ["c_temperature", v => v >= -10 && v <= 60, "Temperature should be between -10 and 60 °C."],
        ["c_humidity", v => v >= 0 && v <= 100, "Humidity should be between 0 and 100%."],
        ["c_ph", v => v >= 0 && v <= 14, "pH should be between 0 and 14."],
        ["c_rainfall", v => v >= 0, "Rainfall cannot be negative."]
    ];

    async function loadMeta() {
        try {
            const resp = await fetch("/api/fertilizer/meta");
            const data = await resp.json();
            if (!data.success) return;

            const soilSel = document.getElementById("f_soil_type");
            for (const s of data.soil_types) {
                const opt = document.createElement("option");
                opt.value = s;
                opt.textContent = s;
                soilSel.appendChild(opt);
            }

            const cropSel = document.getElementById("f_crop_type");
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

    function showError(message) {
        errorBox.innerHTML = "<i class='fa-solid fa-triangle-exclamation'></i> " + message;
        errorBox.classList.remove("hidden");
        resultArea.classList.add("hidden");
    }

    function validate() {
        for (const [id, test, message] of cropChecks) {
            const el = document.getElementById(id);
            const val = parseFloat(el.value);
            if (el.value === "" || isNaN(val) || !test(val)) {
                showError(message);
                el.focus();
                return false;
            }
        }

        if (!document.getElementById("f_soil_type").value) {
            showError("Please select a soil type.");
            return false;
        }

        const moisture = document.getElementById("f_moisture");
        const m = parseFloat(moisture.value);
        if (moisture.value === "" || isNaN(m) || m < 0 || m > 100) {
            showError("Soil moisture should be between 0 and 100%.");
            moisture.focus();
            return false;
        }
        return true;
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        errorBox.classList.add("hidden");

        if (!validate()) return;

        const payload = {
            nitrogen: document.getElementById("c_nitrogen").value,
            phosphorus: document.getElementById("c_phosphorus").value,
            potassium: document.getElementById("c_potassium").value,
            temperature: document.getElementById("c_temperature").value,
            humidity: document.getElementById("c_humidity").value,
            ph: document.getElementById("c_ph").value,
            rainfall: document.getElementById("c_rainfall").value,
            soil_type: document.getElementById("f_soil_type").value,
            crop_type: document.getElementById("f_crop_type").value,
            moisture: document.getElementById("f_moisture").value
        };

        submitBtn.disabled = true;
        submitBtn.classList.add("loading");
        submitBtn.querySelector("span").textContent =
            currentT ? currentT.loading : PAGE_STRINGS.loading;

        try {
            const resp = await fetch("/api/recommend", {
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

    const PAGE_STRINGS = {
        pageTitle: "Complete Recommendation",
        pageSubtitle: "One form - get both the recommended crop and a suitable fertilizer.",
        cropSectionTitle: "Soil & Weather Values (for crop model)",
        fertSectionTitle: "Soil & Crop Details (for fertilizer model)",
        lblNitrogen: "Nitrogen (N)",
        lblPhosphorus: "Phosphorus (P)",
        lblPotassium: "Potassium (K)",
        lblTemperature: "Temperature (°C)",
        lblHumidity: "Humidity (%)",
        lblPh: "Soil pH",
        lblRainfall: "Rainfall (mm)",
        lblSoilType: "Soil Type",
        lblCropType: "Crop Type",
        lblMoisture: "Soil Moisture (%)",
        optSoilPh: "Select soil type",
        optCropPh: "Select crop type",
        autoCropNote: "If the predicted crop matches a known crop type, it is used automatically for the fertilizer model.",
        button: "Get Complete Recommendation",
        loading: "Running both models...",
        cropResultTitle: "Recommended Crop",
        fertResultTitle: "Recommended Fertilizer",
        cropResultConf: "Crop model confidence",
        fertResultConf: "Fertilizer model confidence",
        guidanceTitle: "General Farming Guidance",
        guidanceText: "Prepare the field well before sowing, keep the soil moist but not waterlogged, and apply the recommended fertilizer according to the crop stage. Observe the crop regularly for pests and diseases. These are general guidelines - consult your local agriculture officer for crop-specific advice.",
        modelNote: "Results come from two separate Random Forest models (crop + fertilizer). They are model-based suggestions, not guarantees."
    };

    let lastCrop = "";
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

    function renderResult(data) {
        lastCrop = data.crop;
        lastFert = data.fertilizer;
        const lang = getSavedLanguage();
        Promise.all([
            ensureStrings(lang),
            NLP.translate([data.crop, data.fertilizer], lang)
        ]).then(function (results) {
            const t = results[0];
            const cropName = results[1][0];
            const fertName = results[1][1];
            document.getElementById("resultCrop").textContent = cropName;
            document.getElementById("resultCropConf").textContent =
                t.cropResultConf + ": " + Math.round(data.crop_confidence * 100) + "%";
            document.getElementById("resultFert").textContent = fertName;
            document.getElementById("resultFertConf").textContent =
                t.fertResultConf + ": " + Math.round(data.fertilizer_confidence * 100) + "%";

            document.getElementById("guidanceText").textContent = t.guidanceText;
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
            set("cropSectionTitle", t.cropSectionTitle);
            set("fertSectionTitle", t.fertSectionTitle);
            set("lblNitrogen", t.lblNitrogen);
            set("lblPhosphorus", t.lblPhosphorus);
            set("lblPotassium", t.lblPotassium);
            set("lblTemperature", t.lblTemperature);
            set("lblHumidity", t.lblHumidity);
            set("lblPh", t.lblPh);
            set("lblRainfall", t.lblRainfall);
            set("lblSoilType", t.lblSoilType);
            set("lblCropType", t.lblCropType);
            set("lblMoisture", t.lblMoisture);
            set("autoCropNote", t.autoCropNote);
            set("cropResultTitle", t.cropResultTitle);
            set("fertResultTitle", t.fertResultTitle);
            set("guidanceTitle", t.guidanceTitle);
            document.getElementById("optSoilPh").textContent = t.optSoilPh;
            document.getElementById("optCropPh").textContent = t.optCropPh;
            NLP.localizeOptions(lang, document.getElementById("f_soil_type"));
            NLP.localizeOptions(lang, document.getElementById("f_crop_type"));
            submitBtn.querySelector("span").textContent = t.button;
            const guidance = document.getElementById("guidanceText");
            if (!guidance.classList.contains("hidden")) guidance.textContent = t.guidanceText;
            const note = document.getElementById("modelNote");
            if (!note.classList.contains("hidden")) note.textContent = t.modelNote;
            if (lastCrop && lastFert) {
                return NLP.translate([lastCrop, lastFert], lang).then(function (out) {
                    document.getElementById("resultCrop").textContent = out[0];
                    document.getElementById("resultFert").textContent = out[1];
                    const cropConf = document.getElementById("resultCropConf");
                    const fertConf = document.getElementById("resultFertConf");
                    const cm = cropConf.textContent.match(/\d+%/);
                    const fm = fertConf.textContent.match(/\d+%/);
                    if (cm) cropConf.textContent = t.cropResultConf + ": " + cm[0];
                    if (fm) fertConf.textContent = t.fertResultConf + ": " + fm[0];
                });
            }
        });
    }

    document.addEventListener("agri:langchange", function (e) { applyPageLanguage(e.detail.lang); });

    loadMeta();

    applyPageLanguage(getSavedLanguage());
});
