import sqlite3
import requests
from bs4 import BeautifulSoup
import time
import json

manga_name = input("Enter the name of manga or manhwa: ").lower().replace(" ", "-")
chapter_range = input("Enter a chapter range (e.g., 1, 10): ")
start, end = map(int, chapter_range.split(','))

conn = sqlite3.connect('manga_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS manga (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manga_name TEXT,
    chapter TEXT,
    chapter_url TEXT,
    image_url TEXT
    )
''')

# data = []


for chapter in range(start, end + 1):
    chapter_formatted = f"{chapter:03d}"  # Format chapter number with leading zeros
    chapter_url = f'https://www.mangasub.net/manga/{manga_name}/ch-{chapter_formatted}/'
    print(f"Fetching data for Chapter {chapter_formatted} from {chapter_url}")
    
    response = requests.get(chapter_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        content = soup.find('div', class_="reading-content")
        if content:
            image_urls = [img['src'].replace("\t\t\t\n\t\t\t", "") for img in content.find_all('img') if img.has_attr('src') and img['src'].strip()]
            # image_urls_str = ",".join(image_urls)
            image_urls_json = json.dumps(image_urls)
            try:
                cursor.execute('''
                    INSERT INTO manga (manga_name, chapter, chapter_url, image_url)
                    VALUES (?, ?, ?, ?)
                ''', (manga_name.replace("-", " "), chapter_formatted, chapter_url, image_urls_json))  
            except Exception as e:
                print(f"Error inserting data: {e}")
        time.sleep(1)
    else:
        print(f"Failed to fetch Chapter {chapter_formatted}: {response.status_code}")

conn.commit()
conn.close()

print("Data saved to the database successfully!")
