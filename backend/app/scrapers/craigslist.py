import time
import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urlencode

def _parse_results(html_text: str, city_hint: str | None = None):
    html = HTMLParser(html_text)
    items = []
    rows = html.css('li.result-row') or html.css('ul.rows > li')
    for row in rows:
        a = row.css_first('a.result-title') or row.css_first('a.hdrlnk')
        if not a:
            continue
        link = a.attributes.get('href', '')
        title = a.text(strip=True)
        price_el = row.css_first('span.result-price') or row.css_first('span.price')
        price = None
        try:
            if price_el:
                ptxt = price_el.text(strip=True).replace('$','').replace(',','')
                price = int(ptxt)
        except Exception:
            price = None
        img = row.css_first('img')
        photo = img.attributes.get('src') if img and img.attributes.get('src') else ''
        items.append({
            "source": "craigslist",
            "source_url": link,
            "title": title,
            "price": price,
            "photo": photo,
            "city": city_hint or "",
        })
    return items

def fetch_craigslist(location_subdomain: str = "sfbay", category: str = "apa",
                     min_price: int | None = None, max_price: int | None = None,
                     beds: float | None = None, query: str | None = None,
                     pages: int = 1, delay_sec: float = 1.5):
    base = f"https://{location_subdomain}.craigslist.org/search/{category}"
    params = {
        "min_price": min_price or "",
        "max_price": max_price or "",
        "min_bedrooms": beds or "",
        "query": query or "",
        "availabilityMode": 0,
    }
    headers = {"User-Agent": "Mozilla/5.0 (compatible; RentalBot/0.1)"}
    all_items = []
    with httpx.Client(timeout=30, headers=headers, follow_redirects=True) as client:
        for p in range(pages):
            url = f"{base}?{urlencode(params)}&s={p*120}"
            r = client.get(url)
            r.raise_for_status()
            page_items = _parse_results(r.text, city_hint=location_subdomain)
            all_items.extend(page_items)
            time.sleep(delay_sec)
    return all_items
