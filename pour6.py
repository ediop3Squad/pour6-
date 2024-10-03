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
        self.target_port = 80  # Default HTTP port
        self.username = None
        self.password = None
        self.wordlist = None  # Wordlist for brute force
        self.selected_module = None  # Currently selected module
        self.built_in_usernames = self.load_built_in_usernames()  # Built-in usernames
        self.built_in_passwords = self.load_built_in_passwords()  # Built-in passwords
        self.print_logo()
        self.command_loop()  # Start the interactive command loop

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
        """Load built-in usernames."""
        return ["admin", "user", "root", "guest", "admin1", "admin2", "test"]

    def load_built_in_passwords(self):
        """Load built-in passwords."""
        return ["password", "123456", "admin", "letmein", "welcome", "12345678", "qwerty"]

    def command_loop(self):
        """Start an interactive command loop."""
        while True:
            command = input("\n[pour6> ").strip().lower()  # Custom prompt
            if command == 'exit':
                print("Exiting...")
                break
            elif command == 'help':
                self.show_help()
            elif command.startswith('use'):
                _, module_name = command.split() if len(command.split()) > 1 else (None, None)
                if module_name:
                    self.select_module(module_name)
                else:
                    print("Module name is required. Usage: use <module>")
            elif command.startswith('exec'):
                _, shell_command, *args = command.split() if len(command.split()) > 1 else (None, None, None)
                if shell_command:
                    self.exec_command(shell_command, args)
                else:
                    print("Shell command is required. Usage: exec <shell_command> <args>")
            elif command.startswith('search'):
                _, search_term = command.split() if len(command.split()) > 1 else (None, None)
                if search_term:
                    self.search_module(search_term)
                else:
                    print("Search term is required. Usage: search <search_term>")
            elif command.startswith('scan'):
                self.scan_network()
            elif command.startswith('set target'):
                _, ip, *port = command.split()
                self.set_target(ip, int(port[0]) if port else 80)
            elif command.startswith('set wordlist'):
                _, filepath = command.split()
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
                _, option, value = command.split() if len(command.split()) > 2 else (None, None, None)
                if option and value:
                    self.set_option(option, value)
                else:
                    print("Option and value are required. Usage: set <option> <value>")
            elif command.startswith('check'):
                self.check_vulnerability()
            else:
                print("Unknown command. Type 'help' for options.")

    def show_help(self):
        """Show the help menu."""
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
            self.modules[self.selected_module]()  # Call the selected exploit
        else:
            print("No module selected.")

    def exec_command(self, shell_command, args):
        """Execute a shell command."""
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
        """Search for modules containing the search term."""
        print(f"Searching for modules containing: {search_term}")
        found_modules = [key for key in self.modules if search_term in key]
        if found_modules:
            print("Found modules:")
            for module in found_modules:
                print(module)
        else:
            print("No modules found.")

    def show_options(self):
        """Show options for the selected module."""
        if self.selected_module:
            print(f"Options for {self.selected_module}:")
            # OHOHOH
            print(" - target")
            print(" - username")
            print(" - password")
        else:
            print("No module selected.")

    def show_info(self):
        """Show info for the selected module."""
        if self.selected_module:
            print(f"Info for {self.selected_module}:")
            # LOL
            print("UHUHUH JUST RUN ON THE TARGETTTTTT after selecting the target ofc")
        else:
            print("No module selected.")

    def check_vulnerability(self):
        """Check if the target is vulnerable based on the selected module."""
        if self.selected_module:
            print(f"Checking vulnerability for {self.selected_module} on {self.target_ip}:{self.target_port}")
            # Here, you would implement vulnerability checking logic for the selected module.
            print("Vulnerability check complete.")
        else:
            print("No module selected.")

    def cisco_exploit(self):
        """Example exploit for Cisco routers."""
        print("Exploiting Cisco router...")
        # OHOH
        time.sleep(1)  # time delay for the exploit
        print("Cisco exploit completed.")

    def tplink_exploit(self):
        """Example exploit for TP-Link routers."""
        print("Exploiting TP-Link router...")
        # l
        time.sleep(1)  # fak yu
        print("TP-Link exploit completed.")

    def netgear_exploit(self):
        """LLLL"""
        print("Exploiting Netgear router...")
        # no
        time.sleep(1)  # lol
        print("Netgear exploit completed.")

    def dlink_exploit(self):
        """UHUHUHUH"""
        print("Exploiting D-Link router...")
        # YAAAA
        time.sleep(1)  # L
        print("D-Link exploit completed.")

    def zyxel_exploit(self):
        """LEOL."""
        print("Exploiting ZyXEL router...")
        # BUDY
        time.sleep(1)  # LOL :skull: :sob:
        print("ZyXEL exploit completed.")

    def linksys_exploit(self):
        """FAK U"""
        print("Exploiting Linksys router...")
        # NOOO
        time.sleep(1)  # UHUHUH
        print("Linksys exploit completed.")

if __name__ == "__main__":
    RouterExploitFramework()
