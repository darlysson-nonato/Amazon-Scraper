# Amazon Scraper

This Python script scrapes Amazon for product offers, filtering by a specified discount percentage. It uses ScraperAPI to bypass Amazon's bot protection.

## Features

- Search for products by title and category.
- Scrape multiple pages of search results.
- Filter results by discount percentage.
- Save offers to a JSON file.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- A valid ScraperAPI key

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/darlysson-nonato/amazon-scraper.git
    ```

2. Navigate into the project directory:
    ```bash
    cd amazon-scraper
    ```

3. Install the necessary libraries using the provided `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set up your configuration in `config.json`.
2. Run the script:
    ```bash
    python scraper.py
    ```

3. Follow the prompts to input the title, category, and discount threshold.

## Configuration

The script uses a `config.json` file to store the ScraperAPI key, Amazon's mk_pt_BR code, search parameters, and the currency symbol.

### Example `config.json`:

```json
{
    "scraperapi_key": "your_scraperapi_key",
    "__mk_pt_BR": "ÅMÅŽÕÑ",
    "search_params": {
        "base_url": "https://www.amazon.com.br/",
        "ref_number": "2",
        "num_pages": 5
    },
    "currency_symbol": "R$"
}
