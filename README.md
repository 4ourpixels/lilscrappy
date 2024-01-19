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
