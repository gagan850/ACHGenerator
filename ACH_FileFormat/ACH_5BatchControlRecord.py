import sys
import os

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ACH_Util.FieldConfig import FieldConfig
from ACH_Util.RecordConfig import RecordConfig
from ACH_Constant.Constant import PADDING_LEFT, PADDING_RIGHT

class ACH_BatchControlRecord:
    def __init__(self, entryAddendaCount, entryHash, totalDebitAmount, totalCreditAmount, companyId, originatingBankRoutingNumber, batchNumber):
        """
        Initializes the Batch Control Record object.

        :param entryAddendaCount: Total number of entry and addenda records in this batch (6 digits).
        :param entryHash: Hash total of the first 8 digits of all routing numbers in the batch (10 digits).
        :param totalDebitAmount: Total debit amount in cents (12 digits).
        :param totalCreditAmount: Total credit amount in cents (12 digits).
        :param companyId: Same as Batch Header company_id (10 digits).
        :param originatingBankRoutingNumber: First 8 digits of the originating bank’s routing number.
        :param batchNumber: Same as Batch Header batch number (7 digits).
        """

        # Variables (Detail from CSV)
        self.entryAddendaCount             = entryAddendaCount
        self.entryHash                     = entryHash
        self.totalDebitAmount              = totalDebitAmount
        self.totalCreditAmount             = totalCreditAmount
        self.companyId                     = companyId
        self.originatingBankRoutingNumber  = originatingBankRoutingNumber
        self.batchNumber                   = batchNumber
        
        # Define all field configurations for the header
        self.all_fields = [             
            FieldConfig(name="Record Type Code",                length=1,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="8"),
            FieldConfig(name="Service Class Code",              length=3,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=True, value="200"),
            FieldConfig(name="Entry/Addenda Count",             length=6,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Entry Hash",                      length=10,  padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Total Debit Entry Dollar Amount", length=12,  padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Total Credit Entry Dollar Amount",length=12,  padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Company ID",                      length=10,  padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),   
            FieldConfig(name="Reserved",                        length=19,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True,  value=""),
            FieldConfig(name="Reserved",                        length=6,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=True,  value=""),
            FieldConfig(name="Originating DFI Identification",  length=8,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Batch Number",                    length=7,   padding=PADDING_LEFT,   fillChar="0",       mandatory=True,    constant=False) 
        ]
        
    def generate(self):
        """
        Generate the formatted Batch Control Record.
        """
        record = RecordConfig(self.all_fields)
        values = {
            "Entry/Addenda Count"               : self.entryAddendaCount,
            "Entry Hash"                        : self.entryHash,
            "Total Debit Entry Dollar Amount"   : self.totalDebitAmount,
            "Total Credit Entry Dollar Amount"  : self.totalCreditAmount,
            "Company ID"                        : self.companyId,
            "Originating DFI Identification"    : self.originatingBankRoutingNumber,
            "Batch Number"                      : self.batchNumber
        }
        return record.generate(values)

# Example Usage
if __name__ == "__main__":
    batch_control   = ACH_BatchControlRecord(
        entryAddendaCount               = 5,  # Total of 5 entries/addenda in the batch
        entryHash                       = 123456789,  # Hash total of routing numbers
        totalDebitAmount                = 10000,  # Total debit amount in cents ($100.00)
        totalCreditAmount               = 5000,  # Total credit amount in cents ($50.00)
        companyId                       = "1522206279",  # Company ID
        originatingBankRoutingNumber    = "06100010",  # Originating DFI Routing Number
        batchNumber                     = 1  # Batch number
    )
    print(batch_control.generate())
