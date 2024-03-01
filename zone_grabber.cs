using System.Runtime.InteropServices;
using Geotab.Checkmate;
using Geotab.Checkmate.ObjectModel;
using Geotab.Checkmate.ObjectModel.Exceptions;
using System.IO;
using System.Reflection.Metadata;

// Create the API object and authenticate
API api = new API("REDACTED", "REDACTED", null, "REDACTED", "REDACTED");
await api.AuthenticateAsync();
//destination save file directory
string src_path = @"C:\Users\VSU Computer Science\Documents\UVA\Geotab Data Puller\Geotab Data Puller\zone_coords";

//create directory if it doesn't exist
if(!Directory.Exists(src_path)){
        Directory.CreateDirectory(src_path);
    }

//Get all devices
var zones = await api.CallAsync<List<Zone>>("Get", typeof(Zone), new
{
    search = new ZoneSearch
    {
        Name = "CAPSTONE - VSU McCormick Rd ENTRY"
    }
});

foreach (Zone zone in zones)
{
    var path = src_path + "\\coords.txt";
    Console.WriteLine(zone.Name);
    File.Create(path).Dispose();
    using (StreamWriter outFile = File.AppendText(path))
    {
        foreach (Coordinate point in zone.Points)
        {
            outFile.WriteLine(point);
        }
    }
}
