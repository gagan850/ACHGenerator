import json
import sys
import os
import re

from PyQt5.QtWidgets import QMessageBox

# Add the parent directory of the current file to the system path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Determine if we are in a packaged application (e.g., .dmg, .app)
if getattr(sys, 'frozen', False):  # This check is for bundled executables
    # If running from a bundled application, use sys._MEIPASS to find the package location
    base_path = sys._MEIPASS
else:
    # If running in development mode (not packaged), use the current script directory
    base_path = os.path.dirname(os.path.abspath(__file__))

# Define the path to the 'ACH_Constant' directory
constants_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'ACH_Constant/Constant.py')

def load_json_file(file_name):
    """Helper function to load a JSON file."""
    try:
        file_path = os.path.join(constants_dir, file_name)
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error loading file: {e}")
        return {}

def loadCompanyDetails():
    """Load the company details from JSON files."""
    default_details = load_json_file('DEFAULT_COMPANY_DETAILS.json')        
    updated_details = load_json_file('UPDATED_COMPANY_DETAILS.json')    
    return default_details, updated_details

def loadTransactionDetails():
    """Load the transaction details from JSON files."""    
    return load_json_file('TRANSACTION_DETAILS.json')


def saveCompanyDetails(updated_company_details):
    """Save the UPDATED_COMPANY_DETAILS dictionary to the constants file."""
    try:
        file_path = os.path.join(constants_dir, 'UPDATED_COMPANY_DETAILS.json')
        with open(file_path, "w") as file:
            json.dump(updated_company_details, file, indent=4)
    except Exception as e:
        print(f"Error saving to constants file: {e}")

def showPopup(message, title="Information"):
    """Show a popup message."""
    QMessageBox.information(None, title, message)


def updateCompanyDetails(updatedCompanyDetails):
    update_constant_in_file(constants_dir, "UPDATED_COMPANY_DETAILS", updatedCompanyDetails)


def update_constant_in_file(file_path, variable_name, new_value):
    """
    Updates a specific constant in a Python constants file.

    Args:
        file_path (str): The path to the constants file.
        variable_name (str): The name of the constant to update (e.g., 'UPDATED_COMPANY_DETAILS').
        new_value (dict): The new value for the constant (as a Python dictionary).
    """
    try:
        # Read the current content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Prepare the new value as valid Python code
        new_value_str = f"{variable_name} = {repr(new_value)}"

        # Create a regex pattern to match the specific constant
        # Matches variable assignment followed by a dictionary
        pattern = rf"(?m)^\s*{variable_name}\s*=\s*\{{.*?\}}"

        # Replace the old value with the new value
        updated_content = re.sub(pattern, new_value_str, content, flags=re.DOTALL)

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)

        print(f"Successfully updated '{variable_name}' in {file_path}.")

    except Exception as e:
        print(f"Error updating the constant: {e}")


# Example Usage
#file_path = "constants.py"  # Path to your file containing constants

#new_updated_company_details = {
#    "Company Name": "New WIS/WEM LLC",
#    "Company Id": "9999999999",
#    "Company Financial Services": "Updated Inform. Serv.",
#    "Company Routing Number": "999999999",
#    "Bank Name": "Updated Bank Inc.",
#    "Bank Routing Number": "999999999"
#}

#update_constant_in_file(file_path, "UPDATED_COMPANY_DETAILS", new_updated_company_details)
