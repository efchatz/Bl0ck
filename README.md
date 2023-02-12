[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/efchatz/Bl0ck">
    <img src="images/bl0ck-logo.png" alt="Logo" width="400" height="400">
  </a>

  <h3 align="center">Bl0ck attack tool</h3>

  <p align="center">
    An attack tool to utilize Bl0ck attacks
    <br />
    <br />
    <a href="https://github.com/efchatz/Bl0ck/issues">Report Bug</a>
    ·
    <a href="https://github.com/efchatz/Bl0ck/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The Bl0ck attack tool was created based on the publication titled ["Bl0ck: Paralyzing 802.11 connections through Block Ack frames"](#). The following text mentions a summary of these attacks and how they can be used with the Bl0ck tool. A more detailed analysis is mentioned in the relevant publication.

The Bl0ck attack tool serves the purpose of having an easy and with a terminal argument access to three different attacks we managed to identify, regarding Wi-Fi 5 (802.11ac) and Wi-Fi 6 (802.11ax) networks. These attacks are separated into three cases:
* Block-Ack Requests (BAR): An attacker sends BAR frames to the AP, spoofing the MAC address of an already connected STA and requesting a Starting Sequence Number (SSN) that is invalid. The behaviour of the AP was to stop responding with QoS Data frames to the source MAC address of these frames, but without disconnecting it. Even after this attack stopped, the legitimate STA while remain connected to that AP, was unable to retrieve QoS Data frames. As a result, the legitimate STA, to have access to QoS Data frames, needed to reconnect to that AP manually. Practically, this means that this STA was unable to retrieve any relevant Data frame, while it remain connected to this AP. As a result, an attacker could exploit further this issue, by executing a Deauthentication/Disassociation or an Evil Twin assault, to trick the targeted STA into changing the wireless network. Some APs behave the same way when they were targeted with BA frames.
* Block-Ack (BA): An attacker sends BA frames to the AP, spoofing the MAC address of an already connected STA and requesting a Starting Sequence Number (SSN) that is invalid. The behaviour of the AP was to stop responding with QoS Data frames to all connected STAs. This means that regardless of the targeted STA or the source MAC address (yes, we can use a completely random one), the AP will not respond to any STA with any QoS Data frame. At least, for as long as the attack remains active. After that, in most cases, the AP started again to respond with QoS Data frames. This attack is quite handed, as it can tear down whole networks, without any special equipment. For instance, an attacker in a public Wi-Fi AP, could escalate this attack to refuse to all STAs the Internet access. Most users will probably stop using this Wi-Fi service, since they could not have any Internet access. As a result, an attacker can use the whole bandwidth for their purposes.
* Block-Ack Requests special case (BARS): This is a special case of the BAR attack. The only difference with this attack is that the SSN is valid. Again, the behaviour is the same as with the BAR attack.

The following table demonstrates each issue we observed for each AP we managed to test. The * depict APs that can be affected by the BA frames too, while being vulnerable to the attack I. Hostapd behaviour depends on the particular WNIC, in our case Intel AX200. Zyxel AP was vulnerable only to the BARS attack.
|  AP | Attack I (BAR)| Attack II (BA)| CVE ID |
|---|---|---|---|
|Asus RT88AXU|✗| ✓  | –  |
|Vendor |  ✓* | ✗  |  – |
|  TP-Link AX10v1|  ✗ | ✓  |  – |
|  D-Link DIR X-1560 |  ✓* | ✗  | [CVE-2022-32666](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2022-32666)  |
|  Zyxel NWA50AX | ✓  | ✗  |  [CVE-2022-32666](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2022-32666) |
|  Huawei AX3 |  ✓ | ✗  | –  |
|  Linksys MR7350 |  ✓ | ✗  | – |
| Hostapd |  ✓ | ✓  | – |

From our evaluation, attack I (BAR) and BARS is based on the IEEE 802.11 standard. This means that most APs will be vulnerable when operate on Wi-Fi 5 or 6. This happens because there is no such protection in the relevant standard, to handle spoofed BAR frames with invalid SSN. On the other hand, attack II (BA) is basically based on vendor's specific misconfiguration, which accepts unsolicited BA frames. Note that is attack affects both WPA2 and WPA3, since they both operate on WiFi 5 and 6. As a result, this attack does not work against Wi-Fi 4 (802.11n) networks, regardless of the authentication method they use. 

### Built With

This section lists all major frameworks/libraries used to create this project. Tested with Python 3.7 and Scapy 2.4.3. Probably other versions of Scapy and Python will be applicable too.

[![Python][Python.py]][Python-url] <br />
[![Scapy][Scapy]][Scapy-url]



<!-- GETTING STARTED -->
## Getting Started

To start this tool, first make sure you have installed a Python 3 version and the WNIC you possess has monitoring capabilities.


### Installation

```
1. sudo pip3 install -r requirements.txt
```
2. Put WNIC into monitoring mode
3. sudo python3 Bl0ck.py -h


<!-- USAGE EXAMPLES -->
## Usage

This section is dedicated to the usage of the tool. After installation, a user will have to put their WNIC into monitoring mode. Then, they can execute in the terminal the following command as an example, first changing any relevant values: sudo python3 Bl0ck.py --sta MAC --ap MAC --wnic wlan0 --attack BA --num 100 --random 0

Details about each parameter are mentioned in the following help me output of the tool.

```
  ____  _  ___       _    
 | __ )| |/ _ \  ___| | __                    __
 |  _ \| | | | |/ __| |/ /                  .'  '.
 | |_) | | |_| | (__|   <                  | STOP |
 |____/|_|\___/ \___|_|\_\                  '.__.'
                                              ||
                                              ||
                                              ||
                                            \||///
                                         ^^^^^^^^^^^^^

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
usage: Bl0ck.py [-h] [--sta STA] [--ap AP] [--wnic WNIC] [--attack ATTACK]
                [--num NUM] [--rand RAND] [--frames FRAMES]
                [--verbose VERBOSE]

optional arguments:
  -h, --help            show this help message and exit
  --sta STA, -c STA     Target STA MAC address: AA:BB:CC:DD:EE:FF
  --ap AP, -b AP        Target AP MAC address: AA:BB:CC:DD:EE:FF
  --wnic WNIC, -i WNIC  Wireless interface: wlan0
  --attack ATTACK, -a ATTACK
                        Attack choice: BAR (Block-Ack Request), BA (Block-Ack)
                        or BARS (Block-Ack Request special case)
  --num NUM, -n NUM     Number of concurrent frames to send: between 1 to 3000
  --rand RAND, -r RAND  Enable/Disable the usage of random source MAC address,
                        overwrites the --sta/-c argument: 0 (disable) or 1
                        (enable)
  --frames FRAMES, -f FRAMES
                        Number of frames to send to the targeted AP: e.g.,
                        100. If 0 was given, the attack with continue
                        indefinitely.
  --verbose VERBOSE, -v VERBOSE
                        Enable/Disable verbose messages of Scapy: 0 (disable)
                        and 1 (enable)

```

Regarding the concurrent frames (--num flag) a WNIC needs to exploit an AP, this differs for each AP. Generally, 10 to 100 frames are enought to achieve this result. It is suggested to start with a low value, like 10 and increase it every time by 10-20, till observing the QoS Data interruption. For the --rand parameter, the BA attack is the most suitable one to be used with. The BAR and BARS ones will rarely have a positive impact against APs. However, if BA attack works and the opposite AP operates with a Wireless IDS, enabling this flag with probably bypass this protection.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information. The attack tool is provided only for educational purposes and authorized audits. Use it at your own risk.



<!-- CONTACT -->
## Contact

[![LinkedIn][linkedin-shield]][linkedin-url] - Efstratios Chatzoglou -  efchatzoglou@gmail.com  <br />
[![LinkedIn][linkedin-shield]][linkedin-url2] - Vyron Kampourakis -  brykam@gmail.com  


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

We would like to thank all the vendors we contacted and reported these attacks, along with the retrieved bug bounties we received. Especially, MediaTek, which reserved [CVE-2022-32666](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2022-32666) for its products. Also, we would like to give some acknowledgement to our Wi-Fi fuzzer named [WPAxFuzz](https://github.com/efchatz/WPAxFuzz), which helps us at the early stages of this study, [the README template repo](https://github.com/othneildrew/Best-README-Template), which helped us to create this README file and [logo.com](https://logo.com/), which allowed us to create the Bl0ck attack tool logo.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/Contributors-2-brightgreen?style=for-the-badge
[contributors-url]: https://github.com/efchatz/Bl0ck/contributors
[stars-shield]: https://img.shields.io/badge/Stars-2-blue?style=for-the-badge
[stars-url]: https://github.com/efchatz/Bl0ck/stargazers
[forks-shield]: https://img.shields.io/badge/Forks-0-blue?style=for-the-badge
[forks-url]: https://github.com/efchatz/Bl0ck/network/members
[issues-shield]: https://img.shields.io/badge/Issues-0-lightgrey?style=for-the-badge
[issues-url]: https://github.com/efchatz/Bl0ck/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/efchatz/Bl0ck/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/efstratios-chatzoglou-b2b09616b
[linkedin-url2]: https://gr.linkedin.com/in/vyron-kampourakis
[product-screenshot]: images/screenshot.png
[Python.py]: https://img.shields.io/badge/Python-3.7-blue
[Python-url]: https://www.python.org/
[Scapy]: https://img.shields.io/badge/scapy-2.4.3-blue
[Scapy-url]: https://github.com/secdev/scapy
