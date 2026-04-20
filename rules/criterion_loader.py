import json
from models.file_record import FileRecord
from helpers.operators import ops


class CriterionLoader:

    def __init__(self, json_file):
        self.json_file = json_file
        self.criteria = self.load_criteria()

    def load_criteria(self):
        with open(self.json_file, 'r') as file:
            return json.load(file)

    def verify_criteria(self, file_record: FileRecord):

        for criterion in self.criteria["criteria"]:
            if len(criterion["properties"]) > 1:
                if not self.check_multiple_criteria(criterion, file_record):
                    return False
            else:
                if not self.check_single_criterion(criterion, file_record):
                    return False

        return True

    def get_property_value(self, file_record: FileRecord, property_name: str):

        file_value = getattr(file_record, property_name, None)

        if file_value is None:
            file_value = file_record.metadata.get(property_name)

        return file_value

    def check_multiple_criteria(self, criterion, file_record: FileRecord):

        property_value = self.get_property_value(file_record, criterion["properties"][0])

        if property_value is None:
            return False

        for i in range(1, len(criterion["properties"])):
            operator = criterion["operations"][i-1]
            value = self.get_property_value(file_record, criterion["properties"][i])

            if value is None:
                return False

            property_value = ops[operator](property_value, value)

        comparison_operator = criterion["operations"][-1]

        for value in criterion["values"]:
            if ops[comparison_operator](property_value, value):
                return True

        return False

    def check_single_criterion(self, criterion, file_record: FileRecord):
        property_name = criterion["properties"][0]
        operator = criterion["operations"][0]
        values = criterion["values"]

        file_value = self.get_property_value(file_record, property_name)

        if file_value is None:
            return False

        for value in values:
            if ops[operator](file_value, value):
                return True

        return False