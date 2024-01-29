import re
import os
import sys
import shutil
from datetime import datetime as dt
from geopy.distance import geodesic

def get_day_of_week (date):
    #returns an integer from 0 to 6, with 0 being Monday and 6 being Sunday
    date = date.weekday()

    if date == 0:
        return "Monday"
    elif date == 1:
        return "Tuesday"
    elif date == 2:
        return "Wednesday"
    elif date == 3:
        return "Thursday"
    elif date == 4:
        return "Friday"
    elif date == 5:
        return "Saturday"
    elif date == 6:
        return "Sunday"

#Path to source data 1
path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\log"
#scan file directory to create a python list that contains all file names
event_logs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

#Path to source data 2
#Currently unused
path2 = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\log\other"
event_logs2 = [f for f in os.listdir(path2) if os.path.isfile(os.path.join(path2, f))]

#Destination path for sorted files, arranged by year, month, and time, and hour
path3 = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\sorted_log"
if os.path.exists(path3):
    shutil.rmtree(path3)

#Destination path for sorted files, arranged by day of the week
path4 = os.path.join(path3, "plot_data")

path5 = os.path.join(path, "filtered")

#delete existing directory for path 4
if os.path.exists(path4):
    shutil.rmtree(path4)
os.makedirs(path4)

if os.path.exists(path5):
    shutil.rmtree(path5)
os.makedirs(path5)
    
#counts for total number of events and total events per weekday, respectively
tcount = 0
count = 0
print("Program is running, please wait...")

#scan through each file for events
for file in event_logs:
    file_path = os.path.join(path, file)
    myfile = open(file_path)
    #list that holds event data while it is being constructed
    event = []
    #placeholders that will hold file locations for the two destination paths listed above
    new_path3 = new_path4 = ""
    hour = ""
    #holds latitude, longitude, and speeds for distance/acceleration calculations
    lat1 = lat2 = long1 = long2 = speed1 = speed2 = ""
    
    #markers to signify the start and end of an exception event
    event_start = False
    event_end = True
    #scan through text in file
    for line in myfile:
        #signifies the start of an event
        if re.search("Event", line):
            event_start = True
            tcount += 1
            event.append("Vehicle: " + file[:5] + '\n')
            continue
        #gets time information from event and generates destination file paths
        if re.search("Time start:", line):
            event.append(line)
            #find date in line
            date = re.search("[0-9]+/[0-9]+/[0-9]{4}", line).group()
            
            #find time in line
            time = re.split("\t", line)[0]
            #trim line to get the time
            time = time[11:]
            time = time[-11:]

            #extract month, day, and year from time
            month, day, year = re.split("/", date)

            #get hour from time
            hour = re.split(":", time)[0] + " " + re.search("AM|PM", time).group()
            
            #convert date to datetime formate
            date_as_dt = date = dt(int(year), int(month), int(day))
            #get month as string
            month_text = date_as_dt.strftime("%B")
            #get day of the week from date
            day_of_week = get_day_of_week(date_as_dt) + ".txt"

            #find initial latitude, longitude, and speed in line
            lat1 = float(re.search("Latitude: -?[0-9]+.[0-9]+", line).group()[10:])
            long1 = float(re.search("Longitude: -?[0-9]+.[0-9]+", line).group()[11:])
            speed1 = re.search("Speed: [0-9]+.[0-9]+|Speed: [0-9]+", line).group()
            
            #build root destination path if it doesn't exist
            if not os.path.exists(path3):
                os.makedirs(path3)
    
            #build year destination path
            new_path3 = os.path.join(path3, year)
            if not os.path.exists(new_path3):
                os.makedirs(new_path3)

            #build month destination path
            new_path3 = os.path.join(new_path3, month_text)
            if not os.path.exists(new_path3):
                os.makedirs(new_path3)

            #build day destination path
            new_path3 = os.path.join(new_path3, day)
            if not os.path.exists(new_path3):
                os.makedirs(new_path3)

            #build day of the week destination path
            new_path4 = os.path.join(path4, day_of_week)
            continue
        #for every line after time start for event and before new event
        elif event_start and not re.search("Event", line):
            #this signifies end of an event
            if re.search("Time end:", line):
                event_start = False
                event.append(line)
                
                #store final latitude, longitude, and speed from line
                lat2 = float(re.search("Latitude: -?[0-9]+.[0-9]+", line).group()[10:])
                long2 = float(re.search("Longitude: -?[0-9]+.[0-9]+", line).group()[11:])
                speed2 = re.search("Speed: [0-9]+.[0-9]+|Speed: [0-9]+", line).group()

                #ignore event if initial and final data is the same
                if lat1 == lat2 and long1 == long2 and speed1 == speed2:
                    event.clear()
                    continue
                #calculate the distance (currently unused)
                else:
                    pos1 = (lat1, long1)
                    pos2 = (lat2, long2)
                    distance = geodesic(pos1, pos2).m
                    event_end = True
                    continue
            #end of event signifier
            #if we reach this, then there was no time end for recorded event, ignore data
            if re.search("^-", line):
                event_start = False
                event.clear()
                continue
            #for all other points between time start and end
            else:
                event.append(line)
        #begin writing event to file
        if event_end:
            event_end = False
            #increment count for day of week
            count += 1
            #first, save to destination path 3
            #set filename for hour event occured
            filename = hour + ".txt"
            sorted_path = os.path.join(new_path3, filename)
            with open(sorted_path, 'a') as outfile:
                #write event to file
                for row in event:
                    outfile.write(row)
                outfile.write("-\n")

            #second, save to destination path 4
            try:
                #append to existing file if it exists
                if os.path.exists(new_path4):
                    with open(new_path4, 'a') as outfile:
                        for row in event:
                            outfile.write(row)
                        outfile.write("-\n")
                #create file if it doesn't exist
                else:
                    with open(new_path4, 'w') as outfile:
                        for row in event:
                            outfile.write(row)
                        outfile.write("-\n")
            except FileNotFoundError:
                pass
            filename = os.path.join(path5, file)
            if bool(event):
                try:
                    if os.path.exists(filename):
                        with open(filename, 'a') as outfile:
                            for row in event:
                                outfile.write(row)
                            outfile.write("-\n")
                    else:
                        with open(filename, 'w') as outfile:
                            for row in event:
                                outfile.write(row)
                            outfile.write("-\n")
                except FileNotFoundError:
                    pass
            event.clear()
        

print("Total events: " + str(tcount))
print("Total events after filter: " + str(count))
print("Program Complete!")
