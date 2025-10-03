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


for location in data["locations"]:
    site = location.get("site", "?")
    
    # Counting how many objects we have in that list
    total = len(location.get("devices", []))
    online = sum(1 for d in location["devices"] if d.get("status") == "online")
    offline = sum(1 for d in location["devices"] if d.get("status") == "offline")

    report += f"{site}: {total} enheter ({online} online, {offline} offline)\n"

report += "\n"

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
        t = device.get("type")
        counts[t] = counts.get(t, 0) + 1

# Write a nice section for the report
report += "STATISTIK PER ENHETSTYP\n-------------------------\n"
report += "Typ".ljust(18) + "Antal\n"
report += "-" * 26 + "\n"              
# 26 is the column width

# Sorted alphabetically
for t, n in sorted(counts.items()):
    
    nice = t.replace("_", " ").title()
    report += nice.ljust(18) + str(n) + "\n"

report += "\n"





               


report += "ENHETER MED LÅG UPTIME (<30 dagar)\n-----------------------------------\n\n"

# Counting all units with less than a 30 days uptime

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

total_ports = 0
used_ports  = 0

for location in data["locations"]:
    for device in location["devices"]:
        if device.get("type") == "switch" and "ports" in device: 
            total_ports += int(device["ports"].get("total", 0))
            used_ports  += int(device["ports"].get("used", 0))

pct = (used_ports / total_ports * 100) if total_ports else 0.0
free_ports = total_ports - used_ports
report += f"Switch-portar totalt: {used_ports}/{total_ports} ({pct:.1f}%), ledigt: {free_ports}\n\n"





report += "SWITCHAR MED HÖG PORTANVÄNDNING (>80%)\n----------------------------------------\n\n"

 # Listing all VLANs
report += "VLAN-ÖVERSIKT\n-------------\n\n"

unik_vlans = set()

for location in data["locations"]:
    for device in location["devices"]:
        for v in device.get("vlans", []):   # If no vlans, empty list
            unik_vlans.add(v)

# Map puts together the number to strings, join puts them together nicely

vlans_lista = sorted(unik_vlans) 
report += ", ".join(map(str, vlans_lista)) + "\n\n"

vlans_lista = sorted(unik_vlans)

report += "STATISTIK PER SITE\n------------------\n\n"

report += "ACCESS POINTS - KLIENTÖVERSIKT\n-------------------------------\n\n"

report += "REKOMMENDATIONER\n----------------\n\n"



# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

# Write the title and date of the report
