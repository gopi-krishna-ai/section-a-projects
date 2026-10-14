const el = (id) => document.getElementById(id);
const esc = (s) => { const d = document.createElement("div"); d.textContent = s ?? ""; return d.innerHTML; };
const showLoading = (on) => { el("loading").hidden = !on; };
let DOCS = [];
let CURRENT_PACK = null;

function toast(msg) {
  const t = el("toast"); t.textContent = msg; t.hidden = false;
  clearTimeout(t._timer); t._timer = setTimeout(() => { t.hidden = true; }, 2800);
}
async function api(url, opts) {
  const res = await fetch(url, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}
const post = (url, body) => api(url, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(body || {}) });

/* tabs */
document.querySelectorAll(".tab-btn").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  btn.classList.add("active"); el("tab-" + btn.dataset.tab).classList.add("active");
  if (btn.dataset.tab === "accuracy") renderBenchmark();
}));

/* upload */
el("upload-zone").addEventListener("click", () => el("file-input").click());
el("file-input").addEventListener("change", e => { if (e.target.files.length) uploadFile(e.target.files[0]); });
["dragover","dragleave","drop"].forEach(evt => el("upload-zone").addEventListener(evt, e => {
  e.preventDefault(); el("upload-zone").classList.toggle("drag", evt === "dragover");
  if (evt === "drop" && e.dataTransfer.files.length) uploadFile(e.dataTransfer.files[0]);
}));
async function uploadFile(file) {
  el("upload-error").textContent = "";
  el("upload-status").textContent = `Processing “${file.name}” — extracting text and building semantic embeddings…`;
  showLoading(true);
  const fd = new FormData(); fd.append("file", file);
  try { const d = await api("/api/upload", {method:"POST", body:fd});
    el("upload-status").textContent = `Added “${d.name}” — ${d.pages} page(s), ${d.words.toLocaleString()} words, ${d.language.name}` + (d.ocr_pages.length ? ` · OCR on ${d.ocr_pages.length} page(s)` : "");
    await loadDocs(); toast("Document added to your study library.");
  } catch(e) { el("upload-status").textContent=""; el("upload-error").textContent=e.message; }
  finally { showLoading(false); }
}

/* documents */
async function loadDocs() {
  const d = await api("/api/documents"); DOCS = d.rows;
  el("stat-docs").textContent = DOCS.length;
  el("doc-list").innerHTML = DOCS.length ? DOCS.map(doc => `
    <div class="doc-item"><div><div class="doc-name">${esc(doc.name)}</div><div class="doc-meta">
      <span>${doc.pages} page(s)</span><span>${doc.words.toLocaleString()} words</span><span>${esc(doc.language.name)}</span><span>${doc.topic_count} topics</span>
      ${doc.ocr_pages.length ? `<span>OCR ×${doc.ocr_pages.length}</span>` : ""}
    </div></div><button class="btn small danger" data-del="${doc.id}">Remove</button></div>`).join("") : `<p class="empty">Your library is empty. Upload a study note or PDF to begin.</p>`;
  document.querySelectorAll("[data-del]").forEach(b => b.addEventListener("click", async () => {
    if (!confirm("Remove this document from the study library?")) return;
    showLoading(true); try { await api(`/api/documents/${b.dataset.del}`, {method:"DELETE"}); await loadDocs(); toast("Document removed."); }
    catch(e){ toast(e.message); } finally { showLoading(false); }
  }));
  const opts = DOCS.map(d => `<option value="${d.id}">${esc(d.name)}</option>`).join("");
  el("study-doc").innerHTML = opts || `<option value="">No documents</option>`;
  el("practice-doc").innerHTML = opts || `<option value="">No documents</option>`;
  el("ask-doc").innerHTML = `<option value="">All documents</option>` + opts;
}

/* LLM status */
async function loadLLMStatus() {
  try {
    const s = await api("/api/llm/status");
    const ready = s.available && s.installed;
    el("llm-status").textContent = ready ? `Local AI ready · ${s.model}` : (s.available ? `Ollama found · load ${s.model}` : "Local AI offline");
    el("llm-status").classList.toggle("ok", ready);
    el("stat-llm").textContent = ready ? "Ready" : "Setup";
  } catch(e) { el("llm-status").textContent = "Local AI offline"; el("stat-llm").textContent = "Setup"; }
}

/* study */
el("study-btn").addEventListener("click", async () => {
  const id = el("study-doc").value; el("study-error").textContent="";
  if(!id){el("study-error").textContent="Upload a document first.";return;}
  showLoading(true); try{ const p=await api(`/api/study/${id}`); CURRENT_PACK=p; renderStudy(p); el("study-output").hidden=false; }
  catch(e){el("study-error").textContent=e.message;} finally{showLoading(false);}
});
function renderStudy(p){
  el("summary-abstractive").textContent=p.summary_abstractive||"Not enough text to summarise.";
  el("summary-extractive").innerHTML=(p.summary_extractive||[]).map(s=>`<li>${esc(s)}</li>`).join("")||`<li class="empty">No summary available.</li>`;
  el("concept-chips").innerHTML=(p.concepts||[]).map(c=>`<button class="concept-chip" data-term="${esc(c.term)}">${esc(c.term)} <small>${c.occurrences}</small></button>`).join("");
  document.querySelectorAll(".concept-chip").forEach(c=>c.addEventListener("click",()=>explainTerm(c.dataset.term)));
  el("topic-list").innerHTML=(p.topics||[]).map(t=>`<div class="topic"><div class="topic-label">${esc(t.label)}</div><div class="topic-meta">${t.chunk_count} section(s) · pages ${t.pages.join(", ")}</div>${t.preview?`<div class="topic-meta">${esc(t.preview)}…</div>`:""}</div>`).join("")||`<p class="empty">No topics identified.</p>`;
  const maxImp=Math.max(1,...(p.exam_topics||[]).map(e=>e.importance));
  el("exam-list").innerHTML=(p.exam_topics||[]).map(e=>`<div class="exam-row"><span class="exam-name">${esc(e.term)}</span><span class="exam-bar-bg"><span class="exam-bar" style="width:${Math.round(100*e.importance/maxImp)}%"></span></span><span class="exam-cnt">${e.occurrences}×</span></div>`).join("")||`<p class="empty">Not available.</p>`;
  el("plan-list").innerHTML=(p.study_plan||[]).map(d=>`<div class="plan-day"><b>Day ${d.day}</b><ul>${d.focus.map(f=>`<li>${esc(f)}</li>`).join("")}</ul><div class="topic-meta">pages ${d.pages.join(", ")}</div></div>`).join("")||`<p class="empty">Not available.</p>`;
}
async function explainTerm(term){ const id=el("study-doc").value; showLoading(true); try{const d=await post("/api/explain",{doc_id:id,term});el("explain-box").innerHTML=`<b>${esc(d.term)}</b><br>${esc(d.explanation)}<div class="topic-meta">Source: page ${d.source_page}</div>`;el("explain-box").hidden=false;}catch(e){toast(e.message)}finally{showLoading(false)} }

/* AI Q&A */
el("ask-btn").addEventListener("click", doAskAI);
el("ask-input").addEventListener("keydown", e=>{ if((e.ctrlKey||e.metaKey)&&e.key==="Enter") doAskAI(); });
el("use-docs").addEventListener("change", updateAskBadge);
document.querySelectorAll("#quick-prompts button").forEach(b=>b.addEventListener("click",()=>{el("ask-input").value=b.dataset.q;el("ask-input").focus();}));
function updateAskBadge(){el("ask-mode-badge").textContent=el("use-docs").checked?"Docs + Local AI":"General Local AI";}
async function doAskAI(){
  const q=el("ask-input").value.trim(); el("ask-error").textContent="";
  if(!q){el("ask-error").textContent="Please enter a question.";return;}
  showLoading(true); el("ask-btn").disabled=true;
  try{
    const d=await post("/api/ask-ai",{question:q,use_docs:el("use-docs").checked,doc_id:el("ask-doc").value||null});
    let sources="";
    if((d.sources||[]).length){ sources=`<div class="source-list"><b class="topic-meta">Retrieved document evidence</b>${d.sources.slice(0,4).map(s=>`<div class="source-item"><b>${esc(s.doc_name)}</b> · page ${s.page} · ${(s.score*100).toFixed(1)}% semantic match<br>${esc(s.text.slice(0,260))}${s.text.length>260?"…":""}</div>`).join("")}</div>`; }
    const sourceMeta=d.source?`Grounded with ${esc(d.source.doc_name)} · page ${d.source.page}`:"No document source used";
    el("answer-box").innerHTML=`<div class="answer-card"><div class="answer-text">${esc(d.answer)}</div><div class="answer-meta"><span>${esc(d.mode)}</span><span>Model: ${esc(d.model)}</span><span>${sourceMeta}</span></div>${sources}</div>`;
    el("answer-box").hidden=false;
  }catch(e){el("ask-error").innerHTML=`${esc(e.message)} <code>ollama run llama3.2:3b</code>`;}
  finally{showLoading(false);el("ask-btn").disabled=false;}
}

/* semantic search */
el("search-btn").addEventListener("click",doSearch);el("search-input").addEventListener("keydown",e=>{if(e.key==="Enter")doSearch();});
async function doSearch(){const q=el("search-input").value.trim();if(!q)return;showLoading(true);try{const d=await post("/api/search",{query:q,doc_id:el("ask-doc").value||null});el("search-results").innerHTML=d.rows.length?d.rows.map(h=>`<div class="search-hit"><div class="hit-head"><span>${esc(h.doc_name)} · page ${h.page}</span><span class="hit-score">${(h.score*100).toFixed(1)}% match</span></div><div class="hit-text">${esc(h.text)}</div></div>`).join(""):`<p class="empty">No matching passages found.</p>`;}catch(e){toast(e.message)}finally{showLoading(false)}}

/* practice */
el("practice-btn").addEventListener("click",async()=>{const id=el("practice-doc").value;if(!id){toast("Upload a document first.");return;}showLoading(true);try{const p=await api(`/api/study/${id}`);renderPractice(p);el("practice-output").hidden=false;}catch(e){toast(e.message)}finally{showLoading(false)}});
function renderPractice(p){
  el("flashcards").innerHTML=(p.flashcards||[]).map((c,i)=>{const term=esc(c.front);const mastered=localStorage.getItem("mst_"+term)==="1";return `<div class="flashcard" data-term="${term}" style="position:relative; transition:0.2s; ${mastered?'opacity:0.65; border-left:4px solid #10b981;':''}"><div class="front">${term}</div><div class="hint">Click to reveal</div><div class="back" hidden>${esc(c.back)}<div style="margin-top:12px;text-align:right;"><button class="btn small master-btn" style="background:#10b981;color:#fff;"><i class="fas fa-check"></i> ${mastered?'Unmark':'Mastered'}</button></div></div></div>`;}).join("")||`<p class="empty">Not enough definitions found to build flashcards.</p>`;
  document.querySelectorAll(".flashcard").forEach(card=>{card.addEventListener("click",(e)=>{if(e.target.closest(".master-btn")){e.stopPropagation();const btn=e.target.closest(".master-btn");const term=card.dataset.term;const isMst=localStorage.getItem("mst_"+term)==="1";if(isMst){localStorage.removeItem("mst_"+term);card.style.opacity="1";card.style.borderLeft="";btn.innerHTML='<i class="fas fa-check"></i> Mastered';}else{localStorage.setItem("mst_"+term,"1");card.style.opacity="0.65";card.style.borderLeft="4px solid #10b981";btn.innerHTML='<i class="fas fa-undo"></i> Unmark';}return;}const back=card.querySelector(".back"),hint=card.querySelector(".hint");back.hidden=!back.hidden;hint.textContent=back.hidden?"Click to reveal":"Click to hide";});});
  const quiz=p.quiz||[];el("quiz").innerHTML=quiz.length?quiz.map((q,qi)=>{const stem=esc(q.question).replace("________",'<span class="blank">?</span>');return`<div class="quiz-q" data-q="${qi}"><div class="quiz-stem">${qi+1}. ${stem}</div><div class="quiz-opts">${q.options.map((o,oi)=>`<button class="quiz-opt" data-opt="${esc(o)}" data-ans="${esc(q.answer)}">${String.fromCharCode(65+oi)}) ${esc(o)}</button>`).join("")}</div><div class="quiz-explanation" hidden style="margin-top:10px; font-size:12px; color:var(--muted); background:#f8fafc; padding:10px; border-radius:8px; border-left:3px solid #6366f1;"><b>Explanation:</b> ${esc(q.explanation||'')}</div></div>`;}).join(""):`<p class="empty">Not enough content to build a quiz.</p>`;
  let answered=0,correct=0;document.querySelectorAll(".quiz-opt").forEach(btn=>btn.addEventListener("click",()=>{const parent=btn.closest(".quiz-q");if(parent.dataset.done)return;parent.dataset.done="1";answered++;const ok=btn.dataset.opt===btn.dataset.ans;if(ok)correct++;parent.querySelectorAll(".quiz-opt").forEach(o=>{if(o.dataset.opt===o.dataset.ans)o.classList.add("correct");else if(o===btn)o.classList.add("wrong")});const exp=parent.querySelector(".quiz-explanation");if(exp)exp.hidden=false;if(answered===quiz.length){el("quiz-score").textContent=`Score: ${correct} / ${quiz.length}`;el("quiz-score").hidden=false;}}));
}

/* benchmark */
function renderBenchmark(){const b=BENCHMARK||{};if(!b.reading){el("benchmark-box").innerHTML=`<p class="empty">Benchmark not run yet. Run <code>python model/benchmark_qa.py</code>.</p>`;return;}const card=(title,sub,metrics)=>`<div class="bench-card"><h4>${title}</h4><div class="sub">${sub}</div>${metrics.map(([n,v])=>`<div class="bench-metric"><span>${n}</span><span class="m-val">${v}</span></div>`).join("")}</div>`;el("benchmark-box").innerHTML=`<div class="bench-grid">${card("Reading comprehension","Correct passage supplied",[["Exact Match",(b.reading.exact_match*100).toFixed(1)+"%"],["Token F1",(b.reading.f1*100).toFixed(1)+"%"]])}${card("Retrieval + QA","Full application path",[["Exact Match",(b.retrieval.exact_match*100).toFixed(1)+"%"],["Token F1",(b.retrieval.f1*100).toFixed(1)+"%"],["Retrieval @1",(b.retrieval.retrieval_accuracy*100).toFixed(1)+"%"]])}</div><p class="note">Evaluated on <b>${b.reading.n}</b> sampled questions from <b>${esc(b.dataset)}</b>.</p>`;}

/* boot */
Promise.all([loadDocs(),loadLLMStatus()]).catch(()=>{});updateAskBadge();
