import json
import sys
from playwright.sync_api import sync_playwright

def run_scraper_cli(search_term):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://www.thesouledstore.com/men/t-shirts"

        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")
        except Exception:
            browser.close()
            return results

        for _ in range(4):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        cards = page.query_selector_all("div.productlist.productCard")

        for card in cards:
            try:
                link_el = card.query_selector("a")
                href = link_el.get_attribute("href") if link_el else None
                if not href:
                    continue

                full_link = "https://www.thesouledstore.com" + href
                name = href.split("/")[-1].split("?")[0].replace("-", " ").title()

                img_el = card.query_selector("img")
                img_url = img_el.get_attribute("data-src") or img_el.get_attribute("src") if img_el else ""
                if not img_url or "fallback" in img_url or img_url.strip() == "":
                    continue

                results.append({
                    "name": name,
                    "brand": "SouledStore",
                    "price": "N/A",
                    "link": full_link,
                    "image": img_url
                })
            except:
                continue

        browser.close()
        return results

if __name__ == "__main__":
    search_term = sys.argv[1] if len(sys.argv) > 1 else ""
    output = run_scraper_cli(search_term)

    # ✅ Absolutely no print statements except this
    sys.stdout.write(json.dumps(output))
