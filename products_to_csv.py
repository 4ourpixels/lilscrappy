"""
This Python script serves as a web scraping tool designed 
to extract detailed information about products.

The script takes a list of URLs corresponding to different product 
categories and retrieves essential details for each product, 
including the product name, description, brand, category, 
and images.

// Features:

1. User Input for Customization:

Users can customize certain parameters such as the product image class, 
description class, and product elements class to tailor the script 
according to specific webpage structures.

2. Dynamic URL Input:

The script prompts users to input a list of URLs, allowing flexibility 
in the choice of product categories or pages to scrape. Default URLs are 
provided for convenience.

3. CSV Output:

The extracted product information is saved in a CSV file (data.csv), 
making it easy to analyze and manipulate the data in spreadsheet 
applications or other tools.

4. Progress Tracking:

Utilizes the tqdm library to display a progress bar, providing a visual 
representation of the scraping progress.
// How to Use:

1. Clone the repository.
2. Install the required Python libraries: requests, BeautifulSoup, json, csv, and tqdm.
3. Run the script and follow the prompts to input custom values or use default settings.
4. Retrieve the scraped product information in the generated CSV file.

"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from tqdm import tqdm

# Define default values, modify if needed
product_class_images = input("Enter product image class (default is 'lazyload'): ") or "lazyload"
product_class_description = input("Enter product description class (default is 'description-text'): ") or "description-text"
product_elements_class = input("Enter product elements class (default is 'product-overview'): ") or 'product-overview'

# Get user input for list of URLs
urls_input = input("Enter a list of URLs separated by commas: ")
urls = [url.strip() for url in urls_input.split(',')] if urls_input else []

# List to store all product information
all_products_info = []

def calculate_percentage(part, whole):
    """
    Calculate the percentage completion.
    """
    try:
        percentage = (part / whole) * 100
        return percentage
    except ZeroDivisionError:
        return "Cannot divide by zero."

def get_product_images(href):
    """
    Get product images with .jpg or .jpeg extensions.
    """
    valid_extensions = {".jpeg", ".jpg"}
    try:
        response = requests.get(href)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_image_elements = soup.find_all('img', class_=product_class_images)
            product_images = []
            for element in product_image_elements:
                img_src = element.get('data-src') or element.get('src')
                if any(img_src.lower().endswith(ext) for ext in valid_extensions):
                    product_images.append(img_src)
            return product_images
        else:
            print(f"Failed to retrieve content from {href}. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error occurred while crawling {href}: {str(e)}")
        return []

# Can modify the product class if needed
def get_product_description(href):
    """
    Get product description.
    """
    try:
        response = requests.get(href)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_description_elements = soup.find_all('span', class_=product_class_description)
            if product_description_elements:
                description = [element.get_text(strip=True) for element in product_description_elements]
                return description[0]
            else:
                return "No Description"
        else:
            print(f"Failed to retrieve content from {href}. Status code: {response.status_code}")
            return "No Description"
    except Exception as e:
        print(f"Error occurred while crawling {href}: {str(e)}")
        return "No Description"

def get_product_name(alt):
    """
    Get product name from the 'alt' attribute of the image tag.
    """
    return alt.split('|')[0].strip()

def get_product_category(alt):
    """
    Get product category from the 'alt' attribute of the image tag.
    """
    return alt.split('|')[1].strip()

def get_product_brand(alt):
    """
    Get product brand from the 'alt' attribute of the image tag.
    """
    return alt.split('|')[2].strip()

url_counter = 1
for url in urls:
    response = requests.get(url)
    url_percentage = calculate_percentage(url_counter, len(urls))
    print(f"{url_percentage:.2f}%")
    if response.status_code == 200:
        context = {}
        soup = BeautifulSoup(response.text, 'html.parser')
        product_elements = soup.find_all('li', class_=product_elements_class)
        thumbnails = []
        hrefs = []
        product_images = []
        products_info = []
        product_id_counter = 1

        for product_element in tqdm(product_elements, desc="Scraping Progress", unit="product"):
            a_tag = product_element.find('a')
            if a_tag:
                href = a_tag.get('href')
                hrefs.append(href)
                description = get_product_description(href)
                product_images = get_product_images(href)

                img_tag = product_element.find('img')

                if img_tag:
                    alt = img_tag.get('alt') or img_tag.get('alt')
                    name = get_product_name(alt)
                    category = get_product_category(alt)
                    brand = get_product_brand(alt)
                    img_src = img_tag.get('data-src') or img_tag.get('src')
                    thumbnail = img_src
                    product_images.append(thumbnail)
                else:
                    print("No img tag found in the product.")

                percentage = calculate_percentage(product_id_counter, len(product_elements))
                print(f"{percentage:.2f}%")

                product_info = {
                    "id": product_id_counter,
                    "href": href,
                    "thumbnail": thumbnail,
                    "name": name,
                    "product_images": product_images,
                    "description": description,
                    "brand": brand,
                    "category": category,
                }
                products_info.append(product_info)
                product_id_counter += 1
        context.update({
            "products_info": products_info,
        })
        all_products_info.extend(products_info)
    url_percentage += 1

# Specify the CSV file name
csv_filename = 'data.csv'

# Write all data to a CSV file
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(["id", "href", "thumbnail", "name", "product_images", "description", "brand", "category"])

    # Write data rows
    for product_info in all_products_info:
        csv_writer.writerow([
            product_info["id"],
            product_info["href"],
            product_info["thumbnail"],
            product_info["name"],
            json.dumps(product_info["product_images"]),
            product_info["description"],
            product_info["brand"],
            product_info["category"]
        ])

print(f"Results saved to '{csv_filename}'")
