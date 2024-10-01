import json
import validators as val
from typing import List

from InputClass import Input

class jsonInputControl:
    def __init__(self, id, type, message, invalid_message):
        self.id = id
        self.control = None

        if type == "text":
            self.control = Input(type="text", validateFunc=val.validate_string, message=message, invalid_message=invalid_message)
        elif type == "vlan_number":
            self.control = Input(type="text", validateFunc=val.validate_vlan_number, message=message, invalid_message=invalid_message)
        elif type == "vlan_name":
            self.control = Input(type="text", validateFunc=val.validate_vlan_name, message=message, invalid_message=invalid_message)
        elif type == "ip_address":
            self.control = Input(type="text", validateFunc=val.validate_ip, message=message, invalid_message=invalid_message)
        elif type == "mask":
            self.control = Input(type="text", validateFunc=val.validate_mask, message=message, invalid_message=invalid_message)


class Operation:
    def __init__(self, name, controls, commands: List[str]):
        self.name = name
        self.commands = commands
        self.controls = []

        for index, control in enumerate(controls):
            self.controls.append(jsonInputControl(control["id"], control["type"], control["message"], control["invalid_message"]))

def getDataFromJSON(jsonPath="commands.json"):
    operations = []
    with open(jsonPath, 'r', encoding='utf-8') as jsonFile:
        dane = json.load(jsonFile)["all_commands"]
        for operation in dane:
            operations.append(Operation(operation["name"], operation["controls"], operation["commands"]))
    return operations