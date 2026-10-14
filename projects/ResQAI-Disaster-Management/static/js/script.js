const BAND_COLORS = { CRITICAL: '#dc2626', HIGH: '#ea580c', MEDIUM: '#ca8a04', LOW: '#64748b' };
const el = id => document.getElementById(id);
const showLoading = on => { el('loading').hidden = !on; };
const esc = s => { const d = document.createElement('div'); d.textContent = s ?? ''; return d.innerHTML; };
async function getJSON(url, opts) { const r = await fetch(url, opts); const d = await r.json(); if (!r.ok) throw new Error(d.error || d.detail || 'Request failed'); return d; }
const postJSON = (url, body) => getJSON(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body||{})});

document.querySelectorAll('.tab-btn').forEach(btn=>btn.addEventListener('click',()=>{
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active')); btn.classList.add('active');
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  const target=btn.dataset.tab;
  if(target==='incidents'){ el('tab-incidents').classList.add('active'); loadIncidents(); }
  else if(target==='trends'){ el('tab-trends').classList.add('active'); loadTrends(); }
  else if(target==='report'){ el('tab-report').classList.add('active'); loadDecisionReport(); }
  else if(target==='sources'){ el('tab-sources').classList.add('active'); }
  else if(target==='models'){ el('tab-models').classList.add('active'); renderMetrics(); }
  else if(target==='emergency'){ el('tab-emergency').classList.add('active'); initMap(); }
  else if(target==='monitor'){ el('tab-monitor').classList.add('active'); }
}));

async function loadXStatus(){
  try{ const d=await getJSON('/api/x-status'); el('x-status').innerHTML=`<span class="status-dot ${d.configured?'ok':''}"></span><span>${d.configured?'X API connected':'Simulation Mode Active (No Token)'}</span>`; }
  catch(e){ el('x-status').innerHTML='<span class="status-dot"></span><span>X API status unavailable</span>'; }
}
loadXStatus();

el('fetch-x-btn').addEventListener('click', async()=>{
  el('x-error').textContent=''; showLoading(true);
  try{
    const d=await postJSON('/api/live-x',{query:el('x-query').value.trim(),count:Number(el('x-count').value)});
    el('x-summary').innerHTML=`Fetched <b>${d.fetched}</b> posts (${esc(d.source)}). Disaster-classified posts are added to the Incident Queue. Select <b>Verify coverage</b> to find related publisher reporting.`; el('x-summary').hidden=false; renderXFeed(d.posts); loadIncidents();
  }catch(e){ el('x-error').textContent=e.message; }
  finally{ showLoading(false); }
});

function renderClassification(d){
  const cls=d.is_disaster?'is-disaster':'not-disaster';
  const terms=Object.values(d.severity_terms||{}).flat();
  
  let explainHtml = '';
  if(d.model_explanation && d.model_explanation.length > 0) {
      explainHtml = `<div class="explanation-box" style="margin-top: 15px;">
        <div style="font-size: 11px; font-weight: 800; color: #475569; text-transform: uppercase; margin-bottom: 8px;">Why the model made this prediction (Word Influence)</div>
        <div class="term-chips" style="margin-top:0">
          ${d.model_explanation.map(e => `<span class="chip ${e.weight > 0 ? 'pos' : 'neg'}" title="${e.weight > 0 ? 'Pushes toward Disaster' : 'Pushes toward Not Disaster'}">${esc(e.word)} (${e.weight > 0 ? '+' : ''}${e.weight})</span>`).join('')}
        </div>
      </div>`;
  }

  let reportHtml = `
    <div style="margin-top: 15px; padding: 12px; background: #fff; border: 1px solid var(--border); border-radius: 10px; display: flex; gap: 15px; flex-wrap: wrap;">
      <div style="flex: 1; min-width: 200px;">
        <div style="margin-bottom: 8px;">
          <span style="font-size: 11px; font-weight: 800; color: #475569; text-transform: uppercase;">What Happened:</span>
          <span style="font-size: 13px; font-weight: 600; color: var(--text);">${esc(d.category || 'Unclassified Event')}</span>
        </div>
        <div style="margin-bottom: 8px;">
          <span style="font-size: 11px; font-weight: 800; color: #475569; text-transform: uppercase;">Casualties:</span>
          <span style="font-size: 13px; font-weight: 600; color: var(--text);">${d.casualties_mentioned ? esc(d.casualties_mentioned) : 'None reported in text'}</span>
        </div>
        <div>
          <span style="font-size: 11px; font-weight: 800; color: #475569; text-transform: uppercase;">How it should be solved:</span>
          <span style="font-size: 13px; font-weight: 600; color: var(--text);">${esc(d.reaction || 'Standard monitoring.')}</span>
        </div>
      </div>
      <div id="incident-img-container" style="width: 120px; height: 90px; background: #e2e8f0; border-radius: 8px; overflow: hidden; display: flex; align-items: center; justify-content: center; position: relative;">
        <span style="font-size: 10px; color: #64748b; font-weight: bold; text-align: center; padding: 5px;">Incident Image<br>(Searching...)</span>
      </div>
    </div>
  `;

  el('classify-result').innerHTML=`<div class="result-card ${cls}">
    <div class="result-head">
      <span class="result-label ${cls}">${esc(d.label)}</span>
      ${d.is_disaster?`<span class="pill ${d.priority_band}">${d.priority_band} PRIORITY</span>`:''}
    </div>
    <div class="result-meta">
      <div>Model confidence<b>${d.confidence}%</b></div>
      <div>Priority<b>${d.priority}/100</b></div>
    </div>
    <div class="bar-bg">
      <div class="bar-fill" style="width:${d.priority}%;background:${BAND_COLORS[d.priority_band]||'#64748b'}"></div>
    </div>
    ${d.is_disaster ? reportHtml : ''}
    ${terms.length?`<div class="term-chips" style="margin-top: 15px;"><div style="width:100%; font-size: 11px; font-weight: 800; color: #475569; text-transform: uppercase; margin-bottom: 4px;">Severity terms found</div>${terms.map(t=>`<span class="chip" style="background:#fee2e2;color:#991b1b">${esc(t)}</span>`).join('')}</div>`:''}
    ${explainHtml}
  </div>`;
  el('classify-result').hidden=false;

  // Fetch realistic image from Wikipedia API based on the event details
  if(d.is_disaster) {
      let searchQuery = d.category || 'Disaster';
      if(d.category === 'Terrorism / Attack' && d.text.toLowerCase().includes('world trade center')) {
          searchQuery = 'September 11 attacks';
      } else if (d.location) {
          searchQuery = d.location + ' ' + d.category.split('/')[0].trim();
      }
      
      const wikiUrl = `https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(searchQuery)}&prop=pageimages&format=json&pithumbsize=400&gsrlimit=1&origin=*`;
      fetch(wikiUrl).then(r=>r.json()).then(data => {
          const pages = data.query?.pages;
          if(pages) {
              const page = Object.values(pages)[0];
              if(page && page.thumbnail) {
                  const imgContainer = el('incident-img-container');
                  if(imgContainer) {
                      imgContainer.innerHTML = `<img src="${page.thumbnail.source}" style="width: 100%; height: 100%; object-fit: cover;" alt="Incident Image" />`;
                  }
              } else {
                  el('incident-img-container').innerHTML = `<span style="font-size: 10px; color: #64748b; font-weight: bold; text-align: center; padding: 5px;">No Image<br>Found</span>`;
              }
          }
      }).catch(e => {
          el('incident-img-container').innerHTML = `<span style="font-size: 10px; color: #64748b; font-weight: bold; text-align: center; padding: 5px;">No Image<br>Found</span>`;
      });
  }
}

el('classify-btn').addEventListener('click',async()=>{
  const text=el('tweet-text').value.trim(); el('classify-error').textContent=''; if(!text){el('classify-error').textContent='Enter a report first.';return;} showLoading(true);
  try{renderClassification(await postJSON('/api/classify',{text,location:el('tweet-location').value.trim()||null}));}catch(e){el('classify-error').textContent=e.message;}finally{showLoading(false);}
});

if(el('run-demo-btn')) {
  el('run-demo-btn').addEventListener('click', () => {
    // Fill with a real, high-priority realistic disaster incident
    el('tweet-text').value = "BREAKING: Massive 7.8 magnitude earthquake just struck central Turkey. Multiple residential high-rise buildings have completely collapsed. Hundreds feared trapped under the rubble. Emergency rescue teams urgently needed on site!";
    el('tweet-location').value = "Turkey";
    if(el('char-counter')) el('char-counter').textContent = el('tweet-text').value.length + ' chars';
    
    // Auto-trigger classification
    el('classify-btn').click();
  });
}

if(el('clear-input-btn')) {
    el('clear-input-btn').addEventListener('click', () => {
        el('tweet-text').value = '';
        el('tweet-location').value = '';
        el('classify-result').hidden = true;
        el('classify-error').textContent = '';
        if(el('char-counter')) el('char-counter').textContent = '0 chars';
    });
}

if(el('tweet-text') && el('char-counter')) {
    el('tweet-text').addEventListener('input', (e) => {
        el('char-counter').textContent = e.target.value.length + ' chars';
    });
}

function renderXFeed(posts){
  const host=el('x-feed');
  if(!posts.length){host.innerHTML='<div class="empty">No posts matched this query. Try a broader disaster keyword.</div>';return;}
  host.innerHTML=posts.map((p,i)=>{
    const disaster=!!p.is_disaster; const dt=p.created_at?new Date(p.created_at).toLocaleString():'';
    const metrics=p.public_metrics||{};
    return `<article class="x-card ${disaster?'disaster':'safe'}"><div class="x-top"><div><div class="author">${esc(p.author_name)} ${p.verified?'✓':''}</div><div class="handle">@${esc(p.username)}</div></div><span class="pill ${disaster?p.priority_band:'LOW'}">${esc(p.label)}${disaster?' · '+esc(p.priority_band):''}</span></div><div class="x-text">${esc(p.text)}</div><div class="x-meta"><span>${esc(dt)}</span><span>${p.confidence}% confidence</span><span>♥ ${metrics.like_count??0}</span><span>↻ ${metrics.retweet_count??0}</span><span>Reply ${metrics.reply_count??0}</span></div><div class="x-actions">${p.url?`<a class="action-link primary" href="${p.url}" target="_blank" rel="noopener">Open original X post ↗</a>`:''}<button class="action-link" data-index="${i}">Verify coverage</button></div></article>`;
  }).join('');
  host.querySelectorAll('button[data-index]').forEach(btn=>btn.addEventListener('click',()=>verifyCoverage(posts[Number(btn.dataset.index)])));
  window.__lastXPosts=posts;
}

theory();
function theory(){}

async function verifyCoverage(post){
  // Automatically switch to the Sources tab
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.querySelector('.tab-btn[data-tab="sources"]').classList.add('active');
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  el('tab-sources').classList.add('active');

  const words = post.text.replace(/https?:\/\/\S+/g,' ').replace(/[^\w\s#-]/g,' ').split(/\s+/).filter(w=>w.length>3);
  const seed = words.filter(w=>/earthquake|flood|wildfire|fire|storm|cyclone|tornado|tsunami|explosion|collapse|crash|disaster|emergency|evacuat|landslide|rescue|hurricane/i.test(w)).slice(0,5);
  const query = seed.length ? seed.join(' ') : words.slice(0,6).join(' ');
  el('source-query-label').textContent=`Coverage search: ${query}`; el('news-sources').innerHTML='<div class="empty">Searching Google News coverage…</div>'; showLoading(true);
  try{
    const d=await getJSON('/api/news-sources?q='+encodeURIComponent(query)+'&limit=5');
    if(!d.sources.length){el('news-sources').innerHTML='<div class="empty">No related publisher results were returned. Try a more specific place, disaster type, or headline term.</div>';return;}
    el('news-sources').innerHTML=d.sources.map(s=>`<article class="news-card"><div class="publisher">${esc(s.publisher)}</div><div class="title">${esc(s.title)}</div><div class="date">${esc(s.published)}</div><a href="${s.link}" target="_blank" rel="noopener">Open publisher article ↗</a></article>`).join('');
  }catch(e){el('news-sources').innerHTML=`<div class="empty">${esc(e.message)}</div>`;} finally{showLoading(false);}
}

el('clear-feed-btn').addEventListener('click',()=>{el('x-feed').innerHTML='<div class="empty">Feed cleared. Fetch live posts to begin again.</div>';el('x-summary').hidden=true;el('news-sources').innerHTML='<div class="empty">Select “Verify coverage” on an X post.</div>';el('source-query-label').textContent='No post selected.';});


const DEMO_ROWS = [
  {priority:88, priority_band:'CRITICAL', category:'Terrorism / Attack', location:'New York', confidence:91.4, text:'The moment shocked the nation. Two planes, hijacked by Islamic jihadists vowing death to all Americans, plowed into both towers at the World Trade Center in New York.'},
  {priority:73, priority_band:'HIGH', category:'Fire / Wildfire', location:'Bengaluru', confidence:87.2, text:'Large fire reported near an industrial area with smoke visible from nearby roads.'},
  {priority:61, priority_band:'CRITICAL', category:'Earthquake / Landslide', location:'Himachal Pradesh', confidence:89.6, text:'Strong tremors followed by a landslide blocking a mountain road.'},
  {priority:47, priority_band:'HIGH', category:'Transport Accident', location:'Mumbai', confidence:82.1, text:'Major road accident reported; emergency services requested at the scene.'},
  {priority:31, priority_band:'MEDIUM', category:'Severe Weather', location:'Hyderabad', confidence:76.8, text:'Severe storm warning with localized damage and power interruptions.'}
];

async function loadIncidents(){
  try{const d=await getJSON('/api/incidents?limit=50'); renderIncidents(d.rows||[]);}catch(e){el('incident-table').innerHTML=`<div class="empty">${esc(e.message)}</div>`;}
}
function renderIncidents(rows){
  const bands={}; rows.forEach(r=>bands[r.priority_band]=(bands[r.priority_band]||0)+1);
  el('incident-summary').innerHTML=[['Total',rows.length],['Critical',bands.CRITICAL||0],['High',bands.HIGH||0],['Medium',bands.MEDIUM||0]].map(([a,b])=>`<div class="queue-stat"><span>${a}</span><strong>${b}</strong></div>`).join('');
  if(!rows.length){el('incident-table').innerHTML='<div class="empty">Queue is empty. Analyse a report or fetch live X posts to add disaster incidents.</div>';return;}
  el('incident-table').innerHTML=rows.map(r=>`<div class="incident-row"><div><div class="priority">${r.priority}</div><span class="pill ${esc(r.priority_band)}">${esc(r.priority_band)}</span></div><div><strong>${esc(r.category||'Other')}</strong><div class="text">${esc(r.text)}</div><div class="meta">${esc(r.location||'Location not provided')} · ${r.confidence}% confidence</div></div><div class="meta">${esc(r.timestamp||'')}</div></div>`).join('');
}

async function loadTrends(){
  try{const d=await getJSON('/api/trends'); const live=(d.categories||[]).length>0; renderTrendData(live?d:null);}catch(e){renderTrendData(null);}
}
function renderTrendData(d){
  const rows=d?DEMO_ROWS.map((x)=>x):DEMO_ROWS; const live=!!d;
  el('trend-mode').textContent=live?'Live session data':'Demo snapshot';
  const total=live?Object.values(d.bands||[]).reduce((a,x)=>a+(x.count||0),0):rows.length;
  const critical=live?((d.bands||[]).find(x=>x.name==='CRITICAL')||{}).count||0:2;
  const high=live?((d.bands||[]).find(x=>x.name==='HIGH')||{}).count||0:2;
  const categories=live?(d.categories||[]):DEMO_ROWS.reduce((a,r)=>{const f=a.find(x=>x.name===r.category);if(f)f.count++;else a.push({name:r.category,count:1});return a},[]);
  el('trend-cards').innerHTML=[['Reports tracked',total],['Critical',critical],['High',high],['Top categories',categories.length]].map(([l,v])=>`<div class="stat-card"><div class="label">${l}</div><div class="value">${v}</div></div>`).join('');
  el('trend-categories').innerHTML=categories.slice(0,6).map(x=>`<div class="mini-row"><span>${esc(x.name)}</span><span>${x.count}</span></div>`).join('');
  const bands=live?(d.bands||[]):DEMO_ROWS.reduce((a,r)=>{const f=a.find(x=>x.name===r.priority_band);if(f)f.count++;else a.push({name:r.priority_band,count:1});return a},[]);
  el('trend-bands').innerHTML=bands.map(x=>`<div class="mini-row"><span>${esc(x.name)}</span><span>${x.count}</span></div>`).join('');
}

async function loadDecisionReport(){
  try{const d=await getJSON('/api/report'); if((d.summary||[]).length>0){el('report-mode').textContent=d.summary[0].startsWith('No disaster')?'Demo report':'Live session report'; renderReport(d.summary, !d.summary[0].startsWith('No disaster'));}else renderReport([],false);}catch(e){renderReport([],false);}
}
function renderReport(summary,live){
  if(!live || !summary.length || summary[0].startsWith('No disaster')){
    el('report-mode').textContent='Demo report';
    el('decision-report').innerHTML=DEMO_ROWS.slice(0,4).map((r,i)=>`<div class="report-item demo"><strong>${i===0?'Priority focus':i===1?'Situation summary':i===2?'Resource cue':'Verification cue'}</strong>${esc(i===0?'Prioritize the CRITICAL flood and earthquake reports for immediate review.':i===1?'The demo snapshot contains a small mix of flood, fire, earthquake, transport and weather events.':i===2?'Prepare rescue, medical and traffic-control resources for the highest-priority locations.':'Cross-check major claims against official agencies and independent publisher coverage before dispatch.')}</div>`).join('');
    return;
  }
  el('decision-report').innerHTML=summary.map(t=>`<div class="report-item"><strong>Live decision insight</strong>${esc(t)}</div>`).join('');
}

el('clear-incidents-btn').addEventListener('click',async()=>{try{await postJSON('/api/clear',{});loadIncidents();}catch(e){alert(e.message);}});

function renderMetrics(){
 const rows=Object.entries(MODEL_METRICS?.scores||{});
 el('metrics-table').innerHTML='<thead><tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>CV F1</th></tr></thead><tbody>'+rows.map(([name,m])=>`<tr class="${name===MODEL_METRICS.best_model?'winner':''}"><td>${esc(name)}${name===MODEL_METRICS.best_model?' ★':''}</td><td>${m.accuracy}</td><td>${m.precision}</td><td>${m.recall}</td><td>${m.f1}</td><td>${m.cv_f1 ?? '-'}</td></tr>`).join('')+'</tbody>';
 el('dataset-note').textContent=`Best model: ${MODEL_METRICS.best_model}. Live X screening uses the same trained classifier; current X posts are analysed online and are not treated as ground-truth labels.`;
}

let mapInitialized = false;
function initMap() {
    if (mapInitialized) return;
    mapInitialized = true;
    
    setTimeout(() => {
        const map = L.map('map').setView([20.5937, 78.9629], 5);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        const incidents = [
            {lat: 28.7041, lng: 77.1025, title: 'Delhi - Heavy Rains'},
            {lat: 19.0760, lng: 72.8777, title: 'Mumbai - Building Collapse'},
            {lat: 13.0827, lng: 80.2707, title: 'Chennai - Flooding'},
            {lat: 31.1048, lng: 77.1734, title: 'Himachal Pradesh - Landslide'}
        ];

        const redIcon = new L.Icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        incidents.forEach(inc => {
            L.marker([inc.lat, inc.lng], {icon: redIcon}).addTo(map).bindPopup('<b>Incident:</b> ' + inc.title);
            L.circle([inc.lat, inc.lng], {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.2,
                radius: 50000
            }).addTo(map);
        });

        const helpCenters = [
            {lat: 28.5355, lng: 77.3910, title: 'NDRF Base - Noida'},
            {lat: 18.5204, lng: 73.8567, title: 'Pune - Regional Command Center'},
            {lat: 22.5726, lng: 88.3639, title: 'Kolkata - Disaster Management Office'},
            {lat: 30.7333, lng: 76.7794, title: 'Chandigarh - Emergency Response'}
        ];
        
        helpCenters.forEach(help => {
            L.marker([help.lat, help.lng]).addTo(map).bindPopup('<b>Help Center:</b> ' + help.title);
        });
    }, 100);
}

