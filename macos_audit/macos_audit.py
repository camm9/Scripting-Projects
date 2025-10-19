import subprocess, sys

# This script audits your Mac OS configuration for common security configurations.

class SecurityAuditor:
    def __init__(self):
        self.results = []

    def run_mac_command(self, cmd):
        """ Execute Terminal command and return output"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
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

        # Check for global policies
        cmd = '/usr/bin/pwpolicy -n /Local/Default -getaccountpolicies || echo "No global policy set"'

        result = self.run_mac_command(cmd)

        
        
        # Check for local policies

        cmd = '/usr/bin/pwpolicy -n /Local/Default -getaccountpolicies '

        result = self.run_mac_command(cmd)



    # Check critical system file permissions -- /etc/passwd /etc/shadow /etc/sudoers /var/log

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

if __name__ == "__main__":
    auditor = SecurityAuditor()
    auditor.run_audit()