import re
import sys

def parse_line(line):
    #This function arse a line into (serial, priority).
    #and also Supports comma, tab, or whitespace delimiters.
    
    # Split by comma OR whitespace
    parts = re.split(r"[\s,]+", line.strip())
    if not parts or len(parts) < 2:
        return None

    try:
        serial = int(parts[0])
        priority = int(parts[1])
    except ValueError:
        return None

    if not (1 <= priority <= 10):
        return None

    return (serial, priority)


def check_header(line):
    #Return True if line looks like a header 
    #Return False then first lne should be included
    # if it contains non-numeric tokens then header.
    tokens = re.split(r"[\s,]+", line.strip())
    return any(not tok.isdigit() for tok in tokens)


def read_file(filename, serial_only):
    packets = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
             lines = [l for l in f if l.strip()]
    except FileNotFoundError:
        print(f'File {filename} was not found')
        sys.exit(1)

    if not lines:
        print("No inputs to proces, file is empty")
        return
    #checking if the file has readers
    linenumber1 = lines[0]
    with_header = check_header(linenumber1)

    if with_header:
        lines = lines[1:]  # if header ignore first lin:  line[0}

    for line in lines:
        parsed = parse_line(line)
        if parsed:
            packets.append(parsed)

    # process in batches of 10
    for i in range(0, len(packets), 10):
        batch = packets[i:i+10]
        #order by highest priority and lowest serial number
        #Priority 1 is the highest, 10 is the lowest.
        # then Sort by priority ASC, then serial ASC
        batch.sort(key=lambda x: (x[1], x[0]))
        for serial, priority in batch:
            if serial_only:
                print(serial)
            else:
                print(f"{serial},{priority}")


if __name__ == "__main__":
# This program simulates a firewall to filter network packets
    #inputs: A file containing serial number and priority of packets
    #Output: Serial numbers ordered by highest priority and lowest serial number
    # In this implmenattion the file shpulb indicate by parameter:
    #python scriptName -f input.tx [--serialnumber] , where serial-only is optional
    if len(sys.argv) < 3 or sys.argv[1] != "-f":
        print("Follow the format below:")
        print("  python MiniFirewall.py -f filename.tx [--serial-only]")
        print ("--serial-only is optional")
        sys.exit(1)
    filename=sys.argv[2]
    # cerify is  --serial-only prameter is indicated
    if len(sys.argv) > 3 and sys.argv[3] == "--serial-only":
        serial_only = True #only print out  serial numbers
    else:
        serial_only = False #print both: serialNo and priority
    read_file(filename,serial_only)

