from pdf2image import convert_from_path
import pytesseract
import os
import re
import sqlite3
from  pyspark.sql import SparkSession

spark = SparkSession.builder.appName("text extract from pdf").getOrCreate()

def extract_text_ocr(pdf_path) -> str:
    images = convert_from_path(pdf_path)
    text = "\n".join([pytesseract.image_to_string(img) for img in images])
    return text

def clean_text(text) -> str:
    text = re.sub(r'[^A-Za-z0-9.,!?\'\"\n ]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)  # Reduce excessive newlines but keep paragraph breaks
    text = re.sub(r' +', ' ', text).strip()  # Normalize spaces
    return text

manga_dir = "./data/stored_manga/pdfs"
manga_names = [d for d in os.listdir(manga_dir) if os.path.isdir(os.path.join(manga_dir, d))]
# print(manga_names)
# exit(0)
for manga_name in manga_names:
    pdf_path = os.path.join(manga_dir, manga_name)
    # print(pdf_path)
    pdf_files = os.listdir(pdf_path)
    # print(pdf_files)
    # exit(0)

    pdf_files = [f for f in pdf_files if f.endswith('.pdf')]
    sorted_files = sorted(pdf_files, key=lambda x: int(x.split('_')[1].split('.')[0]))[1:2]

    # Connect to database
    conn = sqlite3.connect("manga_data.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(manga)")
    columns = [col[1] for col in cursor.fetchall()]
    if "extracted_text" not in columns:
        cursor.execute("ALTER TABLE manga ADD COLUMN extracted_text TEXT;")
        conn.commit()

    for file in sorted_files:
        chapter_name = file.replace(".pdf", "").replace("chapter_", "")  # Extract chapter number
        
        extracted_text = extract_text_ocr(os.path.join(pdf_path, file))
        cleaned_text = clean_text(extracted_text)

        # Check if the record exists before updating
        cursor.execute("SELECT COUNT(*) FROM manga WHERE manga_name = ? AND chapter = ?", (manga_name.replace('_', " "), chapter_name))
        count = cursor.fetchone()[0]

        if count > 0:
            cursor.execute("""
                UPDATE manga 
                SET extracted_text = ? 
                WHERE manga_name = ? AND chapter = ?""", (cleaned_text, manga_name.replace('_', " "), chapter_name))
            print(f"✅ Text inserted for {manga_name.replace('_', " ")}: Chapter - {chapter_name}")
        else:
            print(f"⚠️ No matching record for {manga_name.replace('_', " ")} - Chapter {chapter_name} in database.")

    conn.commit()
    conn.close()

print("Text extraction complete.")
