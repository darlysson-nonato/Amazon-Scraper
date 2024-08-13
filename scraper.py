import requests, json, random, time
from bs4 import BeautifulSoup

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

def save_offers(offers):
    with open("items_offers.json", "w", encoding="utf-8") as f:
        json.dump(offers, f, indent=2, ensure_ascii=False)

def get_amazon_offers(title, category, discount_threshold):
    config = load_config()
    SCRAPERAPI_KEY = config["scraperapi_key"]
    __mk_pt_BR = config["__mk_pt_BR"]
    num_pages = config["search_params"]["num_pages"]
    ref_number = config["search_params"]["ref_number"]
    base_url = config["search_params"]["base_url"]
    currency_symbol = config["currency_symbol"]
    search_params_full = {
        "k": title,
        "i": category,
        "__mk_pt_BR": __mk_pt_BR,
        "ref": f"nb_sb_noss_{ref_number}"
    }
    items_offers = []
    for page in range(1, num_pages + 1):
        search_params_full["page"] = page
        amazon_url = f"{base_url}?{requests.compat.urlencode(search_params_full)}"
        scraperapi_url = f"http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={amazon_url}"

        response = requests.get(scraperapi_url)

        if response.status_code != 200:
            print("Failed to fetch the page. Status code:", response.status_code)
            break

        soup = BeautifulSoup(response.content, "html.parser")

        print(f"Page {page} Title:", soup.title.get_text())

        items = soup.select(".s-main-slot .s-result-item")
        if not items:
            print("No items found in the page.")
            break

        for item in items:
            title_elem = item.select_one("h2 .a-link-normal")
            if not title_elem:
                continue
            title = title_elem.get_text().strip()
            print(f"Found title: {title}")

            price_whole = item.select_one(".a-price-whole")
            price_fraction = item.select_one(".a-price-fraction")
            price = None
            if price_whole and price_fraction:
                price = float(price_whole.get_text().strip().replace(",", "") + "." + price_fraction.get_text().strip())
                print(f"Found price: {price}")

            original_price_elem = item.select_one(".a-price.a-text-price .a-offscreen")
            if original_price_elem:
                original_price = float(original_price_elem.get_text().strip().replace(currency_symbol, "").replace(",", ".").strip())
                print(f"Found original price: {original_price}")

                if price and original_price and (original_price - price) / original_price >= discount_threshold / 100:
                    items_offers.append({
                        "title": title,
                        "price": price,
                        "original_price": original_price,
                        "discount": round((original_price - price) / original_price * 100, 2)
                    })
                    print(f"Added offer: {title} with {round((original_price - price) / original_price * 100, 2)}% discount")

                    save_offers(items_offers)

        time.sleep(random.uniform(1, 3))

    return items_offers

if __name__ == "__main__":
    title = input("Enter the title to search for: ")
    category = input("Enter the category (e.g., stripbooks, electronics, etc.): ")
    discount_threshold = float(input("Enter the discount percentage threshold (e.g., 40 for 40%): "))
    offers = get_amazon_offers(title, category, discount_threshold)
    print("Offers saved to items_offers.json")