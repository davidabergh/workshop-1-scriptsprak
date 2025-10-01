# Import the json library so that we can handle json
import json

# Read json from products.json to the variable products
# open(filePath, "r" for read, encoding = character encoding)
data = json.load(open("network_devices.json","r",encoding = "utf-8"))

# Create a variable that holds our whole text report
report = "Nätverksrapport - Techcorp AB\n\n"

# Added dates for the daily updated report 

last_updated_str = data["last_updated"]
report += f"Senast uppdaterad: {last_updated_str}\n\n"

report += "Executive Summary\n------------------\n\n"

report += "ENHETER MED PROBLEM\n--------------------\n\n"

report += "ENHETER MED LÅG UPTIME (<30 dagar)\n-----------------------------------\n\n"

report += "STATISTIK PER ENHETSTYP\n------------------------\n\n"

report += "PORTANVÄNDNING SWITCHAR\n------------------------\n\n"

report += "SWITCHAR MED HÖG PORTANVÄNDNING (>80%)\n----------------------------------------\n\n"

report += "VLAN-ÖVERSIKT\n-------------\n\n"

report += "STATISTIK PER SITE\n------------------\n\n"

report += "ACCESS POINTS - KLIENTÖVERSIKT\n-------------------------------\n\n"

report += "REKOMMENDATIONER\n----------------\n\n"

# loop through the location list
for location in data["locations"]:
    # add the site/'name' of the report
    
    report+= "\n" + location["site"] + "\n" + "\n"
    
    # add a list of the host names of the devices on the report
    # on the location to the report
    for device in location["devices"]:
        report += "  " + device["hostname"] + "\n"

# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

# Write the title and date of the report
