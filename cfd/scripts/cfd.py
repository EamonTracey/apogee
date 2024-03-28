journal = open("journal_tui.jou").read()

journal_file = input("Journal file: ")

input_case_file = input("Input case file: ")
mach_number = input("Mach number: ")
temperature = input("Temperature (K): ")
iterations = input("Iterations: ")
output_report_file = input("Output report file: ")
output_case_file = input("Output case file: ")
output_data_file = input("Output data file: ")

journal = journal.replace("<INPUT CASE FILE>", input_case_file)
journal = journal.replace("<MACH NUMBER>", mach_number)
journal = journal.replace("<TEMPERATURE KELVIN>", temperature)
journal = journal.replace("<ITERATIONS>", iterations)
journal = journal.replace("<OUTPUT REPORT FILE>", output_report_file)
journal = journal.replace("<OUTPUT CASE FILE>", output_case_file)
journal = journal.replace("<OUTPUT DATA FILE>", output_data_file)

with open(journal_file, "w") as f:
    f.write(journal)
