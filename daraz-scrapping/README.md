# 🛒 Daraz Web Scraper & Data Analysis using Python 🐍

This project is a **Web Scraping and Data Analysis tool** built with **Python, Selenium, and Pandas**.  
It scrapes **product details from [Daraz.pk](https://www.daraz.pk)** based on a given keyword (e.g., "smart watch"), stores them in a CSV file, and performs **data analysis & visualization** on prices.

---

## 🚀 Features

- Scrapes real-time product data from Daraz (title, price, rating, link)  
- Supports multiple pages scraping  
- Saves clean data into a CSV file (`daraz_products.csv`)  
- Performs data analysis — average, median, cheapest, most expensive products  
- Visualizes price distribution with Matplotlib  
- Headless (no browser window pops up while scraping)  

---

## 🧰 Tech Stack

- **Python 3.x**
- **Selenium** – for dynamic web scraping  
- **Pandas** – for data processing  
- **Matplotlib** – for visualizing results  
- **WebDriverManager** – for automatic ChromeDriver setup  

---

## 📂 Project Structure

daraz-scrapping/
│
├── daraz_scrapper.py # Main Python script
├── daraz_products.csv # Output file (after scraping)
├── README.md # Project documentation
└── requirements.txt # Python dependencies 
