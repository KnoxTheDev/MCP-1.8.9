#!/usr/bin/env python2
import os
import platform
import subprocess
import sys
import urllib

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

def run_command(cmd):
    """ Run a command with optional sudo on Linux/macOS, or directly on Windows """
    if platform.system() == 'Windows':
        try:
            subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print("Error running command: {}".format(e))
    else:
        if USE_SUDO:
            cmd = ['sudo'] + cmd
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            print("Error running command: {}".format(e))

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
    try:
        run_command(['apt', 'update'])  # Update package list
        run_command(['apt', 'install', '-y', 'openjdk-8-jdk'])  # Install Java 8
        print("Java 8 installed successfully!")
    except Exception as e:
        print("Error during Java installation: {}".format(e))
        print("Attempting to fix broken installs...")
        run_command(['apt', '--fix-broken', 'install'])  # Fix broken installs

def gp_vncsession():
    """ Run the gp-vncsession command for headless Minecraft testing """
    confirm = raw_input("Do you want to run gp-vncsession for headless Minecraft testing? (yes/no): ").strip().lower()
    if confirm == 'yes':
        if platform.system() == 'Windows':
            print("This feature is not available for Windows.")
        else:
            run_command(['gp-vncsession'])
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

def download_legacy_launcher():
    """ Download and install the LegacyLauncher """
    confirm = raw_input("Do you want to install the LegacyLauncher for Minecraft testing? (yes/no): ").strip().lower()
    if confirm == 'yes':
        if platform.system() == 'Windows':
            url = 'https://llaun.ch/installer'
            file_name = 'LegacyLauncherInstaller.exe'
        elif platform.system() == 'Linux':
            url = 'https://llaun.ch/ubuntu'
            file_name = 'legacylauncher.deb'
        elif platform.system() == 'Darwin':  # macOS
            url = 'https://llaun.ch/macos'
            file_name = 'legacylauncher.pkg'
        else:
            print("Unsupported OS.")
            return

        # Download the installer
        try:
            print("Downloading LegacyLauncher from {}".format(url))
            urllib.urlretrieve(url, file_name)
            print("Download complete.")

            # Install the launcher
            if platform.system() == 'Windows':
                print("Running installer...")
                os.startfile(file_name)  # For Windows
            elif platform.system() == 'Linux':
                run_command(['dpkg', '-i', file_name])
            elif platform.system() == 'Darwin':  # macOS
                run_command(['installer', '-pkg', file_name, '-target', '/'])
            
            print("LegacyLauncher installed successfully!")
        except Exception as e:
            print("Error during installation: {}".format(e))
    else:
        print("Skipping LegacyLauncher installation.")

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