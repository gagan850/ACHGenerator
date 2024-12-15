# YourScriptFolder/main.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from ACH_UI.CompanyDetailsTab import CompanyDetailsTab
from ACH_UI.ACHGeneratorTab import ACHGeneratorTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('ACH Generation Tool')
        self.setGeometry(100, 100, 800, 600)

        # Create QTabWidget
        self.tabs = QTabWidget(self)
        
        # Create the tabs and add to QTabWidget
        self.company_details_tab = QWidget()
        self.ach_generator_tab = QWidget()

        self.tabs.addTab(self.company_details_tab, 'Company Details')
        self.tabs.addTab(self.ach_generator_tab, 'ACH Generator')

        # Initialize and set up the tabs
        self.company_details_tab_widget = CompanyDetailsTab(self.company_details_tab)
        self.ach_generator_tab_widget = ACHGeneratorTab(self.ach_generator_tab)

        self.tabs.setCurrentIndex(0)
        # Set layout for the main window
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
