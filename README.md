# Scraping and MongoDB Models for Quotes and Authors

This repository contains Python scripts and MongoDB models for scraping quotes and author information from a website and storing them in a MongoDB database. The project is managed using the Poetry package manager. Here, I will provide an overview of the files and their purpose.

## Files

1. `main.py`: This script uses the Scrapy framework to scrape quotes and author information from the "http://quotes.toscrape.com/" website. It defines two Scrapy Items, `AuthorItem` and `QuoteItem`, to hold the scraped data. The scraped data is processed by the `QuotesPipline` class, which stores the quotes and author information in separate lists. After the spider finishes crawling, the collected data is saved as JSON files.

2. `filling_db.py`: This script contains the MongoDB models for storing the scraped quotes, authors, and contact information in the database. It uses the `mongoengine` library to define the document classes. The `Author` class represents author information, the `Quote` class represents quotes with references to authors, and the `Contact` class represents contact information.

3. `pyproject.toml`: The Poetry project file that specifies project dependencies, Python version, and other project-related metadata.

4. `poetry.lock`: The Poetry lock file that pins the exact versions of the dependencies.

## MongoDB Models

The MongoDB models are defined in `models.py` using the `mongoengine` library. Here's a summary of the models:

1. `Author` Model:
   - Fields: `fullname`, `born_date`, `born_location`, `description`
   - Collection Name: "authors"
   - Indexes: [("fullname", "born_date")]

2. `Quote` Model:
   - Fields: `tags`, `author`, `text`
   - Collection Name: "quotes"

3. `Contact` Model:
   - Fields: `fullname`, `email`, `phone`, `preferred_contact_method`, `logic_`
   - Collection Name: "contacts"

## Usage

To run the scraping script and populate the MongoDB database, follow these steps:

1. Ensure that you have MongoDB installed and running.
2. Install Poetry by following the installation instructions provided at https://python-poetry.org/docs/.
3. Open a terminal or command prompt and navigate to the project directory.
4. Run `poetry install` to install the project dependencies specified in `pyproject.toml`.
5. Set up a MongoDB connection by modifying the `connect` function call in `filling_db.py` with your own database credentials.
6. Run the scraping script by executing `poetry run python scrapy_quotes.py` in the terminal. This will initiate the scraping process and save the scraped data as JSON files.
7. After running the scraping script, execute `poetry run python filling_db.py` in the terminal to store the scraped data in the MongoDB database.

Feel free to explore and modify the scripts as needed for your specific use case.

Please note that this is a general overview of the files and their purpose. For more detailed information, refer to the comments within the code files.

If you have any questions or need further assistance, please don't hesitate to reach out.
