eBay Scraper

This project is a Python program called ebay-dl.py. It collects information about items for sale on eBay and saves it in a file that other programs can read.

What ebay-dl.py does
You give the program a search term, like "drill press".
The program gets the first 10 pages of search results for that term. It can either download them from eBay using the requests library, or read saved practice pages from a folder.
It uses Beautiful Soup (bs4) to look through the HTML of each page and find every item listed.
For each item, it collects these facts:
name: the name of the item
price: the price in cents, as a whole number (so $11.95 is saved as 1195)
status: the condition of the item, like "Brand New" or "Pre-owned"
shipping: the cost of shipping in cents (free shipping is saved as 0)
free_returns: True if the item has free returns, otherwise False
items_sold: how many of the item have been sold
If a listing is missing one of these facts, the program saves it as null (None in Python) instead of leaving it out.
It saves all the items in a JSON file named after the search term. For example, the search "drill press" creates a file called drill press.json.
How to set up

Install the two libraries the program needs:

python -m pip install requests beautifulsoup4
How to run it

The command has this pattern:

python ebay-dl.py --search "SEARCH TERM"

If eBay blocks the program, you can use the saved practice pages instead by adding --pages-dir and the folder name:

python ebay-dl.py --search "SEARCH TERM" --pages-dir practice-pages
The three searches in this repository

The three JSON files in this repository were made with the practice pages in the practice-pages folder, not with live eBay data. The practice pages are artificial listings made for this class, so the items in all three files are the same. Only the file names are different. These are the exact commands I ran:

python ebay-dl.py --search "garden tools" --pages-dir practice-pages
python ebay-dl.py --search "drill press" --pages-dir practice-pages
python ebay-dl.py --search "stuffed animal" --pages-dir practice-pages

This created these three files:

garden tools.json
drill press.json
stuffed animal.json

Project page
https://csci40.rtealwitter.com/projects/02_webscraping/project.html