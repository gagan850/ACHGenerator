import sys, json, os
from datetime import datetime

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ACHGenerationLogic import ACHFileGenerator
from ACH_Constant.Constant import STANDARD_ENTRY_CLASS_MAPPING

ACCOUNTING_SYSTEM = 'XERO'

def preparePayload(companyDetail, transactionalDetail):
    """Prepare ACH payload from company and transaction details."""
    print("Inside prepare ach payload")
    print('"Inside prepare ach payload" company_data: ' + json.dumps(companyDetail, indent=4))
    print(f"Type of transactionalDetail: {type(transactionalDetail)}")
    print(f"Content of transactionalDetail: {transactionalDetail}")

    # Ensure transactionalDetail is always a list of dictionaries
    if isinstance(transactionalDetail, dict):
        transactionalDetail = [transactionalDetail]

    if not isinstance(transactionalDetail, list):
        raise ValueError("transactionalDetail must be a list or a dictionary")

    payloads = []

    for transaction in transactionalDetail:
        if not isinstance(transaction, dict):
            raise ValueError("Each transaction must be a dictionary")
        
        if ACCOUNTING_SYSTEM == "XERO":
            receiver_bank_details = transaction.get("Receiver Bank Details", "")
            if len(receiver_bank_details) >= 9:
                receiver_routing_number = receiver_bank_details[:9]
                receiver_account_number = receiver_bank_details[9:]
                transaction["Receiver Routing Number"] = receiver_routing_number
                transaction["Receiver Account Number"] = receiver_account_number
        payload = {
            "ImmediateOrigin": companyDetail.get("Company Financial Services", ""),
            "ImmediateDestination": companyDetail.get("Bank Name", ""),
            "ImmediateOriginRoutingNumber": companyDetail.get("Company Routing Number", ""),
            "ImmediateDestinationRoutingNumber": companyDetail.get("Bank Routing Number", ""),
            "TransactionType": transaction.get("Transaction Type", "Debit"),   
            "CompanyName": companyDetail.get("Company Name", ""),
            "CompanyId": companyDetail.get("Company Id", ""),
            "ReceiverName": transaction.get("Receiver Name", ""),
            "ReceivingBankAccountNumber": transaction.get("Receiver Account Number", ""),
            "ReceivingDFI": transaction.get("Receiver Routing Number", ""),
            "OriginatingBankRoutningNumber": companyDetail.get("Bank Routing Number", ""),
            "StandardEntryClassCode": STANDARD_ENTRY_CLASS_MAPPING.get(transaction.get("Standard Entry Class Code"), "PPD"),
            "EntryDescription": transaction.get("Entry Description", "VENDOR"),
            "Amount": transaction.get("Amount", ""),
            "TransactionIdentifier": transaction.get("Transaction Identifier", ""),
            "EntryNumber": transaction.get("Entry Number", "1"),
            "Reference": transaction.get("Reference", "")
        }
        print('Generated payload: ' + json.dumps(payload, indent=4))
        payloads.append(payload)

    return payloads