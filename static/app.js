const results = document.querySelector("#results");
let sort = "price";
let order = "asc";

function setActive() {
  const map = {
    price: document.getElementById("btnSortPrice"),
    thc: document.getElementById("btnSortTHC"),
    yield: document.getElementById("btnSortYield"),
    duration: document.getElementById("btnSortDuration")
  };
  Object.values(map).forEach(b=>b.classList.remove("active"));
  (map[sort]||map.price).classList.add("active");
  document.getElementById("btnOrderAsc").classList.toggle("active", order==="asc");
  document.getElementById("btnOrderDesc").classList.toggle("active", order==="desc");
}

async function run() {
  results.innerHTML = "<div class=\\"loading\\">Suche läuft...</div>";
  const res = await fetch(`/search?sort=${sort}&order=${order}`);
  const data = await res.json();
  if (!data.length) { results.innerHTML = "<div class=\\"empty\\">Keine Ergebnisse.</div>"; return; }
  results.innerHTML = data.map(item => {
    const meta = [
      item.thc_percent!=null?`THC: ${item.thc_percent}%`:"",
      item.yield_grams!=null?`Ertrag: ${item.yield_grams} g`:"",
      item.days!=null?`Dauer: ${item.days} Tage`:"",
      item.price_eur!=null?`Preis: € ${item.price_eur.toFixed(2)}`:""
    ].filter(Boolean).join(" • ");
    const title = `${item.name}` + (item.provider?` — ${item.provider}`:"");
    return `<a class="row" href="${item.url}" target="_blank" rel="noopener noreferrer">` +
           `<div class="title">${title}</div>` +
           `<div class="meta">${meta}</div>` +
           `</a>`;
  }).join("");
}

document.getElementById("btnSortPrice").addEventListener("click", ()=>{ sort="price"; setActive(); });
document.getElementById("btnSortTHC").addEventListener("click", ()=>{ sort="thc"; setActive(); });
document.getElementById("btnSortYield").addEventListener("click", ()=>{ sort="yield"; setActive(); });
document.getElementById("btnSortDuration").addEventListener("click", ()=>{ sort="duration"; setActive(); });
document.getElementById("btnOrderAsc").addEventListener("click", ()=>{ order="asc"; setActive(); });
document.getElementById("btnOrderDesc").addEventListener("click", ()=>{ order="desc"; setActive(); });
document.getElementById("searchBtn").addEventListener("click", run);

window.addEventListener("DOMContentLoaded", ()=>{ setActive(); /* Suche startet erst beim Klick auf Search */ });
