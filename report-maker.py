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

report += "ENHETER MED PROBLEM\n--------------------\n"

# loop for all the devices that we have to warn about
report += "\nStatus: WARNING\n\n"
for location in data["locations"]:
    for device in location["devices"]:
        if device["status"] == "warning":
            if device["uptime_days"] <= 5:
                report += device["hostname"] + "   "
                report += device["ip_address"] + "   "
                report += device["type"] + "   "
                report += location["site"] + "   "
                report += "(uptime: " + str(device["uptime_days"]) + "dagar)\n\n"
                if "connected_clients" in device:
                    print(device["connected_clients"])
                if "connected_clients" in device and device["connected_clients"] > 40:
                    print("connected_clients")

# loop for all the devices that came in offline
report += "\nStatus: OFFLINE\n\n"
for location in data["locations"]:
    for device in location["devices"]:
        if device["status"] == "offline":
            report += f"{device['hostname']:<16}{device['ip_address']:<16}{device['type']:<12}{location['site']:<12}\n\n"


# Counting all the units in the network
counts = {}  

for location in data["locations"]:
    for device in location["devices"]:
        t = device.get("type", "okänd")
        counts[t] = counts.get(t, 0) + 1

# Skriv en snygg sektion i rapporten
report += "STATISTIK PER ENHETSTYP\n-------------------------\n"
report += "Typ".ljust(18) + "Antal\n"
report += "-" * 26 + "\n"

# SOrted alphabetically
for t, n in sorted(counts.items()):
    
    nice = t.replace("_", " ").title()
    report += nice.ljust(18) + str(n) + "\n"

report += "\n"





               


report += "ENHETER MED LÅG UPTIME (<30 dagar)\n-----------------------------------\n\n"

# Accounting all units with less than a 30 days uptime

report += "Host".ljust(18) + "IP".ljust(16) + "Typ".ljust(12) + "Plats".ljust(16) + "Uptime\n"

found_low = False 
for location in data["locations"]:
    for device in location["devices"]:
        uptime = device.get("uptime_days", 0)  
        if uptime < 30:
            found_low = True
            report += device.get("hostname","?").ljust(18)
            report += device.get("ip_address","?").ljust(16)    # "?" is a fallback if key is missing
            report += device.get("type","?").ljust(12)
            report += location.get("site","?").ljust(14)
            report += f"{uptime} dagar\n"

if not found_low:
    report += "(Inga enheter under 30 dagar)\n"
report += "\n"

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
