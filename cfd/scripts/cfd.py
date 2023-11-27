journal = """; Read case file.
/file/read-case \"<INPUT CASE FILE>\"

; Enable energy equation.
/define/models/energy yes yes yes

; Set turbulence model to K-omega SST.
/define/models/viscous kw-sst yes

; Set air density to ideal gas.
/define/materials/change-create air air yes ideal-gas no no no no no no

; Define boundary conditions (mach number + temperature).
/define/boundary-conditions/pressure-far-field farfield no 0 no <MACH NUMBER> no <TEMPERATURE KELVIN> yes no 1 no 0 no 0 no no yes 5 10
/define/boundary-conditions/pressure-far-field inlet no 0 no <MACH NUMBER> no <TEMPERATURE KELVIN> yes no 1 no 0 no 0 no no yes 5 10
/define/boundary-conditions/pressure-far-field outlet no 0 no <MACH NUMBER> no <TEMPERATURE KELVIN> yes no 1 no 0 no 0 no no yes 5 10

; Make wall stationary and no slip.
/define/boundary-conditions/wall wall 0 no 0 no no no 0 no yes motion-bc-stationary yes shear-bc-noslip no no 0 no 0.5 no 1

; Make all methods second order.
/solve/set/discretization-scheme/pressure 12
/solve/set/discretization-scheme/density 1
/solve/set/discretization-scheme/mom 1
/solve/set/discretization-scheme/k 1
/solve/set/discretization-scheme/omega 1
/solve/set/discretization-scheme/temperature 1

; Create drag force report definition.
/solve/report-definitions add report-def-drag drag force-vector 1 0 0 scaled no thread-names wall , q
/solve/report-files add report-file-drag report-defs report-def-drag , file-name \"<OUTPUT REPORT FILE>\" q
/solve/report-plots add report-plot-drag report-defs report-def-drag , active yes q

; Disable convergence checks.
/solve/monitors/residual/check-convergence no no no no no no no

; Solve with many iterations.
/solve/initialize/set-defaults/x-velocity 200
/solve/initialize/initialize-flow
/solve/iterate <ITERATIONS>

; Write case and data files.
/file/write-case \"<OUTPUT CASE FILE>\"
/file/write-data \"<OUTPUT DATA FILE>\"
"""

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
