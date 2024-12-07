# import time
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver

# #opens link
# driver = webdriver.Chrome()
# driver.get('https://www.pulitzer.org/')

# results = []
# content = driver.page_source
# soup = BeautifulSoup(content, 'html.parser')

# input("Press Enter to close the browser...")
# driver.quit()  # Close the browser after the input

#page dynamically loaded by javascript, figure out how to wait for page to finish loading and get ALL html elements

# print(soup.prettify())

# for element in soup.find_all(attrs={'class': 'slide-wrapper'}):
#     image = element.find(attrs={'class': 'winning-work-image'})
#     caption = element.find(attrs={'class': 'ng-binding'})

#     if image:
#         image_url = image.get('src')
#         results.append(image_url)
    
#     if caption:
#         caption_text = caption.get_text(strip=True)
#         results.append(caption_text)

# for x in results:
#     print(x)


import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib, io, requests, pandas as pd
from PIL import Image
from pathlib import Path

options = uc.ChromeOptions()
options.headless = False  # Keep the browser visible for manual interaction

driver = uc.Chrome(use_subprocess=True, options=options)
driver.get("https://www.pulitzer.org/winners/photography-staff-associated-press-1")

# Allow time for manual CAPTCHA solving
print("Solve the CAPTCHA manually and press Enter to continue...")
input()

# Continue after CAPTCHA
time.sleep(10)  # Give extra time for the page to load, website timelimit

html_source = driver.page_source

# Save the HTML to a file
with open("webpage.html", "w", encoding="utf-8") as file:
    file.write(html_source)
print("HTML data saved to webpage.html")
driver.save_screenshot("after_captcha.png")

# find link, click


soup = BeautifulSoup(html_source, 'html.parser')
results = []
base_url = "https://www.pulitzer.org"

for element in soup.find_all(attrs={'class': 'slide-wrapper'}):
    image = element.find(attrs={'class': 'winning-work-image'})
    caption = element.find(attrs={'class': 'ng-binding'})

    image_url = urljoin(base_url, image.get('src')) if image else None
    caption_text = caption.get_text(strip=True) if caption else None

    if image_url or caption_text:
        results.append({"image_url": image_url or "", "caption": caption_text or ""})

df = pd.DataFrame(results)
df.to_csv('dataFile.csv', index=False, encoding='utf-8')
print("data saved to a CSV file")

# Get the directory where scrapper.py is located
current_dir = Path(__file__).parent
#setup directory for images
output_dir = current_dir / "images"
output_dir.mkdir(parents=True, exist_ok=True)

for result in results:
    image_content = requests.get(result["image_url"]).content
    print(image_content)
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert("RGB")
    file_path = output_dir / (hashlib.sha1(image_content).hexdigest()[:10] + ".png")
    image.save(file_path, "PNG", quality=80)

print(f"'images' folder created at: {output_dir}")

driver.close()


#click on link
#get imageurl and caption info X, also get heading
#organize caption info fields
#download images to a folder X
#rename images 
#might need to manually solve each captcha



'''
#grab imageurl, caption info, heading
#organize information:
•	Date Awarded (Year only) - grab year from header
•	Photographer Name - in caption (/name) or header (*check if group award or not)
•	Photographer’s country of origin (if possible)
•	If Group Award, what group (e.g., Staff of Reuters, Staff of Associated Press) (check if name)
•	Location of where image was taken (city and country or just city).
•	News Outlet worked for (if applicable, e.g. Dallas Morning News, Associated Press, etc)  (in header after of)
•	Competition Category (e.g. Spot News, Breaking News, Feature Photography)
•	Caption

'''




# trying ###
# import asyncio
# import nodriver as uc

# async def main():
#     try:
#         browser = await uc.start()
#         if browser:
#             page = await browser.get('https://www.nowsecure.nl')
#             await page.save_screenshot()
#     finally:
#         if browser:
#             await browser.quit()  # Ensure proper shutdown

# if __name__ == '__main__':
#     asyncio.run(main())

import nodriver as uc
import time

async def main():

    browser = await uc.start(headless=True)
    page = await browser.get("https://www.nowsecure.nl")

    time.sleep(4)

    await page.save_screenshot("image.png")

if __name__ == "__main__":
    uc.loop().run_until_complete(main())

