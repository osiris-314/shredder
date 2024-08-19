#!/usr/bin/env python3
import os
import subprocess
from colorama import Fore, Style

def print_banner():
    print('\n')
    print('''  @@@@@@     @@@  @@@     @@@@@@@      @@@@@@@@     @@@@@@@      @@@@@@@      @@@@@@@@     @@@@@@@ 
 !@@         @@!  @@@     @@!  @@@     @@!          @@!  @@@     @@!  @@@     @@!          @@!  @@@
  !@@!!      @!@!@!@!     @!@!!@!      @!!!:!       @!@  !@!     @!@  !@!     @!!!:!       @!@!!@! 
     !:!     !!:  !!!     !!: :!!      !!:          !!:  !!!     !!:  !!!     !!:          !!: :!! 
 ::.: :       :   : :      :   : :     : :: :::     :: :  :      :: :  :      : :: :::      :   : :''')
    print('\n')

def list_disks():
    # Run the lsblk command and capture its output
    result = subprocess.run(['lsblk', '-o', 'NAME,RM,TYPE,SIZE'], stdout=subprocess.PIPE, text=True)
    
    # Split the output into lines
    lines = result.stdout.strip().split('\n')
    
    # Extract the headers and the disk information
    headers = lines[0].split()
    disks_info = lines[1:]
    
    # Create a list to store the disk information
    disks = []

    # Iterate over the disk information
    for disk in disks_info:
        # Split each line by spaces
        disk_data = disk.split()
        name = disk_data[0]
        removable = disk_data[1]
        dtype = disk_data[2]
        size = disk_data[3]
        
        # Filter out partitions and only get the base disk names
        if dtype == 'disk':
            is_removable = "Yes" if removable == '1' else "No"
            disk_info = (name, size, is_removable)
            disks.append(disk_info)
    
    return disks

def format_table(disks, title):
    table = f"{title}"
    table += f"{'Disk':<10}{'Size':<10}{'Removable':<10}\n"
    table += "-"*30 + "\n"
    for disk in disks:
        name, size, is_removable = disk
        table += f"{name:<10}{size:<10}{is_removable:<10}\n"
    return table

def shred_disk():
    disks = list_disks()
    table = format_table(disks, '')
    print(table)
    disk_choice = input('Enter the name of the disk to shred (e.g., sda): ')
    print(Fore.LIGHTBLUE_EX + 'Go get a coffee this will take a while...\n' + Fore.LIGHTGREEN_EX)
    subprocess.run(f'sudo shred -vfz /dev/{disk_choice}', shell=True)

def shred_file():
    file_path = input('Enter the path to the file to shred: ')
    print(Fore.LIGHTBLUE_EX + 'Shredding the file...\n' + Fore.LIGHTGREEN_EX)
    subprocess.run(f'sudo shred -vzu -n5 {file_path}', shell=True)

def shred_directory():
    dir_path = input('Enter the path to the directory to shred all files within: ')
    if not os.path.isdir(dir_path):
        print(Fore.RED + 'Invalid directory path.' + Style.RESET_ALL)
        return
    
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    if not files:
        print(Fore.RED + 'No files found in the directory.' + Style.RESET_ALL)
        return
    
    print(Fore.LIGHTBLUE_EX + 'Shredding files in the directory...\n' + Style.RESET_ALL)
    for file in files:
        print(Fore.YELLOW + f'Shredding {file}...' + Style.RESET_ALL)
        subprocess.run(f'sudo shred -vzu -n5 {file}', shell=True)

def main():
    print_banner()
    choice = input('Do you want to shred a Disk, File, or Directory? (Enter "d" for Disk, "f" for File, "dir" for Directory): ').strip().lower()
    if choice == 'd':
        shred_disk()
    elif choice == 'f':
        shred_file()
    elif choice == 'dir':
        shred_directory()
    else:
        print(Fore.RED + 'Invalid choice. Please enter "d" for Disk, "f" for File, or "dir" for Directory.' + Style.RESET_ALL)

if __name__ == '__main__':
    main()
