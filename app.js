let source = "all";
const $ = id => document.getElementById(id);
const query = $("query"), results = $("results"), statusEl = $("status"), notice = $("notice");

function setSource(s){
  source=s;
  document.querySelectorAll("[data-source]").forEach(b=>b.classList.toggle("active", b.dataset.source===s));
}
document.querySelectorAll("[data-source]").forEach(b=>b.addEventListener("click",()=>setSource(b.dataset.source)));
$("searchBtn").addEventListener("click", search);
query.addEventListener("keydown", e=>{if(e.key==="Enter") search()});

async function search(){
  const q=query.value.trim();
  if(!q) return;
  statusEl.textContent="Searching…"; notice.classList.add("hidden");
  results.innerHTML='<div class="empty"><div class="big">⌛</div><h2>Searching</h2><p>Please wait…</p></div>';
  try{
    const r=await fetch(`/api/search?q=${encodeURIComponent(q)}&source=${source}`);
    const data=await r.json();
    render(data.items||[]);
    if((data.errors||[]).length){
      notice.textContent=data.errors.join(" • ");
      notice.classList.remove("hidden");
    }
  }catch(e){
    notice.textContent="Search failed. Check the server configuration.";
    notice.classList.remove("hidden");
    results.innerHTML="";
  }finally{statusEl.textContent="Ready"}
}
function render(items){
  if(!items.length){
    results.innerHTML='<div class="empty"><div class="big">♫</div><h2>No results</h2><p>Check your search or API configuration.</p></div>';
    return;
  }
  results.innerHTML=items.map(x=>`
    <article class="card">
      ${x.thumbnail?`<img class="thumb" src="${esc(x.thumbnail)}" alt="">`:`<div class="thumb"></div>`}
      <div class="info">
        <div class="title">${esc(x.title)}</div>
        <div class="meta">${esc(x.channel||"")}</div>
        <div class="source">${esc(x.source)}</div>
      </div>
      <div class="actions"><a class="primary" href="${esc(x.url)}" target="_blank" rel="noopener">Open</a></div>
    </article>`).join("");
}
function esc(s){
  return String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]));
}
