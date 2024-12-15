import sys
import os

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ACH_Util.FieldConfig import FieldConfig
from ACH_Util.RecordConfig import RecordConfig
from ACH_Constant.Constant import PADDING_LEFT, PADDING_RIGHT

class ACH_FileControlRecord:
    def __init__(self, batchCount, blockCount, entryAddendaCount, entryHash, totalDebitAmount, totalCreditAmount):
        """
        Initializes the File Control Record object.

        :param batchCount: Total number of batches in the file (6 digits).
        :param blockCount: Total number of 10-record blocks in the file (6 digits).
        :param entryAddendaCount: Total number of entry and addenda records in the file (8 digits).
        :param entryHash: Hash total of the first 8 digits of all routing numbers in the file (10 digits).
        :param totalDebitAmount: Total debit dollar amount in cents (12 digits).
        :param totalCreditAmount: Total credit dollar amount in cents (12 digits).
        """
        
        # Variables (Detail from CSV)
        self.batchCount           = batchCount
        self.blockCount           = blockCount
        self.entryAddendaCount    = entryAddendaCount
        self.entryHash            = entryHash
        self.totalDebitAmount     = totalDebitAmount
        self.totalCreditAmount    = totalCreditAmount

        # Define all field configurations for the header
        self.all_fields = [             
            FieldConfig(name="Record Type Code",                length=1,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="9"),
            FieldConfig(name="Batch Count",                     length=6,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=True, value="1"),
            FieldConfig(name="Block Count",                     length=6,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=True, value="1"),
            FieldConfig(name="Entry/Addenda Count",             length=8,   padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Entry Hash",                      length=10,  padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Total Debit Entry Dollar Amount", length=12,  padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Total Credit Entry Dollar Amount",length=12,  padding=PADDING_LEFT,    fillChar="0",       mandatory=True,    constant=False),
            FieldConfig(name="Reserved",                        length=39,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True,  value="")
        ]
        
    def generate(self):
        """
        Generate the formatted File Control Record.
        """
        record = RecordConfig(self.all_fields)
        values = {
            "Batch Count"                       : self.batchCount,
            "Block Count"                       : self.blockCount,
            "Entry/Addenda Count"               : self.entryAddendaCount,
            "Entry Hash"                        : self.entryHash,
            "Total Debit Entry Dollar Amount"   : self.totalDebitAmount,
            "Total Credit Entry Dollar Amount"  : self.totalCreditAmount,
        }
        return record.generate(values)
