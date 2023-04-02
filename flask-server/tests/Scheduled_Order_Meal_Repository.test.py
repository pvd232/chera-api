from uuid import uuid4, UUID
# Add the root directory to sys.path
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from test_base.Base_Repository import Base_Repository

class Scheduled_Order_Meal_Repository(Base_Repository):
    def get_upcoming_scheduled_order_meals(self) -> None:
        from repository.Scheduled_Order_Meal_Repository import Scheduled_Order_Meal_Repository
        scheduled_order_meals = Scheduled_Order_Meal_Repository(db=self
                                                                ).get_upcoming_scheduled_order_meals(meal_subscription_id=uuid4())
        self.assertEqual(scheduled_order_meals, None)
        self.tearDown()
    def get_scheduled_order_meals(self):
        from repository.Scheduled_Order_Meal_Repository import Scheduled_Order_Meal_Repository
        s_c = Scheduled_Order_Meal_Repository(db=self).get_scheduled_order_meals()
        self.assertIsInstance(s_c, list)
        self.tearDown()
        
        
    def update_home_page_scheduled_order_meals(self) -> None:
        from repository.Scheduled_Order_Meal_Repository import Scheduled_Order_Meal_Repository
        from domain.Scheduled_Order_Meal_Domain import Scheduled_Order_Meal_Domain
        
        # Substitute a subscription id from postman MealSubscriptionInvoice collection
        meal_subscription_id = UUID("60467dab-aa3a-4970-88e7-1f3554375475")
        current_scheduled_order_meals_map = {}
        updated_scheduled_order_meals_map = {}
        
        # Create a map of the current scheduled order meals
        current_scheduled_order_meals = [Scheduled_Order_Meal_Domain(scheduled_order_meal_object = x,schedule_meal_object=None,scheduled_order_meal_id=None,delivery_date=None,is_paused=None) for x in Scheduled_Order_Meal_Repository(db=self).get_upcoming_scheduled_order_meals(meal_subscription_id=meal_subscription_id)]
        self.assertEqual(len(current_scheduled_order_meals), 24)
        # Mock one new updated scheduled order meal
        updated_scheduled_order_meals = []
        for x in current_scheduled_order_meals:
            updated_scheduled_order_meals.append(x)
            
        new_scheduled_order_meal = Scheduled_Order_Meal_Domain(scheduled_order_meal_object = current_scheduled_order_meals[0],schedule_meal_object=None,scheduled_order_meal_id=None,delivery_date=None,is_paused=None)
        new_scheduled_order_meal.id = uuid4()
        updated_scheduled_order_meals.append(new_scheduled_order_meal)
        updated_scheduled_order_meals.remove(updated_scheduled_order_meals[5])
        for current_scheduled_order_meal in current_scheduled_order_meals:
            current_scheduled_order_meals_map[str(
                current_scheduled_order_meal.id)] = ""                    
        
        # Error presented was adding multiple scheduled order meals with the same id
        for updated_scheduled_order_meal in updated_scheduled_order_meals:
            updated_scheduled_order_meals_map[str(
                updated_scheduled_order_meal.id)] = "" 
        for updated_scheduled_order_meal in updated_scheduled_order_meals:
            # If the updated scheduled order meal is not in the current scheduled order meals map, then it is a new scheduled order meal
            if str(updated_scheduled_order_meal.id) not in current_scheduled_order_meals_map:                
                pass                
            # Otherwise, it is an unchanged existing scheduled order meal and is removed from the current scheduled order meals map
            else:
                current_scheduled_order_meals_map.pop(
                    str(updated_scheduled_order_meal.id))
                updated_scheduled_order_meals_map.pop(str(updated_scheduled_order_meal.id))
        # There should be one remaining scheduled order meal in the updated map, as all the others were already present
        self.assertEqual(len(updated_scheduled_order_meals_map.keys()), 1, msg="updated_scheduled_order_meals_map: {}".format(updated_scheduled_order_meals_map))
        self.assertEqual(len(current_scheduled_order_meals_map.keys()), 1, msg="current_scheduled_order_meals_map: {}".format(current_scheduled_order_meals_map))
        self.tearDown()
        
        


Scheduled_Order_Meal_Repository().get_upcoming_scheduled_order_meals()
Scheduled_Order_Meal_Repository().update_home_page_scheduled_order_meals()
