import os, sys

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ACH_FileFormat.ACH_1FileHeader import ACH_FileHeader
from ACH_FileFormat.ACH_2BatchHeader import ACH_BatchHeader
from ACH_FileFormat.ACH_3EntryDetail import ACH_EntryDetail
from ACH_FileFormat.ACH_5BatchControlRecord import ACH_BatchControlRecord
from ACH_FileFormat.ACH_6FileControlRecord import ACH_FileControlRecord

class ACHFileGenerator:
    def __init__(self, records=[]):
        self.records = records
                
    def calculate_entry_hash(self):
        """Calculate the Entry Hash by summing the first 8 digits of all routing numbers"""
        total_hash = 0
        for record in self.records:
            # Extract the first 8 digits of the routing number
            first_8_digits = int(record['ReceivingDFI'][:8])
            total_hash += first_8_digits
        
        # Format as a 10-digit string (padded with leading zeros if necessary)
        return str(total_hash).zfill(10)

    def calculate_total_debit_amount(self):
        """Calculate the total debit amount from all records."""
        total_debit = 0
        for record in self.records:
            # Assuming 'Amount' field can have decimals and is negative for debits
            amount = float(record['Amount'])  # Convert the string amount to float
            if amount < 0:  # Negative amounts are debits
                total_debit += abs(amount)  # Add absolute value for debits
        return str(int(total_debit * 100))  # Convert to cents (as integer)

    def calculate_total_credit_amount(self):
        """Calculate the total credit amount from all records."""
        total_credit = 0
        for record in self.records:
            # Assuming 'Amount' field can have decimals and is positive for credits
            amount = float(record['Amount'])  # Convert the string amount to float
            if amount > 0:  # Positive amounts are credits
                total_credit += amount  # Add value for credits
        return str(int(total_credit * 100))  # Convert to cents (as integer)
    
    def generate(self):
        """Generate the full ACH content"""
        # Initialize ACH File Header
        file_header = ACH_FileHeader(
            immediateOrigin=self.records[0]['ImmediateOrigin'],
            immediateDestination=self.records[0]['ImmediateDestination'],
            immediateOriginRoutingNumber=self.records[0]['ImmediateOriginRoutingNumber'],
            immediateDestinationRoutingNumber=self.records[0]['ImmediateDestinationRoutingNumber'] ,
            reference=self.records[0]['Reference']
            )

        # Initialize ACH Batch Header
        batch_header = ACH_BatchHeader(
            transactionType=self.records[0]['TransactionType'],
            companyName=self.records[0]['CompanyName'],
            companyId=self.records[0]['CompanyId'],
            standardEntryClassCode=self.records[0]['StandardEntryClassCode'],
            entryDescription=self.records[0]['EntryDescription'],
            effectiveTransactionDate="",
            originatingBankRoutningNumber=self.records[0]['ImmediateDestinationRoutingNumber'],
            batchNumber="1"

        )

        # Loop through records and generate Entry Detail for each row
        entry_details = []
        entry_number = 1  # Start from 1 or any desired starting number
        for record in self.records:
            entry_detail = ACH_EntryDetail(
                transactionType=record['TransactionType'],
                receivingBankRoutingNumber=record['ReceivingDFI'],
                receivingBankAccountNumber=record['ReceivingBankAccountNumber'],
                amount=record['Amount'],
                transactionIdentifier=record['TransactionIdentifier'],
                receiverName=record['ReceiverName'],
                originatingBankRoutningNumber=self.records[0]['ImmediateDestinationRoutingNumber'],
                entryNumber=entry_number
            )
            entry_details.append(entry_detail.generate())
            entry_number += 1
        # Calculate Entry Hash, Total Debit, and Total Credit Amount
        entry_hash = self.calculate_entry_hash()
        total_debit_amount = self.calculate_total_debit_amount()  # Correctly calculate debit
        total_credit_amount = self.calculate_total_credit_amount()  # Correctly calculate credit

        # Initialize ACH Batch Header
        batch_control = ACH_BatchControlRecord(
            entryAddendaCount=len(entry_details),
            entryHash=entry_hash,
            totalDebitAmount=str(total_debit_amount),
            totalCreditAmount=str(total_credit_amount),
            companyId=self.records[0]['CompanyId'],
            originatingBankRoutingNumber=self.records[0]['ImmediateDestinationRoutingNumber'],
            batchNumber="1"

        )
        # Initialize ACH File Control Record
        file_control = ACH_FileControlRecord(
            batchCount=1,  # Just an example; you may need to adjust this based on your needs
            blockCount=1,  # Assuming a single block; adjust as needed
            entryAddendaCount=len(entry_details),  # For simplicity, assuming entry count equals addenda count
            entryHash=entry_hash,  # Placeholder; calculate if needed
            totalDebitAmount=str(total_debit_amount),  # Placeholder; calculate total debit amount
            totalCreditAmount=str(total_credit_amount)  # Placeholder; calculate total credit amount
        )

        # Generate ACH file content
        ach_file = file_header.generate() + '\r\n' + batch_header.generate() + '\r\n'
        for entry in entry_details:
            ach_file += entry  + '\r\n'
        ach_file += batch_control.generate()  + '\r\n'
        ach_file += file_control.generate()

        # Pad lines to ensure the total line count is a multiple of 10
        ach_file = self.pad_lines_to_multiple_of_10(ach_file) + '\r\n'
        return ach_file

    def pad_lines_to_multiple_of_10(self, ach_file_content):
        """
        Ensures the total number of lines in the ACH file is a multiple of 10
        by appending lines with all '9's.
        
        Args:
            ach_file_content (str): The generated ACH file content.
        
        Returns:
            str: The padded ACH file content.
        """
        lines = ach_file_content.split('\r\n')  # Split content into lines
        total_lines = len(lines)
        
        # Calculate the number of lines to add
        lines_to_add = (10 - (total_lines % 10)) % 10  # Add lines only if not already a multiple of 10
        
        # Append lines with all '9's if necessary
        if lines_to_add > 0:
            padding_line = '9' * 94  # Assuming a fixed-width line of 94 characters
            lines.extend([padding_line] * lines_to_add)
        
        return '\r\n'.join(lines)  # Rejoin lines with '\r\n'