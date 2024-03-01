import matplotlib.pyplot as plt
import os
import re
import sys
import math

def get_day_of_week (date):
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
    
def sort_dict(hours, option):
    sorted_hours = {}
    
    while bool(hours):
        hour_list = list(hours.keys())
        min_hour = ""
        min_h_as_mil = ""
        for hour in hour_list:
            if min_hour == "":
                min_hour = hour
                continue
            else:
                m = ""
                h, am_pm = min_hour.strip().split(" ")
                if option == 2:
                    m = h.split(":")[1]
                    h = h.split(":")[0]
                #after prior modifications, m should now hold hour and minutes (hh:mm)
                #add code here that separates m into hour and minutes
                if am_pm == "PM":
                    #multiply m by 60 before storing
                    if h == "12":
                        min_h_as_mil = int(h)
                    else:
                        min_h_as_mil = int(h) + 12
                else:
                    if h == "12":
                        min_h_as_mil = 0
                    else:
                        min_h_as_mil = int(h)
                        
                if option == 2:
                    min_h_as_mil = min_h_as_mil * 60 + int(m)
                
                #add minutes to newly stored min_h variable
                    
                h, am_pm = hour.strip().split(" ")
                if option == 2:
                    m = h.split(":")[1]
                    h = h.split(":")[0]
                #repeat the above process here as well
                if am_pm == "PM":
                    if h == "12":
                        h_as_mil = int(h)
                    else:
                        h_as_mil = int(h) + 12
                else:
                    if h == "12":
                        h_as_mil = 0
                    else:
                        h_as_mil = int(h)
                        
                if option == 2:
                    h_as_mil = h_as_mil * 60 + int(m)
                    
                if h_as_mil < min_h_as_mil:
                    min_hour = hour
                    min_h_as_mil = h_as_mil

        sorted_hours[min_hour] = hours.pop(min_hour)
        
    return sorted_hours

def add_zeroes(hours):
    h = 0
    m = 0
    am_pm = ""
    mn = ""
    hr = ""
    
    while h <= 23 and m <= 50:
        if h >= 12:
            if h >= 18:
                if h >= 21:
                    if h == 21:
                        hr = "9"
                        am_pm = "PM"
                    elif h == 22:
                        hr = "10"
                        am_pm = "PM"
                    elif h == 23:
                        hr = "11"
                        am_pm = "PM"
                elif h == 18:
                    hr = "6"
                    am_pm = "PM"
                elif h == 19:
                    hr = "7"
                    am_pm = "PM"
                elif h == 20:
                    hr = "8"
                    am_pm = "PM"
            elif h >= 15:
                if h == 15:
                    hr = "3"
                    am_pm = "PM"
                elif h == 16:
                    hr = "4"
                    am_pm = "PM"
                elif h == 17:
                    hr = "5"
                    am_pm = "PM"
            elif h == 12:
                hr = "12"
                am_pm = "PM"
            elif h == 13:
                hr = "1"
                am_pm = "PM"
            elif h == 14:
                hr = "2"
                am_pm = "PM"
        elif h >= 6:
            if h >= 9:
                if h == 9:
                    hr = "9"
                    am_pm = "AM"
                if h == 10:
                    hr = "10"
                    am_pm = "AM"
                if h == 11:
                    hr = "11"
                    am_pm = "AM"
            elif h == 6:
                hr = "6"
                am_pm = "AM"
            elif h == 7:
                hr = "7"
                am_pm = "AM"
            elif h == 8:
                hr = "8"
                am_pm = "AM"
        elif h >= 3:
            if h == 3:
                hr = "3"
                am_pm = "AM"
            elif h == 4:
                hr = "4"
                am_pm = "AM"
            elif h == 5:
                hr = "5"
                am_pm = "AM"
        elif h == 0:
            hr = "12"
            am_pm = "AM"
        elif h == 1:
            hr = "1"
            am_pm = "AM"
        elif h == 2:
            hr = "2"
            am_pm = "AM"
            
            
        if m == 0:
            mn = "00"
        elif m == 10:
            mn = "10"
        elif m == 20:
            mn = "20"
        elif m == 30:
            mn = "30"
        elif m == 40:
            mn = "40"
        else:
            mn = "50"
            
        key = hr + ":" + mn + " " + am_pm
        
        if not key in hours:
            hours[key] = 0
            
        if h <= 23:
            if m == 50:
                m = 0
                h += 1
            else:
                m += 10
                
    return hours
            
            
def find_stats(hours):
    mean = 0.0
    median = 0
    std_dev = 0.0
        
    hours_values = sorted(list(hours.values()))
    count = len(hours_values)
    
    i = 0
    while i+1 < count:
        if hours_values[i] == 0:
            hours_values.pop(i)
            count -= 1
        else:
            break
    
    for n in hours_values:
        mean += n
    
    mean /= count
        
    midpoint = count / 2
    
    if not midpoint % 2 == 0:
        midpoint = midpoint - (midpoint % 2)
        mid_upper = (midpoint - 1)
        mid_lower = (midpoint + 1)
        
        median = (hours_values[int(mid_lower)-1] + hours_values[int(mid_upper)-1]) / 2
    else:
        median = hours_values[int(midpoint)]
        
    for n in hours_values:
        tmp = (n - mean)**2
        std_dev += tmp

    print(f"count: {count}")
    std_dev /= count
    std_dev = math.sqrt(std_dev)
        
    return mean, median, std_dev
            
def plot_graphs(benchmark, subfolder, option):
    count = len(values)
    
    for n in range(count):
        if benchmark >= values[n]:
            values[n] = 0
            
    fig = 0
    
    if option == 1:
        fig = plt.figure(figsize = (10, 5))
        plt.bar(times, values, color = 'red', width = 0.4)
    else:
        fig = plt.figure(figsize = (35, 10))        
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
        plt.bar(times, values, color = colors, width = 0.4)
        
    i = 0
    for key in hours:
        plt.text(i, hours[key], hours[key])
        i += 1
        
    plt.xlabel("Time of Day")
    plt.xticks(ticks=range(len(hours)), labels = times, rotation=90)
    plt.title("Harsh Braking Events (" + day + ")")
    
    if benchmark == 0 or benchmark == mean:
        plt.plot([0, count-1], [mean, mean], [0, count-1], [median, median], marker = 'o')
        plt.legend(['Mean Events', 'Median Events'], loc = 'upper left')
        
    if benchmark == mean + std_dev:
        plt.plot([0, count-1], [mean, mean], [0, count-1], [median, median], [0,count-1], [mean + std_dev, mean + std_dev], marker = 'o')
        plt.legend(['Mean Events', 'Median Events', '1 Standard Deviation Above'], loc = 'upper left')
        
    if benchmark == mean + std_dev * 2:
        plt.plot([0, count-1], [mean, mean], [0, count-1], [median, median], [0,count-1], [mean + std_dev*2, mean + std_dev*2], marker = 'o')
        plt.legend(['Mean Events', 'Median Events', '2 Standard Deviations Above'], loc = 'upper left')
        
        sig_path = os.path.join(path, 'significant')
        if not os.path.exists(sig_path):
            os.makedirs(sig_path)
        
        sig_path = os.path.join(sig_path, day)
        with open(sig_path + ".txt", 'w') as s_path:
            s_path.write('Significant Time Blocks:\n')
            for key in hours:
                if hours[key] > benchmark:
                    s_path.write(key + '\n')
            
    img_path = os.path.join(new_path, day)
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    img_path = os.path.join(img_path, subfolder + ".png")
    plt.savefig(img_path)
    plt.close(fig)

path = r"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\sorted_log\plot_data"

days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

new_path = os.path.join(path, "plots")

print("1. Plot by hour")
print("2. Plot by 10 min intervals")
try:
    option = int(input("Select option (1 or 2): "))
except ValueError:
    option = -1
    
try:
    option2 = int(input("Filter data under mean? (1 for yes, 0 for no): "))
except ValueError:
    option2 = 0


if option > 2 or option < 1:
    sys.exit("Invalid option, program terminated")
    
if not os.path.exists(new_path):
    os.makedirs(new_path)

if option == 1:
    new_path = os.path.join(new_path, "hourly")
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        
if option == 2:
    new_path = os.path.join(new_path, "granular")
    if not os.path.exists(new_path):
        os.makedirs(new_path)

count = 0
for day in days_of_week:
    dcount = 0
    file_path = os.path.join(path, day + ".txt")

    with open(file_path, 'r') as myfile:
        hours = {}
        mean = median = std_dev = 0

        for line in myfile:
            if re.search("Time start:", line):
                dcount += 1
                date = re.search("[0-9]+/[0-9]+/[0-9]{4}", line).group()
                
                time = re.split("\t", line)[0]
                time = time[11:]
                time = time[-11:]
                
                if option == 1:
                    hour = re.split(":", time)[0] + " " + re.search("AM|PM", time).group()
                else:
                    h = re.split(":", time)[0]
                    m = int(re.split(":", time)[1])
                    if m < 10:
                        m = "00"
                    elif m < 20:
                        m = "10"
                    elif m < 30:
                        m = "20"
                    elif m < 40:
                        m = "30"
                    elif m < 50:
                        m = "40"
                    else:
                        m = "50"
                    hour = h + ":" + m + " " + re.search("AM|PM", time).group()
                    hour = hour.strip()

                if not hour in hours:
                    hours[hour] = 1
                else:
                    hours[hour] += 1
        
        hours = sort_dict(hours, option)
        
        if option == 1:
            mean, median, std_dev = find_stats(hours)
            
        else:
            hours = add_zeroes(hours)
            
            hours = sort_dict(hours, option)
            
            mean, median, std_dev = find_stats(hours)
            
        times = list(hours.keys())
        values = list(hours.values())
            
        if option2 == 1:
            plot_graphs(0, 'all', option)
            plot_graphs(mean, 'mean', option)
            plot_graphs(mean + std_dev, 'stddev1', option)
            plot_graphs(mean + std_dev*2, 'stddev2', option)
        else:
            plot_graphs(0, 'all', option)
            
        print(str(dcount) + " events recorded for " + day)
    count += dcount

print(str(count) + " total events in logs")