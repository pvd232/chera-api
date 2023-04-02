import unittest


def load_json(filename) -> dict:
    import json
    with open(filename) as file:
        jsn = json.load(file)
        file.close()
    return jsn


class USDA_API_Service_Test(unittest.TestCase):
    # Add the root directory to sys.path
    import sys
    from pathlib import Path
    file = Path(__file__).resolve()
    parent, root = file.parent, file.parents[1]
    sys.path.append(str(root))
    # Test the proper response from the USDA API

    def __init__(self):
        self.fdc_id = '1100856'

    def get_ingredient(self) -> dict:
        from service.USDA_API_Service import USDA_API_Service
        from models import USDA_api_key

        ingredient_data = USDA_API_Service(
            USDA_api_key=USDA_api_key).get_ingredient(fdc_id=self.fdc_id)

        self.assertIsInstance(ingredient_data, dict)


USDA_API_Service_Test().get_ingredient()
