from .Base_Domain import Base_Domain


class FNCE_Lead_Domain(Base_Domain):
    def __init__(self, fnce_lead_json: dict) -> None:
        self.id: str = fnce_lead_json["id"]
        self.first_name: str = fnce_lead_json["first_name"]
        self.last_name: str = fnce_lead_json["last_name"]
        self.is_dietitian: str = fnce_lead_json["is_dietitian"]
        self.is_student: bool = fnce_lead_json["is_student"]
        self.description: str = fnce_lead_json["description"]
