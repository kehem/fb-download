# Facebook Scraper
A Python package to scrape video information from Facebook.

## Installation
```bash
pip install facebook-scraper
```
## Usage
```bash
fb-scraper --url "https://www.facebook.com/watch/?v=971981951549911"
```

**Build the Package**
```bash
# Install build tools if not already installed
pip install --upgrade pip setuptools wheel

# Navigate to the facebook-scraper directory
cd facebook-scraper

# Build the package
python setup.py sdist bdist_wheel
```
**Install Locally (Optional)**
```bash
# Install twine if not already installed
pip install twine

# Upload to PyPI (you'll need a PyPI account)
twine upload dist/*
```
## Usage After Installation
```bash
# Run directly
fb-scraper --url "https://www.facebook.com/watch/?v=971981951549911"

# Or use in Python
from facebook_scraper import FacebookVideoScraper
scraper = FacebookVideoScraper()
info = scraper.get_video_info("https://www.facebook.com/watch/?v=971981951549911")
print(info.to_dict())
```

