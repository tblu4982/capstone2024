import os
import re
import shutil
import sys

path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\log\filtered"
dest_path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\sorted_log\speed_filtered"

if os.path.exists(dest_path):
    shutil.rmtree(dest_path)
os.makedirs(dest_path)

event_logs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for file in event_logs:
    file_path = os.path.join(path, file)
    
    event = []
    
    with open(file_path, 'r') as myfile:
        sem = None
        vi = vf = 0
        for line in myfile:
            if re.search("Vehicle", line):
                event.append(line)
                continue
            elif line == "-\n":
                for row in event:
                    if re.search("Speed: [0-9]+.[0-9]*", row):
                        speed = re.search("Speed: [0-9]+.[0-9]*", row).group()
                        speed = float(speed[7:])
                        if vi == 0:
                            vi = speed
                        else:
                            vf = speed
                if vi - 10 >= vf:
                    if file == "V0465.txt":
                        print(vi)
                        print(vf)
                        print(event)
                    outfile_path = os.path.join(dest_path, file)
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
                vi = 0
                vf = 0
                event.clear()
            else:
                event.append(line)
                    