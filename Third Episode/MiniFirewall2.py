import csv
import sys

#Function to read the inputs (packets) form a csv file
#in the file each line  shoul follow the  below format : SerialNo, Priority eaa
def read_inputs(filename):
    packets = []
    serials_seen = set()
    try:
       with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        lineNumber=1
        for line in reader:
            try:
                lineNumber=lineNumber+1
                serial = int(line["SerialNo"])
                priority = int(line["Priority"])
                
            except KeyError as e:
                print(f'Error in column Name. {e}')
                sys.exit(1)
            except ValueError:
                    print(f"Line {lineNumber}: no numeric values, It's ignored")
                    continue
            if priority < 1 or priority > 10:
                print(f"Line {lineNumber}: priority out of range. It's ignored'")
                continue
            if serial in serials_seen:
                print(f"Line {lineNumber}: SerialNo {serial} duplicated")
            serials_seen.add(serial)
            #packets.append(line)
            packets.append({"SerialNo": serial, "Priority": priority})
            #print(f'packets: {packets}')
            
    except FileNotFoundError:
        print(f'File {filename} was not found')
        sys.exit(1)
    return packets

def sort_inputs(inputs):
    #this funtion is to order inputs dictionary.  Applying Bubble sort.
    #ordered by highest priority and lowest serial number
    #Priority 1 is the highest, 10 is the lowest.
    print(inputs) 
    n = len(inputs)
    for i in range(n):
        for j in range(0, n - i - 1):
            a = inputs[j]
            b = inputs[j + 1]
            # Pfirst is highest priority then serial number
            if (a["Priority"] > b["Priority"]) or (a["Priority"] == b["Priority"] and a["SerialNo"] > b["SerialNo"]):
                inputs[j], inputs[j + 1] = inputs[j + 1], inputs[j]
    return inputs


# Procesar y mostrar paquetes
def print_packets(sorted_packets):
    for element in sorted_packets:
        print(f"{element['SerialNo']},{element['Priority']}")   

def main():
    # This program simulates a firewall to filter network packets
    #inputs: A file containing serial number and priority of packets
    #Output: Serial numbers ordered by highest priority and lowest serial number
    # In this implmenattion the file shpulb indicate by parameter:
    #python scriptName -f input.tx
    if len(sys.argv) < 2:
        print("Follow the format below:")
        print("  python MiniFirewall.py -f filename.txt")
        #print(sys.argv)
        sys.exit(1)
    
    if sys.argv[1] == "-f":
        try:
            filename = sys.argv[2]
            #print (sys.argv)
            inputs=read_inputs(filename)
            #print(inputs)
            if not inputs:
                print("No inputs to process")
                return
            sorted_inputs = sort_inputs(inputs)
            print_packets(sorted_inputs)

        except IndexError as e:
            print(f'No file name was found. {e}')
            sys.exit(2)
            # with open(filename, "r", encoding="utf-8") as f:
            #    domains = [line.strip() for line in f if line.strip()]    
    else:
        print("Follow the format below:")
        print("  python MiniFirewall.py -f filename.txt")

if __name__ == "__main__":
    main()