from google import genai
import urllib.request
from inscriptis import get_text
from bs4 import BeautifulSoup
import csv
from util.logger import logger

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

PROMPT_PREFIX = """Generate as many question answer pairs from the following text as possible.Generate question from every part of the text. The questions should cover the entire text. The answers should be professional. The text is from a website and the question answer will be used for frequently asked question section of the website. The questions should be from the perspective of site visitor and the answer from the perspective of the website owner. Return the questions and answers in json format. The text is as follows:\n\n"""

API_KEY = "AIzaSyB4UDAr3O36su6ZERrPBpScHwl4-bOksdU"
MODEL = "gemini-2.0-flash"


def collectFromWeb(url):
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")  # Read and decode the response

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Remove unwanted elements from the <body>
        for tag in soup.body(["header", "footer", "script", "style"]):
            tag.decompose()  # Removes the tag completely

        # Function to check if an element has meaningful content
        def has_content(tag):
            return tag.get_text(strip=True) != ""

        # Remove empty elements (tags with no meaningful text)
        for tag in soup.body.find_all():
            if not has_content(tag):
                tag.decompose()

        # Get the cleaned body HTML
        cleaned_body_html = soup.body.prettify()

        text = get_text(cleaned_body_html)

        qna_csv = generate_qna_csv(PROMPT_PREFIX + text)

        return qna_csv

    except urllib.error.HTTPError as e:
        logger.error(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        logger.error(f"URL Error: {e.reason}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


def generate_qna_csv(text):
    try:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model=MODEL, contents=text
        )

        lines = response.text.split('\n')
        return '\n'.join(lines[1:-1])
    except genai.exceptions.ApiError as e:
        logger.error(f"API Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":

    # Usage
    url = "https://hummbell.com"
    output_file = './output.txt'

    text = scrape_web(url)
    qa = generate_qna_csv(PROMPT_PREFIX + text)
    with open(output_file, 'w') as file:
        file.write(qa)
