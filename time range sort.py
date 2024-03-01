import os
import re
import shutil

path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\RuleHarshBrakingId\filtered"
dest_path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\sorted_log\custom"

if os.path.exists(dest_path):
    shutil.rmtree(dest_path)
os.makedirs(dest_path)
dest1 = os.path.join(dest_path, "Fall 2022")
os.makedirs(dest1)
dest1 = os.path.join(dest_path, "Fall 2023")
os.makedirs(dest1)

bcount = acount = 0

event_logs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for file in event_logs:
    file_path = os.path.join(path, file)
    
    event = []
    
    with open(file_path, 'r') as myfile:
        sem = None
        for line in myfile:
            if re.search("Vehicle", line):
                event.append(line)
                continue
            elif line == "-\n":
                if bool(sem):
                    dest1 = os.path.join(dest_path, sem)
                    outfile_path = os.path.join(dest1, file)
                    if os.path.exists(outfile_path):
                        with open(outfile_path, 'a') as outfile:
                            for line in event:
                                outfile.write(line)
                            outfile.write("-\n")
                    else:
                        with open(outfile_path, 'w') as outfile:
                            for line in event:
                                outfile.write(line)
                            outfile.write("-\n")
                event.clear()
                sem = None
            else:
                event.append(line)
                if re.search("[0-9]+/[0-9]+/[0-9]{4}", line) and not bool(sem):
                    date = re.search("[0-9]+/[0-9]+/[0-9]{4}", line).group()
                    month, day, year = date.split("/")
                    month = int(month)
                    day = int(day)
                    year = int(year)
                    if year >= 2022:
                        if month >= 8 and month <= 12:
                            if month == 8 and day >= 16 or month >= 8:
                                if year == 2022:
                                    sem = "before"
                                    bcount += 1
                                elif year == 2023:
                                    sem = "after"
                                    acount += 1
                        
print(f"Before:\t{bcount}\nAfter:\t{acount}")