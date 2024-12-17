import os, sys
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton, QComboBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ACH_Util.Util import saveCompanyDetails, showPopup, updateCompanyDetails
from ACH_Constant.Constant import DEFAULT_COMPANY_DETAILS, UPDATED_COMPANY_DETAILS, ACCOUNTING_SYSTEM
from ACH_UI.Styles import error_buttonStyle, success_buttonStyle, normal_buttonStyle

class CompanyDetailsTab:
    def __init__(self, parent):
        self.parent = parent
        self.updatedCompanyDetails = UPDATED_COMPANY_DETAILS
        self.fields = {}
        self.setup_ui()

    def setup_ui(self):
        """Set up the Company Details tab with a form"""
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Add fields and labels dynamically
        
        row = 0  # Initialize row outside of the loop to track the number of rows

        for label_text, default_value in self.updatedCompanyDetails.items(): 
            label = QLabel(label_text)

            if label_text == "Accounting System":
                accountingSystem = QLabel("Accounting System")
                accountingSystemValues = QComboBox()
                for item in ACCOUNTING_SYSTEM:
                    accountingSystemValues.addItem(item)  # Add items to the combo box
                accountingSystemValues.setCurrentText(default_value)
                self.fields[label_text] = accountingSystemValues

                accountingSystemValues.setDisabled(True)
                grid_layout.addWidget(accountingSystem, row, 0)
                grid_layout.addWidget(accountingSystemValues, row, 1)
                
            else:
                line_edit = QLineEdit(default_value)
                line_edit.setReadOnly(True)
                self.fields[label_text] = line_edit
                grid_layout.addWidget(label, row, 0)
                grid_layout.addWidget(line_edit, row, 1)
                # Apply validation based on the field
                if label_text == "Company Name":
                    line_edit.setMaxLength(16) 
                elif label_text == "Company Id":
                    line_edit.setMaxLength(10)  
                elif label_text == "Company Financial Services":
                    line_edit.setMaxLength(23) 
                elif label_text == "Company Routing Number":
                    line_edit.setValidator(QIntValidator(0, 999999999, self.parent))
                    line_edit.setMaxLength(9) 
                elif label_text == "Bank Name":
                    line_edit.setMaxLength(23)  
                elif label_text == "Bank Routing Number":
                    line_edit.setValidator(QIntValidator(0, 999999999, self.parent))
                    line_edit.setMaxLength(9) 
            row += 1;                 
        

        # Add buttons
        self.edit_button = QPushButton("Edit")
        self.edit_button.setStyleSheet(error_buttonStyle)
        
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(success_buttonStyle)
        
        self.reset_button = QPushButton("Reset to Default")
        self.reset_button.setStyleSheet(normal_buttonStyle)

        self.save_button.setVisible(False)

        # Connect buttons
        self.edit_button.clicked.connect(self.toggle_edit_mode)
        self.save_button.clicked.connect(self.save_changes)
        self.reset_button.clicked.connect(self.reset_defaults)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)

        main_layout.addLayout(grid_layout)
        main_layout.addLayout(button_layout)

        self.parent.setLayout(main_layout)

    def toggle_edit_mode(self):
        """Toggle between editable and read-only modes for the fields."""
        is_editable = self.edit_button.isVisible()
        
        for field in self.fields.values():
            if isinstance(field, QLineEdit):
                field.setReadOnly(not is_editable)  # QLineEdit: use setReadOnly
            elif isinstance(field, QComboBox):
                field.setEnabled(is_editable)  # QComboBox: use setEnabled (True for editable, False for read-only)

        self.edit_button.setVisible(not is_editable)
        self.save_button.setVisible(is_editable)

    def save_changes(self):
        """Save changes to UPDATED_COMPANY_DETAILS and toggle back to read-only mode."""
        for label, field in self.fields.items():
            if isinstance(field, QLineEdit):
                self.updatedCompanyDetails[label] = field.text()  # Get text from QLineEdit
            elif isinstance(field, QComboBox):
                self.updatedCompanyDetails[label] = field.currentText()  # Get selected text from QComboBox

        updateCompanyDetails(self.updatedCompanyDetails)

        showPopup("Company details have been updated successfully!")
        self.toggle_edit_mode()

    def reset_defaults(self):
        """Reset all fields to default values."""
        for label, field in self.fields.items():
            default_value = DEFAULT_COMPANY_DETAILS.get(label)
            if default_value is not None:
                if isinstance(field, QLineEdit):
                    field.setText(default_value)  # Set text for QLineEdit
                elif isinstance(field, QComboBox):
                    field.setCurrentText(default_value)  # Set text for QComboBox

        showPopup("Company details have been reset to default values.")
        self.toggle_edit_mode()
