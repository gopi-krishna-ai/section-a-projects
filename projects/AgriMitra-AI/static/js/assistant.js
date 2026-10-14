/* =============================================
   AGRIMITRA AI - AI ASSISTANT PAGE
   Text chat + voice input (Web Speech API)
   + speech output (SpeechSynthesis)
   ============================================= */

document.addEventListener("DOMContentLoaded", function () {

    const chatBox = document.getElementById("chatBox");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const micBtn = document.getElementById("micBtn");
    const speakBtn = document.getElementById("speakBtn");
    const clearBtn = document.getElementById("clearBtn");

    const VOICE_LANGS = {
        en: "en-IN", kn: "kn-IN", hi: "hi-IN", te: "te-IN", ta: "ta-IN"
    };

    let currentLang = (typeof getSavedLanguage === "function") ? getSavedLanguage() : "en";
    let recognition = null;
    let listening = false;
    let lastBotText = "";
    let busy = false;

    /* ---------- chat helpers ---------- */

    function addMessage(text, who) {
        const div = document.createElement("div");
        div.className = "msg " + who;
        div.textContent = text;
        const time = document.createElement("span");
        time.className = "msg-time";
        time.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        div.appendChild(time);
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
        if (who === "bot") lastBotText = text;
        return div;
    }

    function addTypingMessage() {
        const div = document.createElement("div");
        div.className = "msg bot typing";
        div.setAttribute("role", "status");
        div.innerHTML = '<span class="typing-dots" aria-hidden="true"><i></i><i></i><i></i></span>';
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
        return div;
    }

    function welcomeMessage() {
        if (!chatBox.children.length) {
            const msg = currentT ? currentT.welcome : PAGE_STRINGS.welcome;
            addMessage(msg, "bot");
            speakText(msg);
        }
    }

    async function sendQuestion(question) {
        question = (question || "").trim();
        if (!question || busy) return;

        busy = true;
        sendBtn.disabled = true;

        addMessage(question, "user");
        chatInput.value = "";

        const typing = addTypingMessage();

        try {
            const resp = await fetch("/api/assistant", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: question, language: currentLang })
            });
            const data = await resp.json();

            typing.remove();

            if (!data.success) {
                addMessage(data.message || "Sorry, the assistant is unavailable right now.", "bot");
                return;
            }

            addMessage(data.reply, "bot");
            speakText(data.reply);
        } catch (err) {
            console.error(err);
            typing.remove();
            addMessage("Unable to connect to the server. Please try again.", "bot");
        } finally {
            busy = false;
            sendBtn.disabled = false;
            chatInput.focus();
        }
    }

    sendBtn.addEventListener("click", function () {
        sendQuestion(chatInput.value);
    });

    chatInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") sendQuestion(chatInput.value);
    });

    clearBtn.addEventListener("click", function () {
        chatBox.innerHTML = "";
        welcomeMessage();
    });

    document.querySelectorAll(".chat-example").forEach(function (btn) {
        btn.addEventListener("click", function () {
            sendQuestion(btn.getAttribute("data-example"));
        });
    });

    /* ---------- voice input ---------- */

    function setupVoice() {
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SR) {
            micBtn.style.display = "none";
            NLP.translate([PAGE_STRINGS.notSupported], currentLang).then(function (out) {
                addMessage(out[0], "bot");
            });
            return;
        }

        function startRecognition() {
            // Chrome throws if start() is called right after a previous session,
            // so always create a fresh recognition object.
            if (recognition) {
                recognition.stop();
                recognition = null;
            }
            recognition = new SR();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = VOICE_LANGS[currentLang] || "en-IN";

            recognition.onstart = function () {
                listening = true;
                micBtn.classList.add("listening");
                if (currentT) micBtn.title = currentT.listening;
            };

            recognition.onresult = function (event) {
                const transcript = event.results[0][0].transcript;
                chatInput.value = transcript;
                sendQuestion(transcript);
            };

            recognition.onerror = function (event) {
                listening = false;
                micBtn.classList.remove("listening");
                micBtn.title = PAGE_STRINGS.send;
                const err = event.error;
                if (err === "not-allowed" || err === "service-not-allowed" || err === "audio-capture") {
                    NLP.translate([PAGE_STRINGS.micError], currentLang).then(function (out) {
                        addMessage(out[0], "bot");
                    });
                }
                // "no-speech" and "aborted" are normal - just reset silently
            };

            recognition.onend = function () {
                listening = false;
                micBtn.classList.remove("listening");
                micBtn.title = PAGE_STRINGS.send;
            };

            recognition.start();
        }

        micBtn.addEventListener("click", function () {
            if (listening && recognition) {
                recognition.stop();
                return;
            }
            try {
                startRecognition();
            } catch (err) {
                console.error("Voice start failed:", err);
                NLP.translate([PAGE_STRINGS.micError], currentLang).then(function (out) {
                    addMessage(out[0], "bot");
                });
            }
        });
    }

    /* ---------- speech output (text-to-speech) ---------- */

    function speakText(text) {
        if (!text || !("speechSynthesis" in window)) return;
        const synth = window.speechSynthesis;
        synth.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = VOICE_LANGS[currentLang] || "en-IN";
        utter.rate = 0.95;

        const voices = synth.getVoices();
        const preferred = voices.find(function (v) {
            return v.lang && v.lang.toLowerCase().startsWith((VOICE_LANGS[currentLang] || "en-IN").split("-")[0].toLowerCase());
        });
        if (preferred) utter.voice = preferred;

        synth.speak(utter);
    }

    speakBtn.addEventListener("click", function () {
        if (!("speechSynthesis" in window)) return;
        if (window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
            return;
        }
        if (!lastBotText) return;
        speakText(lastBotText);
    });

    if (window.speechSynthesis) window.speechSynthesis.getVoices();

    /* ---------- translations ---------- */

    const PAGE_STRINGS = {
        welcome: "Hello! I am your farming assistant. Ask me about crops, fertilizers, irrigation, soil, pests, or how to use this app.",
        pageTitle: "AI Assistant",
        pageSubtitle: "Ask farming questions in your language. Text or voice both work.",
        placeholder: "Type your farming question...",
        send: "Send",
        listening: "Listening... speak now",
        notSupported: "Voice input is not supported in this browser.",
        micError: "Microphone permission denied or not available.",
        speak: "Speak",
        stopSpeak: "Stop",
        clear: "Clear Chat",
        example1: "Which crop is good for my soil?",
        example2: "When should I irrigate?",
        example3: "How to control pests?"
    };

    let currentT = null;

    function applyPageLanguage(lang) {
        currentLang = lang;
        return NLP.translate(Object.keys(PAGE_STRINGS).map(function (k) { return PAGE_STRINGS[k]; }), lang)
            .then(function (out) {
                const t = {};
                Object.keys(PAGE_STRINGS).forEach(function (k, i) { t[k] = out[i]; });
                currentT = t;
                const set = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
                set("pageTitle", t.pageTitle);
                set("pageSubtitle", t.pageSubtitle);
                chatInput.placeholder = t.placeholder;
                sendBtn.setAttribute("aria-label", t.send);
                clearBtn.title = t.clear;
                clearBtn.setAttribute("aria-label", t.clear);
                speakBtn.setAttribute("aria-label", t.speak);

                const examples = [t.example1, t.example2, t.example3];
                document.querySelectorAll(".chat-example").forEach(function (btn, i) {
                    const textEl = btn.querySelector(".chat-example-text");
                    if (textEl && examples[i]) textEl.textContent = examples[i];
                });

                welcomeMessage();
            });
    }

    document.addEventListener("agri:langchange", function (e) { applyPageLanguage(e.detail.lang); });

    setupVoice();

    applyPageLanguage(getSavedLanguage());
});
