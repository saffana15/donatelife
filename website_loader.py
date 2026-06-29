import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.donatelife.org.in/"


def get_website_content():

    try:

        response = requests.get(
            BASE_URL,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # remove unwanted tags
        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer"
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:12000]

    except Exception as e:

        return (
            f"Website unavailable: {e}"
        )