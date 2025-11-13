import subprocess, sys, re, os, subprocess

# This script audits your Mac OS configuration for common security configurations.

class SecurityAuditor:
    def __init__(self):
        self.results = []
        self.script_location = os.path.dirname(os.path.abspath(__file__))

    def run_mac_command(self, cmd):
        """ Execute Terminal command and return output"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # Combine stdout and stderr, or prioritize stderr if stdout is empty
            output = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
            return output
        except Exception as e:
            return f"Error: {e}"

    # Check firewall status
    def check_firewall_status(self):
        """ Check if firewall is enabled or not """
        print("\nChecking Firewall Status....")
        cmd = '/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate'
        result = self.run_mac_command(cmd)

        if "(State = 1)" in result:
            print("\tFirewall is ENABLED")
            self.results.append({"Firewall":"Enabled"})
        else:
            print("\tFirewall is DISABLED")
            self.results.append({"Firewall":"Disabled"})


    # Check if FileVault is enabled
    def check_filevault_status(self):
        """ Check if full disk encryption is enabled """
        print("\nChecking FileVault status...")
        cmd = "fdesetup status"
        result = self.run_mac_command(cmd)

        if "On" in result:
            print("\tFileVault is ENABLED")
            self.results.append({"FileVault":"Enabled"})
        else:
            print("\tFileVault is DISABLED")
            self.results.append({"FileVault":"Dissabled"})

    # Check if updates are availabe

    # Check password policy
    def check_pw_policy(self):
        """ Check password policy settings """
        print("\nChecking Password Policy...")

        # Check for policies
        cmd = '/usr/bin/pwpolicy -n /Local/Default -getaccountpolicies || echo "No global policy set"'

        result = self.run_mac_command(cmd)

        match = re.search(r'\.{(\d+),}', result) # Regex syntax for password policy

        if match:
            print(f"Password Policy found! Your minimum password length policy is:\n\t{match.group(1)} Characters")
            self.results.append({"PasswordPolicy":match.group(1)})
            if int(match.group(1)) < 8:
                print("This is a short password policy. Consider increasing your policy to passwords of 8 or more characters")
        else:
            print(f"ALERT! No password policy found.")
            self.results.append({"PasswordPolicy":"None"})

    # Check Gatekeeper is enabled
    def check_gatekeeper_status(self):
        """ Check if Gatekeeper is enabled on device """
        print("\nChecking Gatekeeper status...")
        cmd = 'spctl --status'
        result = self.run_mac_command(cmd)

        if 'enabled' in result:
            print("\tGatekeeper is ENABLED")
            self.results.append({"Gatekeeper":"Enabled"})
        else:
            print("\tALERT! Gatekeeper is DISABLED")
            self.results.append({"Gatekeeper":"Disabled"})


    # Check screen lock policy
    def check_screen_lock(self):
        """ Check if screen lock is enabled and if it has a password configured """
        print("\nChecking Screen Lock policies...")
        cmd = 'defaults -currentHost read com.apple.screensaver idleTime 2>&1' # check the amount of time for screen lock to start
        result_idle_time = self.run_mac_command(cmd)

        if 'does not exist' in result_idle_time:
            print("\tALERT! No screen lock policy enabled.")
        else:
            print(f"\tYour screen lock appears in {result_idle_time} seconds.")

    # Run all checks
    def run_audit(self):
        """ Run all security checks """
        print("Starting macOS Security Audit....\n")

        # Check if system is macOS
        if sys.platform != "darwin":
            print("This script only works for macOS.")
            return
                
        self.check_firewall_status()
        self.check_filevault_status()
        self.check_pw_policy()
        self.check_gatekeeper_status()
        self.check_screen_lock()

if __name__ == "__main__":
    auditor = SecurityAuditor()
    auditor.run_audit()