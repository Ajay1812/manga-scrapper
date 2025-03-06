import os
import img2pdf

def convert_manga_to_pdf(manga_dir, output_dir):
    manga_name = os.path.basename(manga_dir.rstrip("/"))  
    manga_pdf_dir = os.path.join(output_dir, manga_name)  

    os.makedirs(manga_pdf_dir, exist_ok=True)
    print(f"Processing manga: {manga_name}")

    for chapter in sorted(os.listdir(manga_dir)):
        chapter_path = os.path.join(manga_dir, chapter)
        pdf_filename = os.path.join(manga_pdf_dir, f"{chapter}.pdf")

        if not os.path.isdir(chapter_path):
            continue  

        if os.path.exists(pdf_filename):
            print(f"PDF already exists for {chapter}, skipping...")
            continue
        
        print(f"Processing {chapter}")

        imgs = []
        for fname in sorted(os.listdir(chapter_path)):
            if fname.endswith(".jpg"):
                imgs.append(os.path.join(chapter_path, fname))

        if imgs:  
            with open(pdf_filename, "wb") as f:
                f.write(img2pdf.convert(imgs))
            print(f"PDF created: {pdf_filename}")
        else:
            print(f"No images found in {chapter_path}, skipping...")

base_dir = "./data/stored_manga/"
pdf_output_dir = "./data/stored_manga/pdfs/"

for manga in sorted(os.listdir(base_dir)):
    manga_path = os.path.join(base_dir, manga)
    if os.path.isdir(manga_path): 
        convert_manga_to_pdf(manga_path, pdf_output_dir)
