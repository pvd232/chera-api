from uuid import uuid4
from domain.USDA_Ingredient_Portion_Domain import USDA_Ingredient_Portion_Domain
from domain.USDA_Ingredient_Nutrient_Domain import USDA_Ingredient_Nutrient_Domain
from domain.Nutrient_Domain import Nutrient_Domain
from domain.Imperial_Unit_Domain import Imperial_Unit_Domain
from dto.USDA_Ingredient_Portion_DTO import USDA_Ingredient_Portion_DTO
from dto.USDA_Ingredient_Nutrient_DTO import USDA_Ingredient_Nutrient_DTO


def get_nutrients(nutrient_list: list[Nutrient_Domain], usda_ingredient_id: str, usda_nutrient_data: list[dict]):
    nutrients_to_return = []
    usda_nutrient_dict_by_id = {}
    for nutrient in usda_nutrient_data:
        usda_nutrient_dict_by_id[str(nutrient["nutrient"]
                                 ["id"])] = nutrient
    for nutrient in nutrient_list:
        if nutrient.id != "trans_fat" and nutrient.id != "net_carb" and nutrient.id != "vitamin_a" and nutrient.id != "vitamin_e":
            if nutrient.usda_id in usda_nutrient_dict_by_id:
                amount = usda_nutrient_dict_by_id.get(nutrient.usda_id)[
                    "amount"]
            else:
                amount = 0
            nutrient_dto = USDA_Ingredient_Nutrient_DTO(usda_ingredient_nutrient_json={
                "id": str(uuid4()),
                "usda_ingredient_id": usda_ingredient_id,
                "nutrient_id": nutrient.id,
                "amount": amount
            })
            nutrients_to_return.append(USDA_Ingredient_Nutrient_Domain(
                usda_ingredient_nutrient_object=nutrient_dto))
    # Then append trans fat
    trans_fat_dto = USDA_Ingredient_Nutrient_DTO(usda_ingredient_nutrient_json={"id": str(uuid4()),
                                                                                "name": nutrient.name,
                                                                                "usda_ingredient_id": usda_ingredient_id,
                                                                                "nutrient_id": "trans_fat",
                                                                                "amount": 0
                                                                                })
    nutrients_to_return.append(USDA_Ingredient_Nutrient_Domain(
        usda_ingredient_nutrient_object=trans_fat_dto))
    return nutrients_to_return


def get_portions(portion_list: list[dict], imperial_units: list[Imperial_Unit_Domain], usda_ingredient_id: str, usda_data_type: str) -> list[USDA_Ingredient_Portion_Domain]:
    portions_to_return: list[USDA_Ingredient_Portion_Domain] = []
    imperial_units_dict = {}
    for imperial_unit in imperial_units:
        imperial_units_dict[imperial_unit.id] = imperial_unit
    if usda_data_type == "Survey (FNDDS)":
        regular_non_metric_units_added = {}
        for portion in portion_list:
            fda_portion_id = portion["id"]
            portion_amount = portion["gramWeight"]
            usda_portion_description = portion["portionDescription"]
            non_metric_unit: str = usda_portion_description.split()[-1]
            is_non_specified_portion = usda_portion_description.find(
                'not specified')
            is_guideline_amount = usda_portion_description.find(
                'Guideline amount per')
            # Regular metric unit
            if non_metric_unit in imperial_units_dict:
                is_imperial = True
                new_portion_dto = USDA_Ingredient_Portion_DTO(usda_ingredient_portion_json={
                    "id": str(uuid4()),
                    "usda_ingredient_id": usda_ingredient_id,
                    "fda_portion_id": fda_portion_id,
                    "non_metric_unit": non_metric_unit,
                    "unit": "g",
                    "grams_per_non_metric_unit": portion_amount,
                    "portion_description": usda_portion_description,
                    "usda_data_type": usda_data_type,
                    "is_imperial": is_imperial
                }
                )
                new_usda_portion = USDA_Ingredient_Portion_Domain(
                    usda_ingredient_portion_object=new_portion_dto)
                portions_to_return.append(
                    new_usda_portion)
                regular_non_metric_units_added[non_metric_unit] = ""
            # Irregular units i.e. tortilla
            # All USDA ingredients have one portion that is "Quantity not specified" which is useless"
            elif is_non_specified_portion == -1 and is_guideline_amount == -1:
                non_metric_unit_to_add = non_metric_unit
                is_imperial = False
                should_add_unit = True
                for imperial_unit in imperial_units:
                    # Irregular units can still have the substring i.e. 1 cup of peanuts etc. inside the string
                    test_if_imperial = usda_portion_description.find(
                        imperial_unit.id)
                    # Substring exists
                    if test_if_imperial != -1:
                        is_imperial = True
                        non_metric_unit_to_add = imperial_unit.id

                        # If the substring has already been added, check if the new one is NFS, which is more accurate
                        if imperial_unit.id in regular_non_metric_units_added:
                            # Dont add a duplicate portion
                            should_add_unit = False
                            is_nfs_portion = usda_portion_description.find(
                                "NFS")
                            if is_nfs_portion != -1:
                                portion_to_update = [
                                    x for x in portions_to_return if x.non_metric_unit == imperial_unit.id][0]
                                portion_to_update.grams_per_non_metric_unit = portion_amount
                                portion_to_update.portion_description = usda_portion_description

                if should_add_unit:
                    if is_imperial:
                        regular_non_metric_units_added[non_metric_unit_to_add] = ""
                    else:
                        # If the unit isnt imperial then it is a non standard unit and should include all elements of the description except for the quantity i.e. 1 large tortilla
                        non_metric_unit_string_list = usda_portion_description.split()

                        # Remove the quantity
                        non_metric_unit_string_list.pop(0)

                        non_metric_unit_to_add = ' '.join(
                            non_metric_unit_string_list)
                    new_portion_dto = USDA_Ingredient_Portion_DTO(usda_ingredient_portion_json={
                        "id": str(uuid4()),
                        "usda_ingredient_id": usda_ingredient_id,
                        "fda_portion_id": fda_portion_id,
                        "non_metric_unit": non_metric_unit_to_add,
                        "unit": "g",
                        "grams_per_non_metric_unit": portion_amount,
                        "portion_description": usda_portion_description,
                        "usda_data_type": usda_data_type,
                        "is_imperial": is_imperial
                    }
                    )
                    new_usda_portion = USDA_Ingredient_Portion_Domain(
                        usda_ingredient_portion_object=new_portion_dto)
                    portions_to_return.append(
                        new_usda_portion)
    elif usda_data_type == "Foundation":
        for portion in portion_list:
            non_metric_unit_to_add = portion['measureUnit']['name']
            portion_amount = portion['gramWeight']
            fda_portion_id = portion["id"]
            usda_portion_description = ''
            if non_metric_unit_to_add in imperial_units_dict:
                is_imperial = True
            new_portion_dto = USDA_Ingredient_Portion_DTO(usda_ingredient_portion_json={
                "id": str(uuid4()),
                "usda_ingredient_id": usda_ingredient_id,
                "fda_portion_id": fda_portion_id,
                "non_metric_unit": non_metric_unit_to_add,
                "unit": "g",
                        "grams_per_non_metric_unit": portion_amount,
                        "portion_description": usda_portion_description,
                        "usda_data_type": usda_data_type,
                        "is_imperial": is_imperial
            }
            )
            portions_to_return.append(new_portion_dto)

    return portions_to_return


class USDA_Nutrient_Mapper_DTO(object):
    def __init__(self, usda_ingredient_id: str, usda_ingredient_name: str, fdc_id: str, usda_ingredient_data: list[dict], nutrients_list: list[Nutrient_Domain], imperial_units: list[Imperial_Unit_Domain]) -> None:
        if 'foodCode' in usda_ingredient_data:
            self.fda_identifier = usda_ingredient_data["foodCode"]
        else:
            self.fda_identifier = fdc_id
        self.usda_data_type = usda_ingredient_data["dataType"]
        self.usda_ingredient_id = usda_ingredient_id
        self.usda_ingredient_name = usda_ingredient_name
        self.fdc_id = fdc_id

        # Survey (FNDDS) and Foundation ingredients provide default values for 100 grams
        self.amount_of_grams = 100
        usda_nutrient_data = usda_ingredient_data['foodNutrients']

        usda_nutrient_dict_by_name = {}
        for nutrient in usda_nutrient_data:
            # Foundation food types will not have calories nor some nutrients
            usda_nutrient_dict_by_name[nutrient["nutrient"]
                                       ["name"]] = nutrient
            if 'Energy' in usda_nutrient_dict_by_name:
                self.calories = usda_nutrient_dict_by_name.get('Energy')[
                    "amount"]
            else:
                self.calories = 0
        self.calories_to_grams_ratio = self.calories / self.amount_of_grams

        self.nutrients = get_nutrients(
            nutrient_list=nutrients_list, usda_ingredient_id=self.usda_ingredient_id, usda_nutrient_data=usda_nutrient_data)

        vitamin_a = 0
        vitamin_a_rae_exists = usda_nutrient_dict_by_name.get('Vitamin A, RAE')
        if vitamin_a_rae_exists:
            vitamin_a = vitamin_a_rae_exists["amount"]
        else:
            vitamin_a_iu_exists = usda_nutrient_dict_by_name.get(
                "Vitamin A, IU")
            if vitamin_a_iu_exists:
                vitamin_a_iu = vitamin_a_iu_exists["amount"]
                vitamin_a = vitamin_a_iu * .3
        vitamin_a_dto = USDA_Ingredient_Nutrient_DTO(
            usda_ingredient_nutrient_json={
                "id": str(uuid4()),
                "usda_ingredient_id": self.usda_ingredient_id,
                "nutrient_id": "vitamin_a",
                "amount": vitamin_a
            }
        )
        self.nutrients.append(USDA_Ingredient_Nutrient_Domain(
            usda_ingredient_nutrient_object=vitamin_a_dto))
        vitamin_e = 0
        vitamin_e_exists = usda_nutrient_dict_by_name.get(
            "Vitamin E (alpha-tocopherol)")
        if vitamin_e_exists:
            vitamin_e_natural = usda_nutrient_dict_by_name.get(
                "Vitamin E (alpha-tocopherol)")["amount"]

            vitamin_e_added = usda_nutrient_dict_by_name.get("Vitamin E, added")[
                "amount"]

            vitamin_e = vitamin_e_natural + vitamin_e_added
        vitamin_e_dto = USDA_Ingredient_Nutrient_DTO(usda_ingredient_nutrient_json={
            "id": str(uuid4()),
            "usda_ingredient_id": self.usda_ingredient_id,
            "nutrient_id": "vitamin_e",
            "amount": vitamin_e
        }
        )
        self.nutrients.append(USDA_Ingredient_Nutrient_Domain(
            usda_ingredient_nutrient_object=vitamin_e_dto))

        self.portions: list[USDA_Ingredient_Portion_Domain] = []
        if 'foodPortions' in usda_ingredient_data:
            portions_data = usda_ingredient_data["foodPortions"]
            self.portions = get_portions(portion_list=portions_data, imperial_units=imperial_units,
                                         usda_ingredient_id=self.usda_ingredient_id, usda_data_type=self.usda_data_type)
        else:
            self.portions = []
