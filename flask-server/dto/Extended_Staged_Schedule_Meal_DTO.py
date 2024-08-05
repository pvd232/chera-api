from dto.Staged_Schedule_Meal_DTO import Staged_Schedule_Meal_DTO
from dto.Extended_Meal_DTO import Extended_Meal_DTO
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.Extended_Staged_Schedule_Meal_Domain import (
        Extended_Staged_Schedule_Meal_Domain,
    )


class Extended_Staged_Schedule_Meal_DTO(Staged_Schedule_Meal_DTO):
    def __init__(
        self,
        extended_staged_schedule_meal_domain: Optional[
            Extended_Staged_Schedule_Meal_Domain
        ] = None,
    ) -> None:
        super().__init__(
            staged_schedule_meal_domain=extended_staged_schedule_meal_domain
        )
        self.associated_meal = Extended_Meal_DTO(
            extended_meal_domain=extended_staged_schedule_meal_domain.associated_meal
        )
