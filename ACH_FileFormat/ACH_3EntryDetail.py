import sys
import os

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ACH_Util.FieldConfig import FieldConfig
from ACH_Util.RecordConfig import RecordConfig
from ACH_Constant.Constant import PADDING_LEFT, PADDING_RIGHT

class ACH_EntryDetail:
    def __init__(self, transactionType, receivingBankRoutingNumber, receivingBankAccountNumber, amount, transactionIdentifier, receiverName, originatingBankRoutningNumber, entryNumber):
        """
        Initializes the Entry Detail object.
        
        :param transaction_code: Transaction type (22 = Credit, 27 = Debit).
        :param receiving_dfi: Receiving bank's routing number (8 digits).
        :param dfi_account_number: Receiver's account number (up to 17 digits).
        :param amount: Amount of the transaction (10 digits, including leading zeros).
        :param identification_number: Unique transaction identifier (15 digits).
        :param individual_name: Receiver's name (22 characters).
        :param trace_number: Unique trace number (15 digits).
        """
        
        # Variables (Detail from CSV)
        self.transactionType                = transactionType
        self.receivingBankRoutingNumber     = receivingBankRoutingNumber
        self.receivingBankAccountNumber     = receivingBankAccountNumber
        self.amount                         = amount
        self.transactionIdentifier          = transactionIdentifier
        self.receiverName                   = receiverName
        self.originatingBankRoutningNumber  = originatingBankRoutningNumber
        self.entryNumber                    = entryNumber
        
        # Define all field configurations for the header
        self.all_fields = [             
            FieldConfig(name="Record Type Code",            length=1,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="6"),
            FieldConfig(name="Transaction Code",            length=2,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),
            FieldConfig(name="Receiving DFI",               length=8,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Check Digit",                 length=1,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Receiver Account Number",     length=17,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),
            FieldConfig(name="Amount",                      length=10,  padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Transaction Identifier",      length=15,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),   
            FieldConfig(name="Receiving Company Name",      length=22,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),
            FieldConfig(name="Discretionary Data",          length=2,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=True, value=""),
            FieldConfig(name="Addenda Record Indicator",    length=1,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=True, value="0"),
            FieldConfig(name="Originating DFI",             length=8,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Entry Number",                length=7,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False) 
        ]
        
    def getTransaction(self, transactionType):
        if transactionType == "Credit":
            return 22
        elif transactionType == "Debit":
            return 27
        
    def formatAmount(self, amount):
        # Ensure amount is a float and round to two decimal places
        formatted_amount = round(float(amount), 2)
        # Remove decimal and multiply by 100 (converting to cents)
        amount_in_cents = int(formatted_amount * 100)
        return amount_in_cents
    
    def generate(self):
        """
        Generate the formatted Entry Detail record.
        """
        record = RecordConfig(self.all_fields)
        values = {
            "Transaction Code"          : self.getTransaction(self.transactionType),
            "Receiving DFI"             : self.receivingBankRoutingNumber,
            "Check Digit"               : "1",
            "Receiver Account Number"   : self.receivingBankAccountNumber,
            "Amount"                    : self.formatAmount(self.amount),
            "Transaction Identifier"    : self.transactionIdentifier,
            "Receiving Company Name"    : self.receiverName,
            "Originating DFI"           : self.originatingBankRoutningNumber,
            "Entry Number"              : self.entryNumber
        }
        return record.generate(values)

# Example usage
if __name__ == "__main__":
    # Define example data
    transactionType                 = "Credit"              # Credit
    receivingBankRoutingNumber      = "12345678"            # Receiving bank routing number
    receivingBankAccountNumber      = "987654327810"        # Receiver's account number
    amount                          = "35.21"               # Transaction amount
    transactionIdentifier           = "943202528"           # Identification number
    receiverName                    = "OUTSELL, INC"        # Receiver's name
    originatingBankRoutningNumber   = "24090924"            # COMPANY BANK ROUTING NUMBER
    entryNumber                     = "281073550000001"     # Trace number (unique)

    # Create EntryDetail object
    entry_detail = ACH_EntryDetail(
        transactionType                 = transactionType,
        receivingBankRoutingNumber      = receivingBankRoutingNumber,
        receivingBankAccountNumber      = receivingBankAccountNumber,
        amount                          = amount,
        transactionIdentifier           = transactionIdentifier,
        receiverName                    = receiverName,
        originatingBankRoutningNumber   = originatingBankRoutningNumber,
        entryNumber                     = entryNumber
    )

    # Generate and print the Entry Detail record
    print(entry_detail.generate())
