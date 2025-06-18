import streamlit as st
import subprocess
import json
import re

st.set_page_config(layout="wide")
st.title("🛍️ Multi-Brand Product Price Aggregator")
st.markdown("Search for fashion items across **BluOrng** and **Bewakoof**.")

search_term = st.text_input("Enter 't-shirt' to search. Currently, we are scraping only t-shirts from BluOrng and Bewakoof.")

if st.button("🔍 Search") and search_term:
    all_results = []
    brand_scrapers = {
        "BluOrng": ["python", "scrapers/bluorng.py", search_term],
        "Bewakoof": ["python", "scrapers/bewakoof.py", search_term],
    }

    for brand, command in brand_scrapers.items():
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)

            # Extract JSON array from output safely
            matches = re.findall(r'(\[\s*{.*?}\s*\])', result.stdout.strip(), re.DOTALL)
            if matches:
                json_text = matches[-1]
                data = json.loads(json_text)
                all_results.extend(data)
                st.success(f"{brand}: {len(data)} items")
            else:
                raise ValueError("No JSON array found in output.")
        except Exception as e:
            st.error(f"Error scraping {brand}: {str(e)}")
            st.markdown(f"```Raw Output:\n{result.stdout.strip()}```")

    if all_results:
        st.subheader(f"🎉 Found {len(all_results)} products!")

        cols = st.columns(3)
        index = 0

        for product in all_results:
            image_url = product.get("image")

            # Skip if image is missing or placeholder
            if not image_url or "fallback" in image_url or image_url.strip() == "":
                continue

            with cols[index % 3]:
                st.image(image_url, use_column_width=True)
                st.markdown(f"**{product['name']}**")
                st.markdown(f"**Brand:** {product['brand']}")
                st.markdown(f"**Price:** {product['price']}")
                st.markdown(f"[🔗 View Product]({product['link']})", unsafe_allow_html=True)
            index += 1
    else:
        st.warning("No products found.")
