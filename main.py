import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from tkinter import Tk, Label, Entry, Button, StringVar

def fetch_product_info(url_ru, url_de):
    wb = Workbook()
    ws = wb.active
    ws.append(['Language', 'Title', 'Price']) 

    urls = {'RU': url_ru, 'DE': url_de}

    for lang, url in urls.items():
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        product_blocks = soup.find_all('div', class_='styles_Product__Tp3hW styles_ProductLoyalty__6RCk5')

        for product in product_blocks:
            title = product.find('div', class_='styles_ProductTitle__CjGN4').text.strip()
            price = product.find('div', class_='styles_PriceDiscount__zS0u0 styles_PriceDiscountInline__Karf8').text.strip()
            ws.append([lang, title, price])

    wb.save('products.xlsx')
    print("Datele au fost inscrise in 'products.xlsx'")

def submit():
    url_ru = url_ru_var.get()
    url_de = url_de_var.get()
    fetch_product_info(url_ru, url_de)

root = Tk()
root.title("URL Input for Product Info")

Label(root, text="Russian URL:").grid(row=0, column=0)
url_ru_var = StringVar()
Entry(root, textvariable=url_ru_var).grid(row=0, column=1)

Label(root, text="German URL:").grid(row=1, column=0)
url_de_var = StringVar()
Entry(root, textvariable=url_de_var).grid(row=1, column=1)

Button(root, text="Fetch and Save to Excel", command=submit).grid(row=2, column=0, columnspan=2)

root.mainloop()
