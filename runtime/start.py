#!/usr/bin/env python2
import os
import platform
import subprocess
import sys

# Global variable to determine if we should use sudo or not
USE_SUDO = False

def check_root():
    """ Check if the user has root privileges. """
    global USE_SUDO
    if platform.system() != 'Windows':
        if os.geteuid() == 0:
            USE_SUDO = True
            print("You are running the script as root. Sudo will be used where necessary.")
        else:
            USE_SUDO = False
            print("Warning: You are not running as root. Some commands might fail if they require elevated privileges.")

def run_command(cmd, use_sudo=False):
    """ Run a command with optional sudo and handle errors """
    if use_sudo and platform.system() != 'Windows':
        cmd = ['sudo'] + cmd  # Prepend sudo for Linux/macOS if needed

    try:
        subprocess.check_call(cmd)  # Remove shell=True for list commands
    except subprocess.CalledProcessError as e:
        print("Error running command: {}".format(e))
        return False  # Return False if the command fails
    return True  # Return True if the command is successful

def change_java_path():
    """ Change the Java path to Java 8 """
    confirm = raw_input("Do you want to change the Java path to Java 8? (yes/no): ").strip().lower()
    if confirm == 'yes':
        if platform.system() == 'Windows':
            os.system('setx JAVA_HOME "C:\\Program Files\\Java\\jdk1.8.0_281"')
            os.system('setx PATH "%PATH%;%JAVA_HOME%\\bin"')
        else:
            print("Adding JAVA_HOME to the current session...")
            os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64'
            os.environ['PATH'] = '{}:{}'.format(os.environ['JAVA_HOME'] + '/bin', os.environ['PATH'])
            print("To make this change permanent, add the following lines to your shell configuration file:")
            print('export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"')
            print('export PATH="$JAVA_HOME/bin:$PATH"')
        print("Java path changed to Java 8 successfully!")
    else:
        print("Java path change skipped.")

def install_java_8():
    """ Install Java 8 and fix broken dependencies if needed """
    print("Attempting to install Java 8...")
    if not run_command(['apt', 'update'], use_sudo=True):  # Update package list
        return  # If this fails, exit the function
    if not run_command(['apt', 'install', '-y', 'default-jre', 'openjdk-8-jdk'], use_sudo=True):  # Install Java 8
        print("Error: Unmet dependencies while trying to install Java 8. Attempting to fix broken installs...")
        run_command(['apt', '--fix-broken', 'install'], use_sudo=True)  # Fix broken installs

def download_legacy_launcher():
    """ Download and install the LegacyLauncher using wget for Linux/macOS and PowerShell for Windows """
    confirm = raw_input("Do you want to install the LegacyLauncher for Minecraft testing? (yes/no): ").strip().lower()
    if confirm == 'yes':
        if platform.system() == 'Windows':
            url = 'https://llaun.ch/repo/downloads/LegacyLauncher_Installer_legacy.exe'
            file_name = 'LegacyLauncher_Installer_legacy.exe'
            
            # Use PowerShell to download the file
            powershell_command = (
                "powershell -Command \"Invoke-WebRequest -Uri '{}' -OutFile '{}'\"".format(url, file_name)
            )
            try:
                print("Downloading LegacyLauncher using PowerShell from {}".format(url))
                run_command(powershell_command)  # Run PowerShell command to download the file
                print("Download complete.")
                
                # Install the launcher on Windows
                print("Running installer...")
                os.startfile(file_name)  # This works for launching .exe files in Windows
                print("LegacyLauncher installed successfully!")
            except Exception as e:
                print("Error during installation: {}".format(e))
        
        elif platform.system() == 'Linux':
            url = 'https://llaun.ch/repo/downloads/TL_legacy.deb'
            file_name = 'TL_legacy.deb'

            # Use wget to download the file
            try:
                print("Downloading LegacyLauncher using wget from {}".format(url))
                run_command(['wget', '-O', file_name, url])  # Use wget on Linux
                print("Download complete.")

                # Verify that the file was downloaded
                if not os.path.exists(file_name):
                    print("Error: Downloaded file not found.")
                    return

                # Install the launcher on Linux
                if run_command(['sudo', 'dpkg', '-i', file_name]):  # Install the .deb package
                    print("LegacyLauncher installed successfully!")
                else:
                    print("Failed to install LegacyLauncher due to dependency issues.")
            except Exception as e:
                print("Error during installation: {}".format(e))
        
        elif platform.system() == 'Darwin':  # macOS
            url = 'https://llaun.ch/repo/downloads/TL_legacy.dmg'
            file_name = 'TL_legacy.dmg'

            # Use wget to download the file
            try:
                print("Downloading LegacyLauncher using wget from {}".format(url))
                run_command(['wget', '-O', file_name, url])  # Use wget on macOS
                print("Download complete.")

                # Verify that the file was downloaded
                if not os.path.exists(file_name):
                    print("Error: Downloaded file not found.")
                    return

                # Install the launcher on macOS
                run_command(['sudo', 'installer', '-pkg', file_name, '-target', '/'])  # Install .dmg on macOS
                print("LegacyLauncher installed successfully!")
            except Exception as e:
                print("Error during installation: {}".format(e))
        
        else:
            print("Unsupported OS.")
    else:
        print("Skipping LegacyLauncher installation.")

def gp_vncsession():
    """ Run the gp-vncsession command for headless Minecraft testing """
    confirm = raw_input("Do you want to run gp-vncsession for headless Minecraft testing? (Only for GitHub Codespaces!) (yes/no): ").strip().lower()
    if confirm == 'yes':
        if platform.system() == 'Windows':
            print("This feature is not available for Windows.")
        else:
            run_command(['gp-vncsession'])  # Pass command as a list
        print("gp-vncsession command executed.")
    else:
        print("gp-vncsession skipped.")

def detect_os():
    """ Detect the user's operating system """
    print("Operating System detected: {}".format(platform.system()))

def install_mcp_toolkit():
    """ Placeholder for MCP-related toolkit installations """
    confirm = raw_input("Do you want to install additional MCP modding tools? (yes/no): ").strip().lower()
    if confirm == 'yes':
        if platform.system() == 'Windows':
            print("Installing MCP modding tools for Windows...")
            # Add specific commands for Windows installation
        else:
            print("Installing MCP modding tools for Linux/macOS...")
            # Add specific commands for Linux/macOS installation
    else:
        print("Skipping MCP modding tools installation.")

def main_menu():
    """ Main menu to interact with different features """
    print("Welcome to the Minecraft MCP Modding QOL Toolkit!")
    detect_os()

    change_java_path()
    gp_vncsession()
    
    # Download and install LegacyLauncher first
    download_legacy_launcher()
    
    # Install Java 8 after LegacyLauncher
    install_java_8()

    # Add other features here
    install_mcp_toolkit()

if __name__ == "__main__":
    check_root()  # Check for root permissions
    main_menu()
