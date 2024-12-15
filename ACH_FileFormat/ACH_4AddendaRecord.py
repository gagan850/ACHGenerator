class ACH_AddendaRecord:
    def __init__(self, paymentRelatedInfo, addendaSequenceNumber, entryDetailSequenceNumber):
        """
        Initializes the Addenda Record object.

        :param paymentRelatedInfo: Payment-related information (up to 80 characters).
        :param addendaSequenceNumber: Sequence number for multiple addenda records (4 digits).
        :param entryDetailSequenceNumber: Last 7 digits of the associated Entry Detail record's trace number.
        """
        
        # Variables (Detail from CSV)
        self.payment_related_info           = paymentRelatedInfo[:80].ljust(80)  # Truncate or pad to 80 characters
        self.addenda_sequence_number        = str(addendaSequenceNumber).zfill(4)  # Ensure 4 digits
        self.entry_detail_sequence_number   = str(entryDetailSequenceNumber).zfill(7)  # Ensure 7 digits
        
        # Constants
        self.record_type_code   = "7"
        self.addenda_type_code  = "05"  # Standard addenda type for payment-related information

    def generate(self):
        """
        Generate the formatted Addenda Record.
        """
        return (
            f"{self.record_type_code}{self.addenda_type_code}{self.payment_related_info}"
            f"{self.addenda_sequence_number}{self.entry_detail_sequence_number}"
        )

# Example Usage
if __name__ == "__main__":
    # Example data
    paymentRelatedInfo          = "Invoice 12345 Payment"
    addendaSequenceNumber       = 1
    entryDetailSequenceNumber   = 1234567

    # Create AddendaRecord object
    addenda_record = ACH_AddendaRecord(
        paymentRelatedInfo          = paymentRelatedInfo,
        addendaSequenceNumber       = addendaSequenceNumber,
        entryDetailSequenceNumber   = entryDetailSequenceNumber
    )

    # Generate and print the Addenda Record
    print(addenda_record.generate())
