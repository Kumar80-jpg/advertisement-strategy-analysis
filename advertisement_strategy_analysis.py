import asyncio
from playwright.async_api import async_playwright
import pyautogui
import csv
import time

brands = ["Nike advertisement", "Apple advertisement", "Coca Cola advertisement"]

async def scrape_ads():

    results = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for brand in brands:

            print(f"Searching ads for: {brand}")

            search_url = f"https://www.youtube.com/results?search_query={brand.replace(' ', '+')}"
            await page.goto(search_url)

            await page.wait_for_timeout(5000)

            videos = await page.query_selector_all("ytd-video-renderer")

            count = 0

            for video in videos[:5]:

                title_element = await video.query_selector("#video-title")
                title = await title_element.inner_text()

                views_element = await video.query_selector("#metadata-line span")
                views = await views_element.inner_text()

                results.append([brand, title, views])

                count += 1

            # Screenshot using PyAutoGUI
            time.sleep(2)
            screenshot = pyautogui.screenshot()
            screenshot.save(f"{brand.replace(' ', '_')}_ads.png")

        await browser.close()

    # Save to CSV
    with open("advertisement_analysis.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Brand Search", "Ad Title", "Views"])
        writer.writerows(results)

    print("Data saved to advertisement_analysis.csv")


asyncio.run(scrape_ads())