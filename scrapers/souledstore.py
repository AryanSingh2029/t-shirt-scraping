import json
import sys
from playwright.sync_api import sync_playwright

def run_scraper_cli(search_term):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "https://www.thesouledstore.com/men/t-shirts"
        page.goto(url, timeout=60000)

        for _ in range(4):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        cards = page.query_selector_all("div.productlist.productCard")

        for card in cards:
            try:
                link_el = card.query_selector("a")
                href = link_el.get_attribute("href")
                if not href:
                    continue
                full_link = "https://www.thesouledstore.com" + href

                name = href.split("/")[-1].split("?")[0].replace("-", " ").title()

                img_el = card.query_selector("img")
                img_url = None
                if img_el:
                    img_url = img_el.get_attribute("data-src") or img_el.get_attribute("src")

                # ✅ skip if image is still None or a placeholder
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
    print(json.dumps(output))
