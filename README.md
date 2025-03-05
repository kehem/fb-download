A Python package to scrape video and reel information from Facebook. This tool allows you to easily retrieve details such as video title, description, URL, and other metadata associated with Facebook videos or reels.

## Features

- Scrape video data from Facebook videos and reels.
- Extract video metadata like title, description, views, and more.
- Simple and easy-to-use Python interface.
- Supports scraping using direct video URLs.
- Command-line interface (CLI) for quick usage.

## Installation

You can install the package from PyPI using the following command:

```bash
pip install fb-video
```
## Requirements
- Python 3.6 or higher.

- The requests and beautifulsoup4 libraries (these will be installed automatically during installation).

## Usage
You can use the Facebook Video Scraper in two ways: through Python code or via the command line interface (CLI).

## Python Code Usage
You can integrate the scraper into your Python project and extract video details by using the following code:
```python

from fb_video import FacebookVideoScraper

# Initialize the scraper
scraper = FacebookVideoScraper()

# Replace with the URL of the Facebook video you want to scrape
url = "https://www.facebook.com/video_url"

# Scrape the video information
info = scraper.get_video_info(url)

# Output the video information
print(info)
```

The get_video_info() function will return a dictionary with various pieces of metadata related to the video, such as:
Title: The title of the video.

- Description: The description of the video.

- Video URL: Direct link to the video.

- Views: The number of views on the video.

- Upload Date: The date the video was uploaded.

## Command Line Interface (CLI)
You can also run the scraper directly from the command line by using the following command:
```bash

python fb-video.py --url https://www.facebook.com/video_url
```

This command will output the video details directly to the console.

## Example Output
When you run the scraper, you will get a structured output like this:

```json
{
  "url": "https://www.facebook.com/video_url",
  "duration_ms": 926766,
  "sd": "https://www.facebook.com/sd_downloadable_link",
  "hd": "https://www.facebook.com/hd_downloadable_link",
  "title": "",
  "thumbnail": "https://www.facebook.com/thumbnail_link"
}

```

## Troubleshooting

### Error: Invalid URL
Ensure that the URL provided is a valid Facebook video or reel URL. The scraper currently only supports public videos. Double-check the link format (e.g., `https://www.facebook.com/video_url`) and confirm the video is accessible without restrictions.

### Error: Permission Denied
If you're unable to access a video, it may be restricted (e.g., private, friends-only, or region-locked) or require login credentials. This scraper does not support private videos or those needing authentication. Use a public video URL to resolve this issue.

### Error: Missing Dependencies
If the package fails to install properly, required dependencies might be missing. Ensure you have Python 3.6+ installed, then run the following command to install necessary libraries:

## Contributing

We welcome contributions to the Facebook Video Scraper! To contribute, please follow these steps:

1. **Fork this repository**  
   Create your own copy of the project by forking it on GitHub.

2. **Clone your fork to your local machine**  
   Download your forked repository to work on it locally using `git clone`.

3. **Create a new branch for your feature or bugfix**  
   Use a descriptive branch name, e.g., `git checkout -b feature/add-new-scraper`.

4. **Make your changes and commit them**  
   Implement your updates and commit with clear messages, e.g., `git commit -m "Add support for reel scraping"`.

5. **Push to your fork and submit a pull request**  
   Push your branch to your forked repository and open a pull request against the main project.

Before submitting, ensure your code passes existing tests. If you're adding new features, please consider including corresponding tests to maintain project quality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.