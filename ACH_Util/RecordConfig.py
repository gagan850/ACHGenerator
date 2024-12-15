class RecordConfig:
    def __init__(self, configs):
        # Store all fields, constant and variable
        self.configs = configs

    def generate(self, values):
        """
        Generate the record, combining constant and variable fields.
        :param values: Dictionary with field names as keys and their values (for variable fields).
        :return: The formatted record string.
        """
        record = ""
        for config in self.configs:
            if config.constant:
                # Use constant value for constant fields
                field_value = config.value
            else:
                # Get dynamic value for variable fields
                field_value = values.get(config.name, "")

            # Format the value based on configuration
            formatted_value = config.format_value(field_value)
            record += formatted_value
        return record
