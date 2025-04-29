import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False) -> dict:
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/GerrieStrongbow/0102cf2f72ec53c66279d35d3dbd5283/raw/99534156af0e0197a42a74c93270c3aa0be76fe2/gerhard-bekker-scrapein.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapein.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPEIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)

    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k not in ["certifications"]
    }

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/gerhard-bekker-a6867b14a/",
            mock=True,
        )
    )
