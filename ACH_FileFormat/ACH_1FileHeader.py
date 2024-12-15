import sys
import os

# Add the parent directory of the current file to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from ACH_Util.FieldConfig import FieldConfig
from ACH_Util.RecordConfig import RecordConfig
from ACH_Constant.Constant import PADDING_LEFT, PADDING_RIGHT


class ACH_FileHeader:
    """
    Represents the ACH File Header (Record Type 1).
    This class handles the creation and formatting of the file header.
    """

    def __init__(self, immediateOrigin, immediateOriginRoutingNumber, immediateDestination, immediateDestinationRoutingNumber, reference=""):
        """
        Initialize the file header with required user-provided information.

        :param immediateOrigin: Name of the sender (e.g., company)
        :param immediateOriginRoutingNumber: Sender's routing number        
        :param immediateDestination: Name of the receiver (e.g., bank or institution)
        :param immediateDestinationRoutingNumber: Receiver's routing number
        :param reference: Optional reference code for the file
        """

        # Variables (Detail from CSV)
        self.immediateOrigin                    = immediateOrigin
        self.immediateDestination               = immediateDestination
        self.immediateOriginRoutingNumber       = immediateOriginRoutingNumber
        self.immediateDestinationRoutingNumber  = immediateDestinationRoutingNumber
        self.reference                          = reference

        # Define all field configurations for the header
        self.all_fields = [
            FieldConfig(name="Record Type Code",            length=1,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="1"),
            FieldConfig(name="Priority Code",               length=2,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=True, value="01"),
            FieldConfig(name="Blank Space",                 length=1,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=True, value=""),
            FieldConfig(name="Immediate Destination",       length=9,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),      # Variable
            FieldConfig(name="Blank Space",                 length=1,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=True, value=""),
            FieldConfig(name="Immediate Origin",            length=9,   padding=PADDING_LEFT,    fillChar=" ",       mandatory=True,    constant=False),      # Variable
            FieldConfig(name="File Creation Date",          length=6,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value=datetime.now().strftime('%y%m%d')),
            FieldConfig(name="File Creation Time",          length=4,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value=datetime.now().strftime('%H%M')),
            FieldConfig(name="File ID Modifier",            length=1,   padding=PADDING_RIGHT,   fillChar="A",       mandatory=True,    constant=True, value="A"),
            FieldConfig(name="Record Size",                 length=3,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="094"),
            FieldConfig(name="Blocking Factor",             length=2,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="10"),
            FieldConfig(name="Format Code",                 length=1,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=True, value="1"),
            FieldConfig(name="Immediate Destination Name",  length=23,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),      # Variable
            FieldConfig(name="Immediate Origin Name",       length=23,  padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False),      # Variable
            FieldConfig(name="Reference Code",              length=8,   padding=PADDING_RIGHT,   fillChar=" ",       mandatory=True,    constant=False)       # Variable
        ]

    def generate(self):
        """
        Generate the formatted ACH file header string.
        :return: Formatted ACH file header
        """
        # Create a RecordConfig object to generate the formatted header
        record = RecordConfig(self.all_fields)
        values = {
            "Immediate Destination"     : self.immediateDestinationRoutingNumber,
            "Immediate Origin"          : self.immediateOriginRoutingNumber,
            "Immediate Destination Name": self.immediateDestination,
            "Immediate Origin Name"     : self.immediateOrigin,
            "Reference Code"            : self.reference
        }
        return record.generate(values)
