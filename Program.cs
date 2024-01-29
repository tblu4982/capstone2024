using System.Runtime.InteropServices;
using Geotab.Checkmate;
using Geotab.Checkmate.ObjectModel;
using Geotab.Checkmate.ObjectModel.Exceptions;
using System.IO;

// Create the API object and authenticate
API api = new API("bp6v@Virginia.edu", "UVADriver01", null, "uva", "my134.geotab.com");
await api.AuthenticateAsync();

//**NOTE: Check entity 'LogRecord' for log data on 'ExceptionEvent' records
/*string[] rules = {"RuleSeatbeltId", "RuleHarshCorneringId", "RulePostedSpeedingId",
    "RuleLightsLeftOnId", "RuleJackrabbitStartsId", "RuleAccidentId",
    "RuleIdlingId", "RuleEngineAbuseId", "RuleHarshBrakingId",
    "RuleEngineLightOnId", "RuleUnauthorizedDeviceRemovalId", "RuleApplicationExceptionId"};*/

string[] rules = {"RuleHarshCorneringId", "RuleAccidentId"};
foreach (string target_rule in rules){
    string src_path = @"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\";
    string target_path = src_path + "\\" + target_rule;
    string target_path2 = target_path + "\\" + "other";

    if(!Directory.Exists(target_path)){
        Directory.CreateDirectory(target_path);
        Directory.CreateDirectory(target_path2);
    }

    // Get all devices
    var devices = await api.CallAsync<List<Device>>("Get", typeof(Device));

    //get specific exception events
    var rule = Id.Create(target_rule);

    //track total harsh braking events
    var totalCount = 0;
    //for conversion from km to mph
    //const double km2mph = 0.6213711922;

    //Search for harsh braking events by car
    foreach (Device device in devices)
    {
        var name = "";
        //track number of harsh braking events per car
        var dCount = 1;
        //Omit entries with '000-000-000'; no matching entry in Geotab database GUI
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
        Console.WriteLine("Querying asset " + device.Name + "...");
        //Only pull exception events that match the current car in queue
        var exceptionEvents = await api.CallAsync<List<ExceptionEvent>>("Get", typeof(ExceptionEvent), new
        {
            search = new ExceptionEventSearch
            {
                DeviceSearch = new DeviceSearch
                {
                    Id = device.Id
                }
            }
        });
        var lockvar = true;
        //Filter out all non-harsh braking events
        foreach (ExceptionEvent exceptionEvent in exceptionEvents)
        {
            var curr_rule = exceptionEvent.Rule;
            //track count of all harsh braking events
            string path = target_path;
            if (name[0] != 'V')
            {
                path = target_path2;
            }
            //switch to creating a directory for vehicle
            //name of file = specific exception event
            //name of folder = vehicle id
            //check directory command: Directory.Exists([path])
            //make directory: DirectoryInfo [var] = Directory.CreateDirectory([path])
            string textfile = name + ".txt";
            if (curr_rule.Id == rule)
            {
                //create/overwrite text file for current asset
                if (lockvar == true)
                {
                    File.Create(Path.Combine(path, textfile)).Dispose();
                    lockvar = false;
                }
                var activeFrom = exceptionEvent.ActiveFrom;
                var activeTo = exceptionEvent.ActiveTo;

                //Console.WriteLine("Searching for brake records from " + activeFrom + " to " + activeTo + "...");
                //Console.WriteLine("Serial Number: " + device.SerialNumber);
                var logRecords = await api.CallAsync<List<LogRecord>>("Get", typeof(LogRecord), new 
                {
                    search = new LogRecordSearch
                    {
                        DeviceSearch = new DeviceSearch
                        {
                            Id = device.Id
                        },
                        FromDate = activeFrom,
                        ToDate = activeTo
                    }
                });
                var pos = 1;
                //write to text file for current asset
                using (StreamWriter outFile = File.AppendText(Path.Combine(path, textfile)))
                {
                    //Console.WriteLine("Event " + dCount);
                    outFile.WriteLine("Event " + dCount + ":");
                    foreach (LogRecord logRecord in logRecords)
                    {
                        //convert logged speed from km to mph
                        //var speed = logRecord.Speed * km2mph;
                        //speed = Math.Round(speed, 2);
                        var speed = logRecord.Speed;
                        string line = "";

                        if (logRecord == logRecords[0])
                        {
                            //Console.WriteLine("Time start: " + logRecord.DateTime + "\tLatitude: " + logRecord.Latitude + "\tLongitude: " + logRecord.Longitude);
                            line = "Time start: " + logRecord.DateTime + "\tLatitude: " + logRecord.Latitude + "\tLongitude: " + logRecord.Longitude;
                        }
                        else if (logRecord == logRecords[^1])
                        {
                            //Console.WriteLine("Time end: " + logRecord.DateTime + "\tLatitude: " + logRecord.Latitude + "\tLongitude: " + logRecord.Longitude);
                            line = "Time end: " + logRecord.DateTime + "\t\tLatitude: " + logRecord.Latitude + "\tLongitude: " + logRecord.Longitude;
                        } else
                        {
                            //Console.WriteLine("Time point " + pos + ": " + logRecord.DateTime + "\tLatitude: " + logRecord.Latitude + "\tLongitude: " + logRecord.Longitude);
                            line = "Time point " + pos + ": " + logRecord.DateTime + "\tLatitude: " + logRecord.Latitude + "\tLongitude: " + logRecord.Longitude;
                        }
                        //Console.WriteLine("Speed: " + speed + "\tDevice ID: " + logRecord.Device);
                        line += "\tSpeed: " + speed + "\tDevice ID: " + logRecord.Device;
                        outFile.WriteLine(line);
                        pos++;
                    }
                //Console.WriteLine("-");
                outFile.WriteLine("-");
                }
                dCount++;
                totalCount++;
            }
        }
    }
    Console.WriteLine("There are " + totalCount + " events recorded for " + target_rule + ".");
}