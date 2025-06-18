import json
import sys
from playwright.sync_api import sync_playwright

def run_scraper_cli(search_term):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()

        url = "https://www.bewakoof.com/men-t-shirts"
        page.goto(url, timeout=60000)

        # ✅ Wait for product cards to load
        page.wait_for_selector("section[data-testid^='product-card-']", timeout=10000)

        # Scroll to load more products
        for _ in range(4):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        cards = page.query_selector_all("section[data-testid^='product-card-']")
       # print("Found cards:", len(cards))

        for card in cards:
            try:
                # Link
                link_el = card.query_selector("a")
                href = link_el.get_attribute("href") if link_el else None
                if not href:
                    continue
                full_link = "https://www.bewakoof.com" + href

                # Image
                img_el = card.query_selector("img")
                name = img_el.get_attribute("alt") if img_el else "N/A"
                img_url = img_el.get_attribute("src") if img_el else ""
                if not img_url or "fallback" in img_url:
                    continue  # skip blank/placeholder images

                # Price
                price_el = card.query_selector("div span:has-text('₹')")
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
    output = run_scraper_cli(search_term)
    print(json.dumps(output, indent=2))
