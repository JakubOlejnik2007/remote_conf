from InquirerPy import inquirer
from setuptools.config.pyprojecttoml import validate


class Input:
    def __init__(self, type, message, validateFunc, invalid_message, default="", choices=None):
        if choices is None:
            choices = []
        self.validateFunc = validateFunc
        self.message = message
        self.type = type
        self.invalid_message = invalid_message
        self.value = ""
        self.default = default
        self.choices = choices

    def callInput(self):
        if self.type == "text":
            self.value = inquirer.text(
                message=self.message,
                default=self.default,
                invalid_message=self.invalid_message,
                validate=lambda result: self.validateFunc(result)
            ).execute()
        elif self.type == "number":
            self.value = inquirer.number(
                message=self.message,
                default=lambda result: self.default,
                invalid_message=self.invalid_message,
                validate=lambda result: self.validateFunc(result)
            ).execute()
        elif self.type == "secret":
            self.value = inquirer.secret(
                message=self.message,
                default=lambda result: self.default,
                invalid_message=self.invalid_message,
                validate=lambda result: self.validateFunc(result)
            ).execute()