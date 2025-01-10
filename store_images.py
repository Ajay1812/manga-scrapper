import os
import sqlite3
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def download_image(image_url, chapter_folder):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        file_name = os.path.basename(urlparse(image_url).path)
        image_path = os.path.join(chapter_folder, file_name)

        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Downloaded: {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_url}: {e}")

def process_chapter(manga_name, chapter, image_urls):
    stored_manga_folder = os.path.join("../../stored_manga")
    os.makedirs(stored_manga_folder, exist_ok=True)

    manga_folder = os.path.join(stored_manga_folder, manga_name)
    os.makedirs(manga_folder, exist_ok=True)

    chapter_folder = os.path.join(manga_folder, f"chapter_{chapter:03d}")
    os.makedirs(chapter_folder, exist_ok=True)
    print(f"Downloading images for {manga_name} Chapter {chapter}...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(lambda url: download_image(url, chapter_folder), image_urls)

def fetch_and_download():
    conn = sqlite3.connect('manga_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT manga_name, chapter, image_url FROM manga")
    rows = cursor.fetchall()

    for row in rows:
        manga_name = row[0].replace(" ", "_")
        chapter = int(row[1])
        image_urls = eval(row[2])
        process_chapter(manga_name, chapter, image_urls)

    conn.close()
    print("All images downloaded successfully!")

if __name__ == "__main__":
    fetch_and_download()
