# Using regular expression to read log file
import re
import os
print(os.getcwd())
print(os.path.exists("samplelog.txt"))

reg_object = re.compile('[@:-]')

retValue = []
def read_log_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Using regex to split the line
            result = re.split('[@:-]', line)
            retValue.append(list(map(str.strip, result[1:])))
            
    return retValue
