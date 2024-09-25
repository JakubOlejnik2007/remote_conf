from InquirerPy import inquirer
from InquirerPy.separator import Separator

from InputClass import Input
import validators as val
import serial.tools.list_ports

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

menu_options = [
    "COM",
    "SSH",
    "Exit"
]
ports = serial.tools.list_ports.comports()
available_ports = [port.device for port in ports]
while True:
    print(Separator())
    try:
        choice = inquirer.select(
            message="Choose connection type:",
            choices=menu_options,
        ).execute()
        print(f"Connection type: {choice}")

        print(Separator())
        if choice == menu_options[2]:
            break

        if choice == menu_options[0]:
            ports = serial.tools.list_ports.comports()
            available_ports = [port.device for port in ports]

            if(len(available_ports) == 0):
                raise WindowsError(f"[{bcolors.FAIL}!{bcolors.ENDC}] {bcolors.FAIL}No available COM ports found. Please check your connections.{bcolors.ENDC}")

            choice = inquirer.select(
                message="Choose available COM port:",
                choices=available_ports,
            ).execute()
            print(f"Port: {choice}")

        if choice == menu_options[1]:
            print(f"Give SSH connection details:")
            inputs_ssh = [
                Input(type="text", message="IP adress:", validateFunc=val.validate_ip, invalid_message="This is not a valid IP adress."),
                Input(type="number", message="Port:", validateFunc=val.validate_port, invalid_message="This is not a valid port.", default=22),
                Input(type="text", message="Username:", validateFunc=val.validate_username, invalid_message="This is not a valid username."),
                Input(type="secret", message="Password:", validateFunc=val.validate_password, invalid_message="This is not a valid password."),
            ]

            for input in inputs_ssh:
                input.callInput()

        print(Separator())

        execPasswordInput = Input(type="secret", message="EXEC Mode password:", validateFunc=val.validate_password, invalid_message="This is not a valid password.")
        execPasswordInput.callInput()

        inputs_mgmt = [
            Input(type="text", message="IP mgmt:", validateFunc=val.validate_ip,
                  invalid_message="This is not a valid IP adress."),
            Input(type="text", message="Mask mgmt:", validateFunc=val.validate_mask,
                  invalid_message="This is not a valid mask."),
            Input(type="text", message="Gateway mgmt:", validateFunc=val.validate_ip,
                  invalid_message="This is not a valid IP adress."),
            Input(type="text", message="Hostname:", validateFunc=val.validate_string,
                  invalid_message="This is not a valid password."),
        ]

        for input in inputs_mgmt:
            input.callInput()

        print(Separator())
    except WindowsError as e:
        print(e)
    except:
        print(f"Something went wrong")

