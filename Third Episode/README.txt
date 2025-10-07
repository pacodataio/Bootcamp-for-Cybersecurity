FUNCTION main():
    The script  supports to print out just the serial numbers:, indicated by optional paramter --serial-only
    Verify  the  CLI interface with -f filename [--serial-only]-- and understandable usage messages.
    if --serial-only is indicated in the parameters
       the output should print only serialNo : serial_only=True
    else both serialNo and priority: serial_only=False
    read the file: read_file(filename, serial_only)

read_file(filename, seial_only):
    set packets as empty list 
    open the file with with error exception in cade the file not exists
    Read all the lines if not lines return message "empty file" and exit.
    check if the file has headers
    if header skip the first line
    for each line :
        Parse line:
             check possible delimiters  and remove spaces
                get  the values and  cast them to integers: serialNo and priority
                 If they are no numeric ignore them , return none
                 if priority out of range (priority < o0 or priority>10) ignore the line , return none
        If line is valid the add it to packets list
     
    process the packets list in batches of 10
        - order each batch   by priority ASC, then serial ASC
        if serial_only= Truee
            - print the batch (serial,priority)
        else
            - print just the serial
        -continue with the nest batch






CLI example: python MiniFirewall -f input.csv 
output:
3,1
10,1
2,3
4,3
1,5
9,5

CLI example: python MiniFirewall -f input.csv --serial-only
output:
3
10
2
4
1
