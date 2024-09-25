from InquirerPy import inquirer
from InquirerPy.separator import Separator
from netmiko import ConnectHandler

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

        switch = {}

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

            print(Separator())
            execPasswordInput = Input(type="secret", message="EXEC Mode password\n(Enter if not present):", validateFunc=val.validate_password,
                                      invalid_message="This is not a valid password.")
            execPasswordInput.callInput()

            switch = {
                'device_type': 'cisco_ios_serial',
                'serial_settings': {
                    'port': choice,
                    'baudrate': 9600,
                },
                'username': '',
                'password': '',
                'secret': execPasswordInput.value,
            }

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
            execPasswordInput = Input(type="secret", message="EXEC Mode password\n(Enter if not present):", validateFunc=val.validate_password,
                                      invalid_message="This is not a valid password.")
            execPasswordInput.callInput()

            switch = {
                'device_type': 'cisco_ios',
                'host': inputs_ssh[0].value,
                'port': inputs_ssh[1].value,
                'username': inputs_ssh[2].value,
                'password': inputs_ssh[3].value,
                'secret': execPasswordInput.value,
            }



        # all
        inputs_mgmt = [
            # Input(type="text", message="Hostname:", validateFunc=val.validate_hostname,
            #       invalid_message="This is not a valid password."),
            # Input(type="text", message="IP mgmt:", validateFunc=val.validate_ip,
            #       invalid_message="This is not a valid IP adress."),
            # Input(type="text", message="Mask mgmt:", validateFunc=val.validate_mask,
            #       invalid_message="This is not a valid mask."),
            # Input(type="text", message="Gateway mgmt:", validateFunc=val.validate_ip,
            #       invalid_message="This is not a valid IP adress."),
        ]

        #
        inputs_add_vlan = [
            Input(type="number", message="VLAN number:", validateFunc=val.validate_vlan_number,
                  invalid_message="This is not a valid VLAN number."),
            Input(type="text", message="VLAN name:", validateFunc=val.validate_vlan_name,
                  invalid_message="This is not a valid VLAN name."),
        ]

        for input in inputs_add_vlan:
            input.callInput()

        print(Separator())

        print(f"{bcolors.WARNING} Establishing connection...{bcolors.ENDC}")

        net_connect = ConnectHandler(**switch)

        if switch['secret']:
            net_connect.enable()

        # commands = [
        #     f'hostname {inputs_mgmt[0].value}',
        #     'exit',
        #     'write memory'
        # ]

        commands = [
            f'Vlan {inputs_add_vlan[0].value}',
            f'Name {inputs_add_vlan[1].value}',
            'exit'
        ]

        output = net_connect.send_config_set(commands)
        print(f"{bcolors.WARNING} Operation results:{bcolors.ENDC}")
        print(output)

        net_connect.disconnect()
    except WindowsError as e:
        print(e)
    except Exception as e:
        print(f"Something went wrong {e}")

