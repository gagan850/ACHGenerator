import sys, os, csv
from datetime import datetime
from ACH_UI.Launcher import uiLauncher
from ACH_Service.ACH_Generator import ACHFileGenerator

def main():
    # Check if CSV processing is requested
    if len(sys.argv) > 1 and sys.argv[1] == '--csv' and len(sys.argv) > 2:
        csv_file_path = sys.argv[2]
        
        if not os.path.isfile(csv_file_path):
            print(f"Error: The specified file '{csv_file_path}' does not exist.")
        elif not csv_file_path.endswith('.csv'):
            print(f"Error: The file '{csv_file_path}' is not a CSV file. Please provide a valid CSV file.")
        else:
            # Process the ACH generation from CSV and directly generate ACH
            records = []
            with open(csv_file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    records.append(row)
            # Print CSV Records
            #print(records)
            
            # Generate ACH
            ach_generator = ACHFileGenerator(records)
            achResponsePayload = ach_generator.generate()
            
            # Extract the directory from the provided CSV file path
            file_directory = os.path.dirname(csv_file_path)
            
            # Save the ACH file in the same directory as the CSV file
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
            ach_filename = f"{formatted_datetime}.txt"
            ach_file_path = os.path.join(file_directory, ach_filename)
            
            # Write the ACH response payload to the file
            with open(ach_file_path, 'w') as file:
                file.write(achResponsePayload)
            
            print(f"ACH file has been saved at: {ach_file_path}")
    
    else:
        # If no arguments or UI mode is requested, start the GUI
        uiLauncher()

if __name__ == "__main__":
    main()
