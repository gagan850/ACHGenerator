import sys
import os

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from ACH_Util.FieldConfig import FieldConfig
from ACH_Util.RecordConfig import RecordConfig
from ACH_Constant.Constant import PADDING_LEFT, PADDING_RIGHT


class ACH_BatchHeader:
    def __init__(self, transactionType, companyName, companyId, standardEntryClassCode, entryDescription, effectiveTransactionDate, originatingBankRoutningNumber, batchNumber):
        """
        Initializes the Batch Header object.
        
        :param transactionType: Type of transactions (200=Mixed, 220=Credit, 225=Debit).
        :param companyName: Name of the company (16 characters max).
        :param companyId: Unique company ID (10 digits, e.g., EIN).
        :param standardEntryClassCode: Standard Entry Class Code (e.g., PPD, CCD).
        :param entryDescription: Description of the batch (10 characters max).
        :param effectiveTransactionDate: Date when transactions should occur (YYMMDD format).
        :param originatingBankRoutningNumber: Routing number of originating bank (first 8 digits).
        :param batchNumber: Unique batch number (7 digits).
        """

        # Variables (Detail from CSV)
        self.transactionType                = transactionType
        self.companyName                    = companyName
        self.companyId                      = companyId
        self.standardEntryClassCode         = standardEntryClassCode
        self.entryDescription               = entryDescription
        self.effectiveTransactionDate       = effectiveTransactionDate
        self.originatingBankRoutningNumber  = originatingBankRoutningNumber
        self.batchNumber                    = batchNumber

        # Define all field configurations for the header
        self.all_fields = [
            FieldConfig(name="Record Type Code",            length=1,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="5"),
            FieldConfig(name="Service Class Code",          length=3,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),
            FieldConfig(name="Company Name",                length=16,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),
            FieldConfig(name="Company Discretionary Data",  length=20,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False, value=""),
            FieldConfig(name="Company Id",                  length=10,  padding=PADDING_RIGHT,   fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Standard Entry Class Code",   length=3,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),
            FieldConfig(name="Company Entry Description",   length=10,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),   
            FieldConfig(name="Company Descriptive Date",    length=6,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=True, value=datetime.now().strftime('%y')),   
            FieldConfig(name="Effective Entry Date",        length=6,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value=datetime.now().strftime('%y%m%d')),
            FieldConfig(name="Settlement Date",             length=3,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=True, value=""), 
            FieldConfig(name="Originator Status Code",      length=1,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="1"),
            FieldConfig(name="Originating DFI",             length=8,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),
            FieldConfig(name="Batch Number",                length=7,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
        ]
    
    
    def getServiceClassCode(self, transactionType):
        """
        Determines the service class code based on the transaction type.
        :return: Service class code (string)
        """
        if transactionType == 'Credit':
            return '220'
        elif transactionType == 'Debit':
            return '225'
        else:
            return '200'  # Default to Mixed if transaction type isn't explicitly Credit or Debit

    def generate(self):
        """
        Generate the formatted Batch Header record.
        """
        # Create a RecordConfig object to generate the formatted header
        record = RecordConfig(self.all_fields)
        values = {
            "Service Class Code"        : self.getServiceClassCode('MIX'),  # Receiver's bank routing number (variable)
            "Company Name"              : self.companyName,  # Sender's EIN or routing number (variable)
            "Company Id"                : self.companyId,  # Receiver's bank name (variable)
            "Standard Entry Class Code" : self.standardEntryClassCode,  # Sender's company name (variable)
            "Company Entry Description" : self.entryDescription,
            "Originating DFI"           : self.originatingBankRoutningNumber,
            "Batch Number"              : self.batchNumber
        }
        return record.generate(values)
    
# Example usage
if __name__ == "__main__":
    # Define example data
    transactionType                 = "Credit"  # Mixed debits/credits
    companyName                     = "WIS/WEM LLC" #Company Name
    companyId                       = "1522206279" #COMPANY ID
    standardEntryClassCode          = "PPD"
    entryDescription                = "VENDOR"
    effectiveTransactionDate        = "      " #datetime.now().strftime('%y%m%d')  #Effeective transaction date
    originatingBankRoutningNumber   = "24090924" #COMPANY BANK ROUTING NUMBER
    batchNumber                     = "1"

    # Create BatchHeader object
    batch_header = ACH_BatchHeader(
        transactionType                 = transactionType,
        companyName                     = companyName,
        companyId                       = companyId,
        standardEntryClassCode          = standardEntryClassCode,
        entryDescription                = entryDescription,
        effectiveTransactionDate        = effectiveTransactionDate,
        originatingBankRoutningNumber   = originatingBankRoutningNumber,
        batchNumber                     = batchNumber
    )

    # Generate and print the Batch Header record
    print(batch_header.generate())
