import json
import sys
from playwright.sync_api import sync_playwright

def run_scraper_cli(search_term):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Only go to main t-shirt listing (search_term not required here)
        url = "https://www.bewakoof.com/men-t-shirts"
        page.goto(url, timeout=60000)

        # Scroll to load more products
        for _ in range(4):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        cards = page.query_selector_all("section[data-testid='product-card']")

        for card in cards:
            try:
                link_el = card.query_selector("a[data-testid='product-card-link']")
                href = link_el.get_attribute("href")
                if not href or not href.startswith("/p/"):
                    continue

                full_link = "https://www.bewakoof.com" + href

                # ✅ Get product name from image alt
                img_el = card.query_selector("img")
                name = img_el.get_attribute("alt") if img_el else "N/A"
                img_url = img_el.get_attribute("src") if img_el else ""

                # ✅ Get price text
                price_el = card.query_selector("div[class*='jpPcAM']")
                price = price_el.inner_text().strip() if price_el else "N/A"

                results.append({
                    "name": name,
                    "brand": "Bewakoof",
                    "price": price,
                    "link": full_link,
                    "image": img_url
                })
            except Exception:
                continue

        browser.close()
        return results

if __name__ == "__main__":
    search_term = sys.argv[1] if len(sys.argv) > 1 else ""
    output = run_scraper_cli(search_term)  # ❌ this returns None in your current code
    print(json.dumps(output))  # ✅ only this should print
