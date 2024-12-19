# ACH_UI.py
import os,sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ACH_UI.CompanyDetailsTab import CompanyDetailsTab
from ACH_UI.ACHGeneratorTab import ACHGeneratorTab

def uiLauncher():
    """Starts the PyQt5 GUI for ACH Generation."""
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle('ACH Generation Tool')
    window.setGeometry(100, 100, 800, 600)

    tabs = QTabWidget(window)
    company_details_tab = QWidget()
    ach_generator_tab = QWidget()

    tabs.addTab(company_details_tab, 'Company Details')
    tabs.addTab(ach_generator_tab, 'ACH Generator')

    company_details_tab_widget = CompanyDetailsTab(company_details_tab)
    ach_generator_tab_widget = ACHGeneratorTab(ach_generator_tab)

    tabs.setCurrentIndex(0)
    
    layout = QVBoxLayout()
    layout.addWidget(tabs)
    window.setLayout(layout)

    window.show()
    app.exec_()
