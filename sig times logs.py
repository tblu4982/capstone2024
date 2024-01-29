import os
import re

sig_path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\sorted_log\plot_data\significant"
days = [f for f in os.listdir(sig_path) if os.path.isfile(os.path.join(sig_path, f))]

data_path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\sorted_log\plot_data"

for day in days:
    file_path1 = os.path.join(sig_path, day)
    file_path2 = os.path.join(data_path, day)
    save_file_path = os.path.join(sig_path, day.replace(".txt", ""))
    if not os.path.exists(save_file_path):
        os.makedirs(save_file_path)
    
    with open(file_path1, 'r') as sig_file:
        for line in sig_file:
            if re.search("[0-9]", line):
                events = []
                vehicle = ""
                with open(file_path2, 'r') as data_file:
                    event_start = False
                    for dataline in data_file:
                        if re.search("Vehicle", dataline):
                            vehicle = dataline
                            continue
                        if re.search("Time start", dataline):
                            time = re.split("\t", dataline)[0]
                            time = time[11:]
                            time = time[-11:].strip()

                            h, m = time.split(":")[0], time.split(":")[1]
                            am_pm = re.search("AM|PM", time).group()
                            
                            m = int(m)
                            m = m - (m % 10)
                            m = str(m)
                            if m == "0":
                                m = "00"
                            
                            time = f"{h}:{m} {am_pm}"
                       
                            if time == line.replace("\n", ""):
                                event_start = True
                                events.append(vehicle)
                                events.append(dataline)
                                continue
                        if event_start: 
                            if re.search("Time end", dataline):
                                events.append(dataline)
                                events.append('-\n')
                                event_start = False
                            elif not re.search("^-", dataline):
                                events.append(dataline)
                filename = line.replace(":", ".") + ".txt"
                filename = filename.replace("\n", "")
                this_save_file_path = os.path.join(save_file_path, filename)
                with open(this_save_file_path, 'w') as outfile:
                    for entry in events:
                        outfile.write(entry)