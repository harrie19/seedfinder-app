import json, os, re, time
from bs4 import BeautifulSoup
import requests

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "providers.json")

def to_float(text):
    if text is None: return None
    t = re.sub(r"[^0-9.,]", "", text).replace(".", "").replace(",", ".")
    try: return float(t)
    except: return None

def scrape_provider(p):
    items=[]
    try:
        resp = requests.get(p["url"], timeout=15, headers={"User-Agent":"Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select(p["selectors"]["item"])[:50]:
            def sel(key):
                s = p["selectors"].get(key)
                if not s: return None
                el = item.select_one(s)
                return (el.get_text(strip=True) if el else None)
            name = sel("name") or "Unknown"
            price = to_float(sel("price"))
            thc = to_float(sel("thc"))
            yld = to_float(sel("yield"))
            dur = to_float(sel("duration"))
            href=None
            link_sel = p["selectors"].get("link")
            if link_sel:
                a = item.select_one(link_sel)
                if a and a.get("href"):
                    href = a.get("href")
                    if href.startswith("/"):
                        from urllib.parse import urljoin
                        href = urljoin(p["url"], href)
            items.append({provider: p.get("name",""), name: name, thc_percent: thc, yield_grams: yld, days: dur, price_eur: price, url: href or p["url"]})
    except Exception:
        pass
    return items

def scrape_all(q=""):
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            providers = json.load(f)
    except Exception:
        providers=[]
    all_items=[]
    for p in providers:
        all_items += scrape_provider(p)
        time.sleep(0.5)
    if not all_items:
        all_items=[
{provider:"DemoShop","name":"Gorilla Auto","thc_percent":20.0,"yield_grams":550,"days":70,"price_eur":29.9,"url":"https://example.com/gorilla-auto"},
{provider:"DemoShop","name":"Northern Lights Auto","thc_percent":18.0,"yield_grams":500,"days":65,"price_eur":24.9,"url":"https://example.com/nla"}
        ]
    if q:
        ql=q.lower()
        all_items=[i for i in all_items if ql in i["name"].lower()]
    return all_items
