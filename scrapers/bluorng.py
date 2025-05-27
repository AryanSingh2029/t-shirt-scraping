import requests
import json
import sys

def scrape_bluorng(search_term):
    url = "https://www.bluorng.com/products.json"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json().get("products", [])
    results = []

    for product in data:
        title = product.get("title", "")
        if search_term.lower() in title.lower():
            results.append({
                "name": title,
                "brand": "BluOrng",
                "price": product.get("variants", [{}])[0].get("price", "N/A"),
                "link": f"https://www.bluorng.com/products/{product.get('handle')}",
                "image": product.get("images", [{}])[0].get("src", "")
            })

    return results

# ✅ Add this block for CLI support
if __name__ == "__main__":
    search = sys.argv[1] if len(sys.argv) > 1 else ""
    output = scrape_bluorng(search)
    print(json.dumps(output))
