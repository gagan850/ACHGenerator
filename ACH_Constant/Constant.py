PADDING_LEFT = "left"
PADDING_RIGHT = "right"

MANUAL_MANDATORY_FIELDS = ["Receiver Name",  "Receiver Account Number", "Receiver Routing Number", "Amount"]

XERO_CSV_FORMAT = [
                    "Amount", 
                   "Receiver Bank Details", 
                   "Receiver Name", 
                   "Reference", 
                   "Transaction Identifier"
                   ]

XERO_CSV_FORMAT_MANDATORY = [
                    "Amount", 
                   "Receiver Bank Details", 
                   "Receiver Name"
                   ]

GENERIC_CSV_FORMAT = [
            "Receiver Name",
            "Receiver Account Number",
            "Receiver Routing Number",
            "Amount",
            "Transaction Identifier",
            "Reference"
        ]

GENERIC_CSV_FORMAT_MANDATORY = [
            "Receiver Name",
            "Receiver Account Number",
            "Receiver Routing Number",
            "Amount"
        ]

STANDARD_ENTRY_CLASS_MAPPING = {
    "Prearranged Payment and Deposit Entries": "PPD",
    "Corporate Credit or Debit Entries": "CCD"
}

ACCOUNTING_SYSTEM = ['Default','Xero']

TRANSACTION_DETAILS = {
    "Receiver Name": "",
    "Receiver Account Number": "",
    "Receiver Routing Number": "",
    "Transaction Type": ["Credit", "Debit"],
    "Standard Entry Class Code": ["Prearranged Payment and Deposit Entries","Corporate Credit or Debit Entries"],
    "Entry Description": "VENDOR",
    "Amount": "",
    "Transaction Identifier":"",
    "Reference": ""
}

DEFAULT_COMPANY_DETAILS = {
    "Company Name": "Dummy Company",
    "Company Id": "0000000000",
    "Company Financial Services": "Dummy Financial Services",
    "Company Routing Number": "000000000",
    "Bank Name": "Dummy Bank",
    "Bank Routing Number": "000000000",
    "Accounting System":"Xero"
}
UPDATED_COMPANY_DETAILS = {'Company Name': 'Dummy Company', 'Company Id': '0000000000', 'Company Financial Services': 'Dummy Financial Service', 'Company Routing Number': '000000000', 'Bank Name': 'Dummy Bank', 'Bank Routing Number': '000000000', 'Accounting System': 'Xero'}