from scrapers.souledstore import scrape_souledstore

results = scrape_souledstore("oversized")  # Try "t-shirt", "oversized", "hoodie"
print("Total:", len(results))
for item in results[:5]:
    print(item)
