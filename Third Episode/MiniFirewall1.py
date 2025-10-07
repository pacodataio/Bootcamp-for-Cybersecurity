import csv
import sys

#Function to read the inputs (packets) form a csv file
#in the file each line  shoul follow the  below format : SerialNo, Priority eaa
def read_inputs(filename):

 
    packets = []
    serials_seen = set()
    try:
       with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, skipinitialspace=True)
        lineNumber=1
        for line in reader:
            lineNumber += 1
            # Ignore empty lines
            if not line or all(v.strip() == "" for v in line.values()):
                    continue
            #Remove the spacing, in case the headres have space before, after o between
            line = {k.strip(): v.strip() for k,v in line.items()}
            try:
                serial = int(line.get("SerialNo", "").strip())
                priority = int(line.get("Priority", "").strip())
            except ValueError:
                    print(f"Line {lineNumber}: no numeric values, ignored")
                    continue
            if priority < 1 or priority > 10:
                print(f"Line {lineNumber}: priority out of range, ignored'")
                continue
            if serial in serials_seen:
                print(f"Line {lineNumber}: SerialNo {serial} duplicated")
            serials_seen.add(serial)
            packets.append({"SerialNo": serial, "Priority": priority})
            #print(f'packets: {packets}')
            
    except FileNotFoundError:
        print(f'File {filename} was not found')
        sys.exit(1)
    return packets

def sort_batch(inputs):
    #this funtion is to order inputs dictionary.  Applying Bubble sort.
    #ordered by highest priority and lowest serial number
    #Priority 1 is the highest, 10 is the lowest.
    n = len(inputs)
    for i in range(n):
        for j in range(0, n - i - 1):
            a = inputs[j]
            b = inputs[j + 1]
            # Pfirst is highest priority then serial number
            if (a["Priority"] > b["Priority"]) or (a["Priority"] == b["Priority"] and a["SerialNo"] > b["SerialNo"]):
                inputs[j], inputs[j + 1] = inputs[j + 1], inputs[j]
    return inputs


#function to process inputs in batches of 10
def process_packets(packets):
    for i in range(0, len(packets), 10):
        batch = packets[i:i+10]
        sorted_batch = sort_batch(batch)
        for element in sorted_batch:
            print(f"{element['SerialNo']},{element['Priority']}")

def main():
    # This program simulates a firewall to filter network packets
    #inputs: A file containing serial number and priority of packets
    #Output: Serial numbers ordered by highest priority and lowest serial number
    # In this implmenattion the file shpulb indicate by parameter:
    #python scriptName -f input.tx
    if len(sys.argv) < 3 or sys.argv[1] != "-f":
        print("Follow the format below:")
        print("  python MiniFirewall.py -f filename.txt")
        sys.exit(1)
    filename = sys.argv[2]
    inputs=read_inputs(filename)
    if not inputs:
        print("No inputs to process")
        return
    process_packets(inputs)
    
if __name__ == "__main__":
    main()