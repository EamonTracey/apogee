import os

JOB = """#!/bin/bash
#$ -M etracey@nd.edu
#$ -m abe
#$ -q long
#$ -pe mpi-24 24
#$ -N <NAME>
#$ -cwd
#$ -v DISPLAY

module load ansys/2023R1

unset noclobber

fluent 3ddp -t1 -g < <JOURNAL FILE> > <LOG FILE>
"""

SCRIPT = "/afs/crc.nd.edu/user/e/etracey/cfd/scripts/cfd.py"
JOURNALS_DIRECTORY = "/afs/crc.nd.edu/user/e/etracey/cfd/journals"
JOBS_DIRECTORY = "/afs/crc.nd.edu/user/e/etracey/cfd/jobs"
RESULTS_DIRECTORY = "/afs/crc.nd.edu/user/e/etracey/cfd/results"
INPUT_CASE = "/afs/crc.nd.edu/user/e/etracey/cfd/models/rocket_<DEGREE>deg.cas.h5"

degrees = ["0", "25", "35", "40"]
mach_numbers = ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6"]
temperatures = ["265", "295"]
iterations = "1000"

for degree in degrees:
    for mach_number in mach_numbers:
        for temperature in temperatures:
            input_case_file = INPUT_CASE.replace("<DEGREE>", degree)
            name = f"{degree}_{mach_number}_{temperature}"
            journal_file = f"{JOURNALS_DIRECTORY}/journal_{name}.jou"
            job_file = f"{JOBS_DIRECTORY}/job_{name}.job"
            log_file = f"{JOBS_DIRECTORY}/log_{name}.log"
            output_report_file = f"{RESULTS_DIRECTORY}/report_{name}"
            output_case_file = f"{RESULTS_DIRECTORY}/case_{name}"
            output_data_file = f"{RESULTS_DIRECTORY}/data_{name}"

            script_input = "\n".join([
                journal_file,
                input_case_file,
                mach_number,
                temperature,
                iterations,
                output_report_file,
                output_case_file,
                output_data_file
            ])
            script_input += "\n"

            with open(".script_input", "w") as f:
                f.write(script_input)
            os.system(f"python3 {SCRIPT} < .script_input")
            os.remove(".script_input")

            job = JOB.replace("<NAME>", "etracey_" + name).replace("<JOURNAL FILE>", journal_file).replace("<LOG FILE>", log_file)
            with open(job_file, "w") as f:
                f.write(job)

