# Manga Scraper Project

This project scrapes manga data (image URLs) from a manga website and stores the images in an organized folder structure. The manga data is stored in an SQLite database, and images are downloaded and saved using Python scripts.

## Project Structure
```

├── Scrapper.ipynb                  # Jupyter notebook for scraping manga data
├── StoreImages.ipynb               # Jupyter notebook for storing images
├── manga_data.db                   # SQLite database storing manga data (name, chapter, image URLs)
├── manga_scrapper.py               # Python script to scrape manga data (single-threaded)
├── manga_scrapper_concurrent.py    # Python script to scrape manga data (multi-threaded)
├── sample.csv                      # Example CSV file with manga data (optional)
├── store_images.py                 # Python script to download and store images
└── structure.png                   # Visual representation of folder structure (optional)

```


## Features
- Download chapters as images or in bulk.
- Easy-to-use command line interface.
- Flexible and customizable to suit your needs.

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ajay1812/manga-scrapper.git
   cd manga-scrapper

2. **Create a Python virtual environment:** To create a virtual environment, use the following command:

#### Requirements

```
   pip install -r requirement.txt
```  

### Usage : Scraping Manga Data
1. Open Scrapper.ipynb in a Jupyter Notebook environment and run the cells to scrape manga data from the web.

2. Alternatively, you can use the following Python scripts to scrape manga data:

- manga_scrapper.py: A single-threaded version for scraping manga data.
- manga_scrapper_concurrent.py: A multi-threaded version for faster scraping.
To run either script:

```

python manga_scrapper.py
# or
python manga_scrapper_concurrent.py

```

### Storing Images
1. Open StoreImages.ipynb in a Jupyter Notebook and run the cells to download and store manga images in the folder structure.

2. Alternatively, you can run the store_images.py script to download images for all manga stored in the database:

```
python store_images.py
```

### Folder Structure for Images
Images for each manga and chapter will be stored in a folder structure like:

```

stored_manga/
    Naruto/
        chapter_001/
            naruto_ch001_001.jpg
            naruto_ch001_002.jpg
            ...
        chapter_002/
            ...
    OnePiece/
        chapter_001/
            ...

```

Each manga (e.g., Naruto, OnePiece) will have its folder, and inside each manga folder, each chapter will have its own subfolder.

### Example Data
Sample data for manga is stored in manga_data.db. You can also use the sample.csv to import data or create your own.
