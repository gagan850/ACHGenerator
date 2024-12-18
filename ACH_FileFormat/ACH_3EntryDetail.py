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
    
    def calculateCheckDigit(self, routingNumber):
        """
        Calculate the check digit for the routing number or return the 9th digit if it already exists.
        :param routingNumber: The routing number (8 or 9 digits)
        :return: The check digit (either provided or calculated)
        """
        if len(routingNumber) == 9:
            # If the routing number is 9 digits, return the 9th digit as the check digit
            return int(routingNumber[-1])
        elif len(routingNumber) == 8:
            # If the routing number is 8 digits, calculate the check digit
            # Weight factors for the routing number digits
            weights = [3, 7, 1] * 3  # Repeat the sequence [3, 7, 1] for all digits
            
            # Append a placeholder '0' for the check digit during the calculation
            routingNumber = routingNumber + "0"

            # Calculate the sum of the products
            sum_products = sum(int(digit) * weight for digit, weight in zip(routingNumber, weights))

            # Find the remainder when divided by 10
            remainder = sum_products % 10

            # Calculate the check digit
            check_digit = (10 - remainder) % 10
            return check_digit
        else:
            # If the routing number is not 8 or 9 digits, raise an error
            raise ValueError("Routing number must be 8 or 9 digits.")

    def generate(self):
        """
        Generate the formatted Entry Detail record.
        """
        record = RecordConfig(self.all_fields)
        values = {
            "Transaction Code"          : self.getTransaction(self.transactionType),
            "Receiving DFI"             : self.receivingBankRoutingNumber,
            "Check Digit"               : self.calculateCheckDigit(self.receivingBankRoutingNumber),
            "Receiver Account Number"   : self.receivingBankAccountNumber,
            "Amount"                    : self.formatAmount(self.amount),
            "Transaction Identifier"    : self.transactionIdentifier,
            "Receiving Company Name"    : self.receiverName,
            "Originating DFI"           : self.originatingBankRoutningNumber,
            "Entry Number"              : self.entryNumber
        }
        return record.generate(values)