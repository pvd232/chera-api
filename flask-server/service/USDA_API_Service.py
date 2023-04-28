import requests


class USDA_API_Service(object):
    def __init__(self, USDA_api_key: str) -> None:
        self.usda_api_key = USDA_api_key

    def get_ingredient(self, fdc_id) -> dict:
        url = (
            f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={self.usda_api_key}"
        )

        nutrients_raw = requests.get(url=url)
        nutrients_json = nutrients_raw.json()
        return nutrients_json
