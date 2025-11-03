import time
import csv
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# --------------------- SCRAPER FUNCTION ---------------------
def scrape_daraz(keyword, pages):
    print("[+] Starting Chrome WebDriver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    all_products = []

    for page in range(1, pages + 1):
        url = f"https://www.daraz.pk/catalog/?q={keyword.replace(' ', '+')}&page={page}"
        print(f"[+] Fetching page {page}: {url}")
        driver.get(url)
        time.sleep(5)

        products = driver.find_elements(By.CSS_SELECTOR, "div[data-qa-locator='product-item']")
        print(f"    → Found {len(products)} items on page {page}")

        for product in products:
            # Extract title
            try:
                title = product.find_element(By.CSS_SELECTOR, "div.title--wFj93, div.info--ifj7U").text.strip()
            except:
                title = "N/A"

            # Extract price (latest Daraz class)
            try:
                price = product.find_element(By.CSS_SELECTOR, "span.ooOxS").text.strip()
            except:
                # fallback if class changes
                try:
                    price = product.find_element(
                        By.XPATH, './/span[contains(@class,"ooOxS") or contains(text(),"Rs.")]'
                    ).text.strip()
                except:
                    price = "N/A"

            # Extract link
            try:
                link = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                link = "N/A"

            # Extract rating (optional)
            try:
                rating = product.find_element(By.CSS_SELECTOR, "span.rating--pwPrp").text.strip()
            except:
                rating = "N/A"

            all_products.append({
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Link": link
            })

    driver.quit()

    if not all_products:
        print("[-] No data scraped at all.")
        return

    # Save to CSV
    with open("daraz_products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Rating", "Link"])
        writer.writeheader()
        writer.writerows(all_products)

    print(f"[+] Scraped {len(all_products)} products and saved to daraz_products.csv")

    # Show a few sample prices
    print("[+] Sample scraped prices:")
    for p in all_products[:5]:
        print("   →", p["Price"])


# --------------------- ANALYSIS FUNCTION ---------------------
def analyze_data():
    print("\n[+] Starting Data Analysis...")

    try:
        df = pd.read_csv("daraz_products.csv")
    except FileNotFoundError:
        print("[-] Error: 'daraz_products.csv' not found. Please run the scraper first.")
        return

    # Clean and extract numeric prices
    df["Price"] = (
        df["Price"]
        .astype(str)
        .str.replace("Rs.", "", regex=False)
        .str.replace("₨", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.extract(r"(\d+)", expand=False)
    )

    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Price"])

    if df.empty:
        print("[-] No valid prices found. Here’s a sample of what was scraped:")
        print(df.head())
        return

    # --- Analysis ---
    print("\nTop 5 Most Expensive Products:")
    print(df.sort_values("Price", ascending=False).head(5)[["Title", "Price"]])

    print("\nTop 5 Cheapest Products:")
    print(df.sort_values("Price", ascending=True).head(5)[["Title", "Price"]])

    print("\nAverage Price:", round(df["Price"].mean(), 2))
    print("Median Price:", round(df["Price"].median(), 2))
    print("Total Products Analyzed:", len(df))

    # --- Visualization ---
    plt.figure(figsize=(8, 5))
    df["Price"].plot(kind="hist", bins=20, edgecolor='black')
    plt.title("Price Distribution of Products")
    plt.xlabel("Price (PKR)")
    plt.ylabel("Number of Products")
    plt.grid(axis='y', alpha=0.75)
    plt.show()


# --------------------- MAIN EXECUTION ---------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daraz Product Scraper with Data Analysis")
    parser.add_argument("-k", "--keyword", type=str, default="smart watch", help="Search keyword")
    parser.add_argument("-p", "--pages", type=int, default=2, help="Number of pages to scrape")
    args = parser.parse_args()

    scrape_daraz(args.keyword, args.pages)
    analyze_data()
