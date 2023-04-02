import unittest


def load_json(filename) -> dict:
    import json
    with open(filename) as file:
        jsn = json.load(file)
        file.close()
    return jsn


class USDA_Nutrient_Mapper_DTO(unittest.TestCase):
    # Add the root directory to sys.path
    import sys
    from pathlib import Path
    file = Path(__file__).resolve()
    parent, root = file.parent, file.parents[1]
    sys.path.append(str(root))
    # Test the proper response from the USDA API

    def __init__(self):
        self.fdc_id = '1100856'

    def test_nutrients(self) -> None:
        from models import USDA_api_key
        from service.USDA_API_Service import USDA_API_Service
        from domain.USDA_Ingredient_Nutrient_Domain import USDA_Ingredient_Nutrient_Domain
        from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain
        nutrients = load_json('nutrient_data/new_nutrients.json')
        usda_ingredients = load_json('nutrient_data/new_usda_ingredients.json')
        imperial_units = [{'name': 'teaspoon', 'ounces': 0.166667}, {
            'name': 'tablespoon', 'ounces': 0.5}, {'ounces': 8.0, 'name': 'cup'}, {'name': 'oz', 'ounces': 1.0}]
        nutrient_usda_ids = [nutrient['usda_id'] for nutrient in nutrients if nutrient['id'] not in [
            'trans_fat', 'net_carb']]
        ingredient_data = USDA_API_Service(
            USDA_api_key=USDA_api_key).get_ingredient(fdc_id=self.fdc_id)

        nutrients_list = ingredient_data['foodNutrients']
        self.assertIsInstance(nutrients_list, list)

        for id in nutrient_usda_ids:
            self.assertIn(id, [str(nutrient['nutrient']['id'])
                          for nutrient in nutrients_list])
        for nutrient in nutrients_list:
            self.assertIsInstance(nutrient, dict)

        for usda_ingredient in usda_ingredients:
            fdc_id = usda_ingredient['fdc_id']
            usda_ingredient_id = usda_ingredient['id']
            usda_ingredient_name = usda_ingredient['name']
            usda_ingredient_data = USDA_API_Service(
                USDA_api_key=USDA_api_key).get_ingredient(fdc_id=fdc_id)

            mapped_usda_ingredient_data = USDA_Nutrient_Mapper_DTO(
                usda_ingredient_id=usda_ingredient_id, usda_ingredient_name=usda_ingredient_name, fdc_id=fdc_id, usda_ingredient_data=usda_ingredient_data, nutrients_list=nutrients, imperial_units=imperial_units)

            self.assertEqual(mapped_usda_ingredient_data.id,
                             usda_ingredient_id)
            self.assertEqual(mapped_usda_ingredient_data.name,
                             usda_ingredient_name)
            self.assertEqual(mapped_usda_ingredient_data.fdc_id, fdc_id)

            for nutrient in mapped_usda_ingredient_data.nutrients:
                self.assertIsInstance(
                    nutrient, USDA_Ingredient_Nutrient_Domain)
                self.assertIn(nutrient.nutrient_id, [
                              x['nutrient_id'] for x in nutrients])
            for portion in mapped_usda_ingredient_data.portions:
                self.assertIsInstance(portion, USDA_Ingredient_Portion_Domain)
