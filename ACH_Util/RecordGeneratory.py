import sys
import os

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FieldConfig import FieldConfig
from RecordConfig import RecordConfig
from ACH_Constant.Constant import PADDING_LEFT, PADDING_RIGHT

if __name__ == "__main__":
    values = {
        "Service Class Code": "220",  # Receiver's bank routing number (variable)
        "Company Name": "WIS/WEM LLC",  # Sender's EIN or routing number (variable)
        "Company Id": "522206279",  # Receiver's bank name (variable)
        "Standard Entry Class Code": "PPD",  # Sender's company name (variable)
        "Entry Description" :"VENDOR",
        "Originating DFI":"24090924",
        "Batch Number":"1",
    }
    
    all_fields = [             
        FieldConfig(name="Record Type Code",            length=1,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="6"),
        FieldConfig(name="Transaction Code",            length=2,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),
        FieldConfig(name="Receiving DFI",               length=8,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),
        FieldConfig(name="Check Digit",                 length=1,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),
        FieldConfig(name="Receiver Account Number",     length=17,  padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),
        FieldConfig(name="Amount",                      length=10,  padding=PADDING_RIGHT,   fillChar="0",       mandatory=True,    constant=False),
        FieldConfig(name="Transaction Identifier",      length=15,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),   
        FieldConfig(name="Receiving Company Name",      length=22,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),
        FieldConfig(name="Entry Number",                length=15,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False) 
    ]
    record = RecordConfig(all_fields)
    formatted_record= record.generate(values)
    print(formatted_record)