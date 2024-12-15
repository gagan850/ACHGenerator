# Button Styles
error_buttonStyle = """
    QPushButton {
        background-color: #e74c3c;  /* Softer red */
        color: white;
        border: 1px solid #c0392b;
        border-radius: 8px;
        font-size: 14px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #f1948a;  /* Lighter red for hover */
    }
    QPushButton:pressed {
        background-color: #c0392b;  /* Darker red when pressed */
    }
"""

normal_buttonStyle = """
    QPushButton {
        background-color: #3498db;  /* Softer blue */
        color: white;
        border: 1px solid #2980b9;
        border-radius: 8px;
        font-size: 14px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #85c1e9;  /* Lighter blue for hover */
    }
    QPushButton:pressed {
        background-color: #2980b9;  /* Darker blue when pressed */
    }
"""

success_buttonStyle = """
    QPushButton {
        background-color: #6abf69;  /* Muted soft green */
        color: white;
        border: 1px solid #5aad59;
        border-radius: 8px;
        font-size: 14px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #7fcf7f;  /* Pastel green for hover */
    }
    QPushButton:pressed {
        background-color: #519e51;  /* Slightly darker soft green for pressed */
    }
"""