import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import json
from concurrent.futures import ThreadPoolExecutor

def logger():
  timestamp


def fetch_chapter_data(manga_name, chapter, db_lock):
    chapter_formatted = f"{chapter:03d}"  # Format chapter number with leading zeros
    chapter_url = f'https://www.mangasub.net/manga/{manga_name}/ch-{chapter_formatted}/'
    print(f"Fetching data for {manga_name.replace('-', ' ')} Chapter {chapter_formatted} from {chapter_url}")
    
    response = requests.get(chapter_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', class_="reading-content")
        if content:
            image_urls = [img['src'].strip() for img in content.find_all('img') if img.has_attr('src') and img['src'].strip()]
            image_urls_json = json.dumps(image_urls)
            
            # Use the lock to safely write to the database
            with db_lock:
                cursor.execute('''
                    INSERT INTO manga (manga_name, chapter, chapter_url, image_url)
                    VALUES (?, ?, ?, ?)
                ''', (manga_name.replace("-", " "), chapter_formatted, chapter_url, image_urls_json))
    else:
        print(f"Failed to fetch {manga_name.replace('-', ' ')} Chapter {chapter_formatted}: {response.status_code}")

def main():
    manga_names = input("Enter the names of manga or manhwa (comma-separated): ").split(",")
    manga_names = [name.strip().lower().replace(" ", "-") for name in manga_names]

    chapter_range = input("Enter a chapter range (e.g., 1, 10): ")
    start, end = map(int, chapter_range.split(','))

    conn = sqlite3.connect('manga_data.db', check_same_thread=False)
    global cursor
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS manga (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manga_name TEXT,
        chapter TEXT,
        chapter_url TEXT,
        image_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    from threading import Lock
    db_lock = Lock()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for manga_name in manga_names:
            for chapter in range(start, end + 1):
                futures.append(executor.submit(fetch_chapter_data, manga_name, chapter, db_lock))
        
        for future in futures:
            future.result()

    conn.commit()
    conn.close()

    print("Data saved to the database successfully!")

if __name__ == "__main__":
    main()
