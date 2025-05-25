import subprocess as cmd
import re
import time

shell = 'netsh wlan show profile'
file=[]
# Clean function: Check if the text contains whitespace and wrap it in quotes if necessary
def clean(text):
    return f'"{text}"' if ' ' in text else text

# extract_profiles function: Extracts profile names from the netsh output
def extract_profiles(text):
    return re.findall(r':\s?(\w+.*)', text)

# Exec function: Executes shell commands and returns the output
def exec(command):
    return cmd.check_output(command, shell=True, text=True)

# Function to crack the password for a given profile
def crack_pass(profile):
    # Pattern for extracting the key content (password)
    pattern = r'\s+Key\s?Content\s+:\s(\S+)'
    string = exec(f'{shell} {profile} key=clear')
    result = re.search(pattern, string)
    
    # Return the profile and password, formatted for readability
    if result:
        return f'{re.sub(r'"','',profile).ljust(28)}\t\t\t{result.group(1)}'
    
    # If no password is found, return a message
    return f'{profile.ljust(48)}{"No password found".ljust(60)}'

# Function to check if the profile has a security key and attempt to crack the password
def hack(profile):
    pattern = r'\s+Security\s?key\s+:\s(\w+)'
    string = exec(f'{shell} {profile}')
    result = re.search(pattern, string)
    
    # If the security key is present, attempt to crack the password
    if result and result.group(1) == 'Present':
        output = crack_pass(profile)
        file.append(output)
        print(output)
def store():
    with open('secrets.txt','w') as f:
        f.write(f'\tDEVICE NAMES{" " * 28}PASSWORDS\n')
        f.write(f'===================={" " * 28}=========\n')
        for i in file:
            f.write(f'{i}\n')
def close_window(exit_time):
    
    for i in range(exit_time):
        print(f'\rExiting in {exit_time-i} second(s)',end="")
        time.sleep(1)    
# Main function to orchestrate the script
def main():
    
    
    # Execute the command to list all profiles and extract their names
    result = exec(shell)
    profiles_list = extract_profiles(result)
    
    print(f'\tDEVICE NAMES{" " * 28}PASSWORDS')
    print(f'===================={" " * 28}=========')
    # Iterate through profiles and attempt to crack passwords
    for profile in profiles_list:
        hack(clean(profile))
    store()
    close_window(10)
# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
    