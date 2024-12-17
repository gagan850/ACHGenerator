import csv, sys, os
from datetime import datetime
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton, QComboBox,QRadioButton,QButtonGroup, QFileDialog, QMessageBox

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ACH_Constant.Constant import GENERIC_CSV_FORMAT, GENERIC_CSV_FORMAT_MANDATORY, XERO_CSV_FORMAT, XERO_CSV_FORMAT_MANDATORY, STANDARD_ENTRY_CLASS_MAPPING

def validate_xero_csv(file_path):
    """
    Validate a CSV file specific to XERO accounting system.
    Assumes that the file does not contain headers and follows the column order defined in XERO_CSV_FORMAT.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of validation error messages.
    """
    expected_columns = XERO_CSV_FORMAT
    mandatory_columns = XERO_CSV_FORMAT_MANDATORY
    issues = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',')

        # Validate rows (No headers, assume column order matches expected_columns)
        for row_num, row in enumerate(reader, start=1):  # No header, start at 1
            for index, field in enumerate(mandatory_columns):
                value = row[index].strip() if len(row) > index else ""

                if not value:
                    issues.append(f"Row {row_num}: Missing value for '{field}'")
                elif field == "Amount":
                    # Validate 'Amount' as a numeric value > 0
                    try:
                        amount = float(value)
                        if amount <= 0:
                            issues.append(f"Row {row_num}: 'Amount' must be greater than 0.")
                    except ValueError:
                        issues.append(f"Row {row_num}: 'Amount' must be a valid numeric value.")
    return issues


def validate_generic_csv(file_path):
    """
    Validate a CSV file for accounting systems other than XERO.
    Expects headers and validates based on mandatory fields.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of validation error messages.
    """
    expected_headers = GENERIC_CSV_FORMAT
    mandatory_fields = GENERIC_CSV_FORMAT_MANDATORY
    issues = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader, None)

        # Check for headers
        if not headers:
            issues.append("File is empty or missing headers.")
            return issues

        # Validate headers
        missing_headers = [field for field in mandatory_fields if field not in headers]
        if missing_headers:
            issues.append(f"Missing mandatory headers: {', '.join(missing_headers)}")

        # Create header mapping
        header_mapping = {header: index for index, header in enumerate(headers)}

        # Validate rows
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            for field in mandatory_fields:
                col_index = header_mapping.get(field)
                value = row[col_index].strip() if col_index is not None and len(row) > col_index else ""

                if not value:
                    issues.append(f"Row {row_num}: Missing value for '{field}'")
                elif field == "Amount":
                    # Validate 'Amount' as a numeric value > 0
                    try:
                        amount = float(value)
                        if amount <= 0:
                            issues.append(f"Row {row_num}: 'Amount' must be greater than 0.")
                    except ValueError:
                        issues.append(f"Row {row_num}: 'Amount' must be a valid numeric value.")
    return issues


def validate_csv(accountingSystem, file_path):
    """
    Wrapper function to validate CSV files based on the accounting system.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of validation error messages.
    """
    if accountingSystem == 'Xero':
        return validate_xero_csv(file_path)
    else:
        return validate_generic_csv(file_path)

      
def download_template(accountingSystem, file_path):
    try:
        # Define the columns for the CSV template
        columns = XERO_CSV_FORMAT if accountingSystem == 'Xero' else GENERIC_CSV_FORMAT
        
        # Write the CSV template
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(columns)
        return file_path
    except Exception as e:
        return f"Error: {str(e)}" 

def read_xero_csv(file_path):
    """
    Read XERO CSV data assuming there are no headers.
    Maps data based on a predefined column order.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries representing each row.
    """
    csv_data = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            # Map rows to the predefined column names
            row_dict = {column: row[index] if index < len(row) else "" for index, column in enumerate(XERO_CSV_FORMAT)}
            csv_data.append(row_dict)
    return csv_data


def read_generic_csv(file_path):
    """
    Read generic CSV data with headers and return it as a list of dictionaries.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries representing each row.
    """
    csv_data = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            csv_data.append(row)
    return csv_data


def read_csv_data(accountingSystem, file_path):
    """
    Wrapper to read CSV data based on the accounting system.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries representing each row.
    """
    if accountingSystem == 'Xero':
        return read_xero_csv(file_path)
    else:
        return read_generic_csv(file_path)
