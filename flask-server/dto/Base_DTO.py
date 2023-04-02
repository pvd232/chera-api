from uuid import UUID
from datetime import datetime, date, timezone


class Base_DTO(object):
    def serialize(self) -> dict:
        attribute_names: list[str] = list(self.__dict__.keys())
        attributes: list = list(self.__dict__.values())
        serialized_attributes: dict = {}
        for i in range(len(attributes)):
            # Catch and stringify unserializable data types
            if isinstance(attributes[i], UUID):
                serialized_attributes[attribute_names[i]] = str(attributes[i])
            elif isinstance(attributes[i], datetime):
                serialized_attributes[attribute_names[i]
                                      ] = attributes[i].replace(tzinfo=timezone.utc).timestamp()
            elif isinstance(attributes[i], date):
                serialized_attributes[attribute_names[i]
                                      ] = attributes[i].strftime("%s")
            elif isinstance(attributes[i], Base_DTO):
                serialized_attributes[attribute_names[i]
                                      ] = attributes[i].serialize()
            else:
                serialized_attributes[attribute_names[i]] = attributes[i]
        return serialized_attributes
