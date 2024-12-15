# ACH Generator

![ACH Generator](https://img.shields.io/static/v1?label=ach-generator&message=active&color=green)

is a Python-based utility designed to help you easily generate NACHA-compliant ACH files. Whether you prefer to input data via a user interface or through CSV files, this tool streamlines the process of creating ACH files for financial transactions.

![image](https://github.com/user-attachments/assets/4ac205f8-c9ed-4791-96fe-75087ecc7a0c)

---

## Table of Contents

- [User Base](#user-base)
- [How it Works](#how-it-works)
  - [User Interface](#user-interface)
  - [Terminal](#terminal)
- [Installation](#installation)
- [How to Execute](#how-to-execute)
- [Support](#support)

---

## 👤 User Base

This is designed to simplify the creation of NACHA-compliant ACH files for SMEs, Banks and financial institutions, We also provide tailored solutons for specific requirements. 


## How it Works

The ACH Generator provides two main ways to input transaction details:

### 📊 User Interface

The **User Interface** allows users to manually input transaction details for a single transaction. If multiple transactions need to be processed, a CSV file can be uploaded.

- **Manual Input**: Users can enter transaction details such as receiver's name, account number, and amount.
- **CSV Upload**: Users can upload a CSV file containing transaction data. The tool will automatically convert it into the proper format for ACH files.

#### Sender Details
Sender details can be configured using the "Company Details" tab:

<img width="797" alt="image" src="https://github.com/user-attachments/assets/9e8da29b-f1ae-43ad-bf06-373926f8b0c6" />

#### Receiver Details
Receiver details can be entered in the "ACH Generator" tab. Once the transaction is ready, clicking the "Generate ACH" button will generate the ACH file, which can then be downloaded.

![Receiver Details](https://github.com/user-attachments/assets/161c390d-4021-49b8-9a1f-a4befb9fcb8d)

###  💻 Terminal 

If you prefer working from the terminal, the ACH Generator also supports command-line operations. You can automate the generation of ACH files from CSVs via the terminal.

---

## 📦 Installation

To install the ACH Generator, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/gagan850/ACHGenerator.git
   ````
2. Install Python, Pip, PyQT5 (only if user interface is required)
   
   
## ⚙️ How to Execute
1. For User Interface:
   ```bash
   cd ACH Generator
   python3 main.py
   ````
2. For Terminal
   ```bash
   cd ACH Generator/ACH_Service
   python3 ACH_Generator.py
   ````

## 💬 Support
Please reach out at bansalgagandeep850@gmail.com in case any additional detail or support is required. This is already live for few SMEs, they are using it on regular basis.