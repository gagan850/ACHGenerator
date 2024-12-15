class FieldConfig:
    def __init__(self, name, length, padding="right", fillChar=" ", mandatory=True, constant=False, value=None):
        self.name       = name
        self.length     = length
        self.padding    = padding
        self.fillChar   = fillChar
        self.mandatory  = mandatory
        self.constant   = constant
        self.value      = value

    def format_value(self, value=None):
        """
        Formats the field value based on the configuration.
        :param value: The input value to format.
        :return: The formatted value as a string.
        """
        if self.constant:
            value = self.value
        elif value is None:
            if self.mandatory:
                raise ValueError(f"Mandatory field '{self.name}' is missing.")
            value = ""
        else:
            value = str(value)[:self.length]  # Truncate if too long

        if self.padding == "left":
            value = value.rjust(self.length, self.fillChar)
        elif self.padding == "right":
            value = value.ljust(self.length, self.fillChar)
            
        return value.upper()
