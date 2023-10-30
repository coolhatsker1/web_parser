import asyncio
import csv
import requests
from bs4 import BeautifulSoup

CATEGORY_URL = "https://www.gorgany.com/odiah/shtany"


async def get_page_data(url):
    response = await loop.run_in_executor(None, requests.get, url)
    return response.text


async def scrape_product_data(page_url):
    response_text = await get_page_data(page_url)
    soup = BeautifulSoup(response_text, "html.parser")
    products = soup.select(".item.product.product-item")

    product_data = []
    for product in products:
        product_link = product.select_one(".product-item-link")

        if product_link:
            name = product_link.getText()
            price = product.select_one(".price").getText()
            link = product_link.get("href")
            sku = product.select_one("form").get("data-product-sku")
            product_data.append([sku, name, price, link])

    return product_data


async def scrape_category_data():
    response_text = await get_page_data(CATEGORY_URL)
    soup = BeautifulSoup(response_text, "html.parser")
    items = soup.select(".items.pages-items")
    count = len(items[0].select("a.page"))

    filename = CATEGORY_URL.split("/")[-1]
    filename = filename + ".csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["sku", "name", "price", "link"])

        tasks = []
        for i in range(count):
            page_url = f"{CATEGORY_URL}?p={i}"
            tasks.append(scrape_product_data(page_url))

        product_data_list = await asyncio.gather(*tasks)
        for product_data in product_data_list:
            writer.writerows(product_data)


async def main():
    await get_page_data(CATEGORY_URL)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    response = loop.run_until_complete(get_page_data(CATEGORY_URL))

    with open('response.txt', 'w', encoding='utf-8') as file:
        file.write(response)