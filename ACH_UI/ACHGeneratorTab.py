import os, sys, json
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton, QComboBox,QRadioButton,QButtonGroup, QFileDialog, QMessageBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ACH_UI.Styles import success_buttonStyle, normal_buttonStyle
from ACH_Constant.Constant import MANUAL_MANDATORY_FIELDS
from ACH_Constant.Constant import UPDATED_COMPANY_DETAILS
from ACH_Constant.Constant import TRANSACTION_DETAILS
from ACH_Service.ACH_CSVHandler import download_template, validate_csv, read_csv_data
from ACH_Service.ACH_PayloadCreator import preparePayload
from ACH_Service.ACH_Generator import generateACH

class ACHGeneratorTab:
    def __init__(self, parent):
        self.parent = parent
        self.transactionDetails = TRANSACTION_DETAILS
        self.fields = {}
        self.setup_ui()

    def setup_ui(self):
        """Set up the Company Details tab with a form"""
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        utility_selector_layout = QVBoxLayout() 
        utility_selector_layout.setSpacing(10)

        self.manual_radio = QRadioButton("Manual")
        self.csv_radio = QRadioButton("CSV")
        self.manual_radio.setChecked(True)
        self.utilityType = QButtonGroup()
        self.utilityType.addButton(self.manual_radio)
        self.utilityType.addButton(self.csv_radio)
        
        # Connect radio buttons to a method to handle state changes
        self.manual_radio.toggled.connect(self.toggle_edit_mode)
        self.csv_radio.toggled.connect(self.toggle_edit_mode)
        
        # Add radio buttons to a layout
        utility_selector_layout.addWidget(self.manual_radio)
        utility_selector_layout.addWidget(self.csv_radio)
        # Add fields and labels dynamically
        # Example of setting up the form with QLineEdits and QComboBoxes using if-elif-else
        for row, (label_text, default_value) in enumerate(self.transactionDetails.items()):
            label = QLabel(label_text)
            
            # Check if the label is "xyz"
            if label_text == "Transaction Type":
                # Create a combo box for "xyz"
                combo_box = QComboBox()
                for item in default_value:
                    combo_box.addItem(item)  # Add items to the combo box
                #combo_box.addItem(default_value[0])  # Add options to the combo box
                #combo_box.addItem(default_value[1])
                self.fields[label_text] = combo_box
                grid_layout.addWidget(label, row, 0)
                grid_layout.addWidget(combo_box, row, 1)
            
            # Check if the label is "abc"
            elif label_text == "Standard Entry Class Code":
                # Create a combo box for "abc"
                combo_box = QComboBox()
                for item in default_value:
                    combo_box.addItem(item)  # Add items to the combo box
                #combo_box.addItem(default_value[0])
                #combo_box.addItem(default_value[1])
                self.fields[label_text] = combo_box
                grid_layout.addWidget(label, row, 0)
                grid_layout.addWidget(combo_box, row, 1)
            
            # For other labels, use QLineEdit
            else:
                # Create a QLineEdit for other fields
                line_edit = QLineEdit(default_value)
                self.fields[label_text] = line_edit
                grid_layout.addWidget(label, row, 0)
                grid_layout.addWidget(line_edit, row, 1)
                        
                # Apply validation based on the field
                if label_text == "Receiver Routing Number":
                    line_edit.setValidator(QIntValidator(0, 999999999, self.parent))
                    line_edit.setMaxLength(9) 
                elif label_text == "Receiver Account Number":
                    line_edit.setMaxLength(17) 
                elif label_text == "Receiver Name":
                    line_edit.setMaxLength(22)  
                elif label_text == "Entry Description":
                    line_edit.setMaxLength(10) 
                elif label_text == "Transaction Identifier":
                    line_edit.setMaxLength(15) 
                elif label_text == "Reference (For File)":
                    line_edit.setMaxLength(8)  
                elif label_text == "Amount":
                    line_edit.setValidator(QDoubleValidator(0.00, 99999999.99, 2, self.parent))  
                    line_edit.setMaxLength(10)  

        # Add buttons
        self.download_template = QPushButton("Download CSV Template")
        self.download_template.setStyleSheet(normal_buttonStyle)
        self.download_template.setVisible(False)
        
        self.upload_button = QPushButton("Upload")
        self.upload_button.setStyleSheet(normal_buttonStyle)
        self.upload_button.setVisible(False)

        self.generateAchButton = QPushButton("Generate ACH")
        self.generateAchButton.setStyleSheet(success_buttonStyle)
        self.generateAchButton.setVisible(True)

        # Connect buttons
        self.download_template.clicked.connect(self.csv_template_download)
        self.upload_button.clicked.connect(self.csv_upload)
        self.generateAchButton.clicked.connect(self.generate_ach)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.download_template)
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.generateAchButton)
        
        main_layout.addLayout(utility_selector_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(button_layout)

        self.parent.setLayout(main_layout)

    def toggle_edit_mode(self):
        """Enable/Disable form fields based on the radio button selection"""
        if self.csv_radio.isChecked():
            # Disable all fields except the Upload and Generate ACH buttons
            for field in self.fields.values():
                field.setDisabled(True)
            self.download_template.setVisible(True)
            self.upload_button.setVisible(True)
            self.generateAchButton.setVisible(False)
            self.reset_fields()
        else:
            # Enable all fields and hide the Upload button
            for field in self.fields.values():
                field.setDisabled(False)
            self.download_template.setVisible(False)
            self.upload_button.setVisible(False)
            self.generateAchButton.setVisible(True)

    def csv_template_download(self):
        """Handle the CSV template download process."""
        # Open a file dialog for the user to select the save location
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save CSV Template", "ACH_Template.csv", "CSV Files (*.csv)", options=options
        )

        if file_path:
            # Call the backend function to generate the CSV template
            result = download_template(file_path)

            if "Error" in result:
                # Show error message if there's an issue
                QMessageBox.critical(None, "Error", result)
            else:
                # Show success message
                QMessageBox.information(None, "Success", f"CSV template has been saved to:\n{result}")
        else:
            QMessageBox.warning(None, "Cancelled", "No file selected. Operation cancelled.")
    
    def csv_upload(self):
        self.generateAchButton.setVisible(False)
        """Allow user to upload only CSV files."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, 
            "Select CSV File", 
            "", 
            "CSV Files (*.csv);;All Files (*)", 
            options=options
        )
        if file_path:
            try:
                # Read and validate the CSV file
                self.csv_file_path = file_path
                issues = validate_csv(file_path)

                if issues:
                    # Display issues to the user
                    issue_message = "\n".join(issues)
                    QMessageBox.warning(
                        self.parent, 
                        "CSV Validation Errors", 
                        f"The following issues were found in the CSV file:\n\n{issue_message}"
                    )
                else:
                    transactional_data = read_csv_data(self.csv_file_path)
                    if not transactional_data:  # Empty list or dictionary
                        QMessageBox.warning(self.parent, "No Records", "The uploaded CSV file contains no records.")
                    else:
                        self.generateAchButton.setVisible(True)
                        QMessageBox.information(
                            self.parent, 
                            "CSV Validation Success", 
                            "CSV file is valid and ready for processing."
                        )
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"An error occurred: {str(e)}")
            
    def generate_ach(self):
        """Generate the ACH payload based on the selected data source."""
        try:
            if self.csv_radio.isChecked() and self.csv_file_path:
                # Use the already uploaded CSV file
                transactional_data = read_csv_data(self.csv_file_path)
                if not transactional_data:  # Empty list or dictionary
                    QMessageBox.warning(self.parent, "No Records", "The uploaded CSV file contains no records.")
                print('transactional_data: ' + json.dumps(transactional_data, indent=4))
                print('company_detail: ' + json.dumps(UPDATED_COMPANY_DETAILS, indent=4))
                payload = preparePayload(UPDATED_COMPANY_DETAILS, transactional_data)
                generateACH(payload)
                self.generateAchButton.setVisible(False)
            else:
                if not self.validate_mandatory_fields():
                    return
                fields_json = {}

                for label, field in self.fields.items():
                    if isinstance(field, QComboBox):
                        current_value = field.currentText()
                        
                        # Store the values in a dictionary
                        fields_json[label] = current_value
                    elif isinstance(field, QLineEdit):
                        # For QLineEdit, store the text value
                        fields_json[label] = field.text().strip()
                print('transactional_data: ' + json.dumps(fields_json, indent=4))
                print('company_detail: ' + json.dumps(UPDATED_COMPANY_DETAILS, indent=4))
                self.generateAchButton.setVisible(True)
                # Handle manual data from form fields
                payload = preparePayload(UPDATED_COMPANY_DETAILS, fields_json)
                generateACH(payload)

        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"An error occurred: {str(e)}")

        
    def reset_fields(self):
        """Reset all fields to their default values from TRANSACTION_DETAILS."""
        default_values = TRANSACTION_DETAILS  # Reload the default data
        for label, field in self.fields.items():
            if isinstance(field, QComboBox):
                # Reset ComboBox to its first option
                field.setCurrentIndex(0)
            elif isinstance(field, QLineEdit):
                # Reset QLineEdit to default value
                field.setText(default_values.get(label, ""))
            
    def validate_mandatory_fields(self):
        """Validate the mandatory fields."""
        missing_fields = []
        invalid_amount = False
        
        # First pass: Check for missing mandatory fields
        for label in MANUAL_MANDATORY_FIELDS:
            field = self.fields.get(label)
            
            if isinstance(field, QComboBox):
                if not field.currentText().strip():  # If combo box is empty
                    missing_fields.append(label)
            elif isinstance(field, QLineEdit):
                text = field.text().strip()
                if not text:  # LineEdit is empty
                    missing_fields.append(label)
                
        # Notify user if any mandatory fields are missing
        if missing_fields:
            missing_fields_str = "\n".join(missing_fields)
            QMessageBox.warning(self.parent, "Missing Fields", f"The following fields are mandatory and cannot be empty:\n\n{missing_fields_str}")
            return False
        
        # Second pass: Validate specific constraints
        for label in MANUAL_MANDATORY_FIELDS:
            field = self.fields.get(label)
            if isinstance(field, QLineEdit):
                text = field.text().strip()
                if label == "Receiver Routing Number":
                    if len(text) != 9:  # Routing number length validation
                        QMessageBox.warning(self.parent, "Invalid Input", "Receiver Routing Number must be exactly 9 digits.")
                        return False
                if label == "Amount":
                    try:
                        amount = float(text)  # Ensure Amount is numeric
                        if amount <= 0:  # Check if Amount is positive
                            QMessageBox.warning(self.parent, "Invalid Amount", "The Amount must be greater than zero.")
                            return False
                    except ValueError:
                        # Notify user immediately if Amount is invalid
                        QMessageBox.warning(self.parent, "Invalid Amount", "The Amount field must be a valid numeric value.")
                        return False

        return True