using System.Runtime.InteropServices;
using Geotab.Checkmate;
using Geotab.Checkmate.ObjectModel;
using Geotab.Checkmate.ObjectModel.Exceptions;
using System.IO;
using Geotab.Checkmate.ObjectModel.Geographical;

// Create the API object and authenticate
API api = new API("bp6v@Virginia.edu", "UVADriver01", null, "uva", "my134.geotab.com");
await api.AuthenticateAsync();
//destination save file directory
string src_path = @"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\trips";

//create directory if it doesn't exist
if(!Directory.Exists(src_path)){
        Directory.CreateDirectory(src_path);
    }

var bottom = 90.0;
var top = -90.0;
var left = 180.0;
var right = -180.0;

var target_zone = await api.CallAsync<List<Zone>>("Get", typeof(Zone), new
{
    search = new ZoneSearch
    {
        Id = Id.Create("b5A8B7")
    }
});

foreach (var point in target_zone[0].Points)
{
    if (point.Y > top)
    {
        top = point.Y;
    }

    if (point.Y < bottom)
    {
        bottom = point.Y;
    }

    if (point.X > right)
    {
        right = point.X;
    }

    if (point.X < left)
    {
        left = point.X;
    }
}

BoundingBox target_region = new BoundingBox(left, bottom, right, top);

//Get all devices
var devices = await api.CallAsync<List<Device>>("Get", typeof(Device));
//Get total count of all devices
var total_devices = devices.Count;
//years we want to look through
string[] semesters = {"Spring", "Fall"};

foreach (string semester in semesters)
{
    var curr_device = 0;
    //iterate for each vehicle in list
    foreach (Device device in devices)
    {
        var distance = 0.0;
        curr_device++;
        var name = "";
        //Omit entries with '000-000-000'; no matching entry in Geotab database
        if (device.Name[0] != 'V' | device.Name != null)
        {
            name = device.Name;
        } else if (device.SerialNumber == "000-000-000")
        {
            continue;
        } else
        {
            name = device.SerialNumber;
        }
        //Time range for query filtering
        DateTime activeFrom = new DateTime(2023, 8, 1, 0, 0, 0);
        DateTime activeTo = new DateTime(2023, 12, 31, 11, 59, 59);
        if (semester == "Spring")
        {
            activeFrom = new DateTime(2023, 1, 1, 0, 0, 0);
            activeTo = new DateTime(2023, 5, 1, 11, 59, 59);
        }
        //Get all trips within time range for all vehicles
        var trips = await api.CallAsync<List<Trip>>("Get", typeof(Trip), new 
                    {
                        search = new TripSearch
                        {
                            DeviceSearch = new DeviceSearch
                            {
                                //For each iteration of the loop, only pull trips that match vehicle
                                Id = device.Id
                            },
                            FromDate = activeFrom,
                            ToDate = activeTo,
                            SearchArea = target_region,
                            IncludeOverlappedTrips = true
                        }
                    });
        //Get total count of trips
        var total_trips = trips.Count;
        var tCount = 0;
        //Only log data for vehicles with trips within time range
        if (total_trips >= 1)
        {
            //create save file directory for year
            string path = src_path + "\\" + semester + " 2023";
            if(!Directory.Exists(path)){
                Directory.CreateDirectory(path);
            }
            //generate filename and create file
            path = path + "\\" + name + ".txt";
            File.Create(path).Dispose();
            //store trips into newly created file
            using (StreamWriter outFile = File.AppendText(path))
            {
                foreach (Trip trip in trips)
                {
                    //Display progress to user
                    Console.Write("\r" + semester + " 2023" + "\tDevice: " + curr_device + " of " + total_devices + "\tTrip " + tCount + " of " + total_trips + " logged...");
                    //write to file
                    outFile.WriteLine("Trip: " + tCount);
                    outFile.WriteLine("Start: " + trip.Start + "\tEnd: " + trip.Stop + "\tDistance: " + trip.Distance);
                    outFile.WriteLine("-");
                    tCount++;
                    distance = distance +(double)trip.Distance;
                }
                outFile.WriteLine("Total Trips: " + tCount);
                outFile.WriteLine("Total Distance: " + distance);
            }
        }
    }
}