import os
import re

paths = []
paths.append(r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\sorted_log\custom\before")
paths.append(r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\sorted_log\custom\after")

for path in paths:
    print(path[-9:])
    count = 0
    event_logs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in event_logs:
        file_path = os.path.join(path, file)
        with open(file_path, 'r') as myfile:
            for line in myfile:
                if re.search("Vehicle", line):
                    count += 1
    print(f"Total Count: {count}")
        