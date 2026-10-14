/* =============================================
   AGRIMITRA AI - SOIL ANALYSIS PAGE
   Rule-based nutrient check (not a lab test).
   ============================================= */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("soilForm");
    const errorBox = document.getElementById("errorBox");
    const resultArea = document.getElementById("resultArea");

    /* Common low/medium/high thresholds for nutrient levels (mg/kg range) */
    function level(value, low, high) {
        if (value < low) return 0;      // low
        if (value <= high) return 1;    // medium
        return 2;                       // high
    }

    function validate() {
        const checks = [
            ["nitrogen", v => v >= 0, "Nitrogen cannot be negative."],
            ["phosphorus", v => v >= 0, "Phosphorus cannot be negative."],
            ["potassium", v => v >= 0, "Potassium cannot be negative."],
            ["ph", v => v >= 0 && v <= 14, "pH should be between 0 and 14."]
        ];
        for (const [id, test, message] of checks) {
            const el = document.getElementById(id);
            const val = parseFloat(el.value);
            if (el.value === "" || isNaN(val) || !test(val)) {
                errorBox.innerHTML = "<i class='fa-solid fa-triangle-exclamation'></i> " + message;
                errorBox.classList.remove("hidden");
                resultArea.classList.add("hidden");
                el.focus();
                return false;
            }
        }
        return true;
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        errorBox.classList.add("hidden");
        if (!validate()) return;

        const n = parseFloat(document.getElementById("nitrogen").value);
        const p = parseFloat(document.getElementById("phosphorus").value);
        const k = parseFloat(document.getElementById("potassium").value);
        const ph = parseFloat(document.getElementById("ph").value);

        renderResult(n, p, k, ph);
    });

    function renderResult(n, p, k, ph) {
        const lang = getSavedLanguage();

        const levels = [
            { key: "n", name: PAGE_STRINGS.lblNitrogen, value: n, lv: level(n, 80, 120) },
            { key: "p", name: PAGE_STRINGS.lblPhosphorus, value: p, lv: level(p, 20, 40) },
            { key: "k", name: PAGE_STRINGS.lblPotassium, value: k, lv: level(k, 100, 160) }
        ];

        const adviceKeys = {
            0: { n: "adviceLowN", p: "adviceLowP", k: "adviceLowK" },
            1: { n: "adviceMedN", p: "adviceMedP", k: "adviceMedK" },
            2: { n: "adviceHighN", p: "adviceHighP", k: "adviceHighK" }
        };

        const texts = [
            PAGE_STRINGS.levelLow, PAGE_STRINGS.levelMedium, PAGE_STRINGS.levelHigh,
            PAGE_STRINGS.phNote, PAGE_STRINGS.phAcidic, PAGE_STRINGS.phNeutral, PAGE_STRINGS.phAlkaline
        ];
        levels.forEach(function (item) {
            texts.push(PAGE_STRINGS[adviceKeys[item.lv][item.key]]);
        });

        NLP.translate(texts, lang).then(function (out) {
            const levelText = [out[0], out[1], out[2]];
            const phNote = out[3];
            const phTexts = { phAcidic: out[4], phNeutral: out[5], phAlkaline: out[6] };
            const adviceTexts = out.slice(7);

            const grid = document.getElementById("resultGrid");
            grid.innerHTML = "";
            levels.forEach(function (item) {
                const box = document.createElement("div");
                box.className = "summary-item";
                const span = document.createElement("span");
                span.textContent = item.name;
                const strong = document.createElement("strong");
                strong.textContent = item.value.toFixed(1) + " - " + levelText[item.lv];
                box.appendChild(span);
                box.appendChild(strong);
                grid.appendChild(box);
            });

            const advice = document.getElementById("adviceList");
            advice.innerHTML = "";

            levels.forEach(function (item, i) {
                const li = document.createElement("li");
                li.textContent = adviceTexts[i];
                if (li.textContent) advice.appendChild(li);
            });

            const phLi = document.createElement("li");
            let phText = phTexts.phNeutral;
            if (ph < 6.0) phText = phTexts.phAcidic;
            else if (ph > 7.5) phText = phTexts.phAlkaline;
            phLi.textContent = phNote + ph.toFixed(2) + " - " + phText;
            advice.appendChild(phLi);

            resultArea.classList.remove("hidden");
            resultArea.scrollIntoView({ behavior: "smooth" });
        });
    }

    const PAGE_STRINGS = {
        pageTitle: "Soil Analysis",
        pageSubtitle: "Simple nutrient check based on the values you enter. For a lab-level report, do a proper soil test.",
        formTitle: "Soil Nutrients",
        lblNitrogen: "Nitrogen (N)",
        lblPhosphorus: "Phosphorus (P)",
        lblPotassium: "Potassium (K)",
        lblPh: "Soil pH",
        button: "Analyze Soil",
        resultTitle: "Soil Nutrient Status",
        levelLow: "Low",
        levelMedium: "Medium",
        levelHigh: "High",
        adviceTitle: "Simple Advice",
        adviceLowN: "Nitrogen is low. Add organic compost or a nitrogen-rich fertilizer (like urea) in small doses.",
        adviceMedN: "Nitrogen is at a medium level. Maintain it with compost or light fertilizer application.",
        adviceHighN: "Nitrogen is high. Avoid extra nitrogen fertilizers this season.",
        adviceLowP: "Phosphorus is low. Add DAP or bone meal before sowing.",
        adviceMedP: "Phosphorus is medium. A small dose at sowing time is enough.",
        adviceHighP: "Phosphorus is high. Avoid phosphorus fertilizers this season.",
        adviceLowK: "Potassium is low. Add potash or wood ash in small amounts.",
        adviceMedK: "Potassium is medium. Maintain with potash at the growth stage.",
        adviceHighK: "Potassium is high. Avoid potassium fertilizers this season.",
        phNote: "pH value: ",
        phAcidic: "Soil is acidic (pH below 6.0). Add lime to raise the pH gradually.",
        phNeutral: "Soil pH is near neutral (6.0 - 7.5), which suits most crops.",
        phAlkaline: "Soil is alkaline (pH above 7.5). Add organic matter to improve the soil.",
        noteText: "This is a simple rule-based check, not a laboratory test."
    };

    function applyPageLanguage(lang) {
        return NLP.applyTo(lang, PAGE_STRINGS).then(function () {
            return NLP.translate([PAGE_STRINGS.button], lang).then(function (out) {
                document.getElementById("submitBtn").querySelector("span").textContent = out[0];
            });
        });
    }

    document.addEventListener("agri:langchange", function (e) { applyPageLanguage(e.detail.lang); });
    applyPageLanguage(getSavedLanguage());
});
