# 🕹 RetroPico (v1.x)

**retroPico** is a complete open-source hardware platform powered by the **Raspberry Pi RP2040** microcontroller. Designed for retro emulation, vintage video/audio projects, and hardware experimentation, it features a modular ecosystem including a motherboard, an I2C Input/Output (IO) extension board, and a dedicated micro-operating system.

> [!NOTE]
> *Please don't be too critical of my design choices and schematics—this is a hobbyist project. My electronics studies date back over 40 years, and I have never worked professionally in hardware design. This project is a personal challenge to prove to myself that I still retain enough knowledge to tinker with modern electronic components. The days of building a Z80 on a breadboard with a 7-segment display, a 2716 EPROM, 2KB of SRAM, and coding it entirely in assembly language feel like they belong to the Paleolithic era!*

⚠️ Please note that this PCB is designed by a hobbyist and is not intended for commercial use.

---

_⚠️ **Important:** I am providing the Gerber files for the PCB so you can assemble your own **retroPico**, which requires a certain level of soldering experience and dexterity. However, you can achieve a functionally equivalent setup using a vanilla Raspberry Pi Pico and a prototyping breadboard.*_

## 🤖 AI Coding Assistant

If you are using an AI agent (such as ChatGPT, Claude, or GitHub Copilot) to help you develop scripts for the retroPico, simply copy and paste the contents of our **RetroPico Mentor Prompt** (`RETROPICO_MENTOR_PROMPT.md`). It will configure the AI with all the exact pinouts and board addresses, guiding you step-by-step without hardware errors!

---

## 📌 Motherboard Specifications (v1.4)

Several revisions were created during development. The most polished and finalized version is **v1.4**. Earlier versions exist in very limited numbers, which is why I keep the development history here.

[image]

The **v1.4 (Stable)** motherboard revision integrates the following features:

<img width="435" height="410" alt="image" src="https://github.com/user-attachments/assets/28c7ffd2-e0df-4d74-8cfb-f1193450a8a2" />

- **Computing Core**: **RP2040** microcontroller backed by **2-16 MB of Flash memory (W25QxxFVSG)**.
- **Video Output**: **VGA port** (DB15 connector). Quick display configuration via three solder jumpers (**SJ1, SJ2, SJ3**) to easily switch between **Monochrome** and **Basic 3-bit RGB** rendering.
- **Storage**: **MicroSD card slot (TF Card)** with an automatic *Card Detect* pin routed to `GP11`.
- **Wireless Connectivity**: Socket for an **ESP-01S (Wi-Fi) module** utilizing pins `GP9` and `GP10`.
- **Audio & Effects**: Integrated **magnetic buzzer (4000Hz)** and a **WS2812B (NeoPixel) addressable RGB LED** managed on `GP23`.
- **Extensions**: External NeoPixel connector (configured on `GP24`) and an I2C extension header.
- **Power & Connectivity**: **USB Type-C** connector (6 pins) equipped with a 500 mA protection fuse and an **AP2114H-3.3** voltage regulator. This female USB port supports **USB Host mode**, allowing you to directly connect a **standard keyboard** or a **Gamepad** to interact with your programs and emulators.

**A lot of features packed into a tiny PCB (60mm x 45mm).**

## 🛠️ Hardware Troubleshooting Guide

Assembling the **retroPico** is a challenge in itself, and booting a PCB for the first time is the ultimate test. Whether you are an experienced builder or taking your first steps with the **RP2040**, soldering mistakes or temperamental components are all part of the process.

To guide you through, the repository includes a comprehensive flowchart based on real debugging sessions:

👉 **[Check out the RetroPico RP2040 PCB Debug Flow](./hardware/RetroPico_DebugPCB.pdf)** **

## VGA Port Specifics

The RetroPico can be configured for either monochrome or 3-bit mode allowing the display of 8 colors. **3-bit Color or Mono Configuration**: Switching between mono and color modes is done by bridging the solder jumpers **SJ1, SJ2, and SJ3**.

The RetroPico VGA port implements the hardware technique from the PICO-VGA-Micropython project by HughMaingauche, [PICO-VGA-Micropython par HughMaingauche](https://github.com/HughMaingauche/PICO-VGA-Micropython/blob/main/VGA.py)  adding a monochrome mode option to free up even more RAM for your projects.

In color mode, the video buffer requires about 120KB of RAM, leaving around 50KB for your program. In monochrome mode, the buffer size drops to about 40KB, giving you significantly more headroom.

It is possible to drive the VGA port using **MicroPython**. While this solution is not fully optimal, I will add MicroPython examples to the `testcode/` directory once my testing is completed.

---

## 📌 GPIO Pinout Table

This table summarizes the RP2040 pin assignments across hardware revisions. Grayed-out areas indicate that the option was not available on that specific version.

<img width="730" height="568" alt="image" src="https://github.com/user-attachments/assets/1c53badb-5805-4934-ac96-cc5509bbca45" />

---

## 🔌 Extension Module: RetroPico I2C Addon (v1.1)

To enrich the user interface, the project includes an optional second PCB that plugs directly into the main I2C port: the **RetroPico I2C Addon**.

* **Visual Interface**: Support for an I2C-connected **SSD1306 OLED screen**.
* **User Inputs**: **3 push-buttons** (`BTN1`, `BTN2`, `BTN3`) managed via a **PCF8574AT** pin expander (saving valuable pins on the RP2040).
* **Environmental Sensors**: Slot for an **AHT20 + BMP280** combined temperature/humidity/pressure sensor.
* **Onboard Storage**: A dedicated **CAT24Cxxx** EEPROM memory chip for the module.
* **WRITE Jumper**: Connects the WP (Write Protect) pin to ground (GND) to **enable writing** to the EEPROM. Left un-bridged, the EEPROM remains locked in read-only mode.
* **Daisy-Chaining**: Features a fused I2C-INPUT port and **two output ports** (`I2C-OUT1`, `I2C-OUT2`) to easily chain additional modules.

<img width="510" height="335" alt="image" src="https://github.com/user-attachments/assets/47bdc560-c56a-44de-9372-f5a676f50c30" />

### Module I2C Address Table

<img width="256" height="154" alt="image" src="https://github.com/user-attachments/assets/037f8af3-744b-4097-852c-e45279ffd713" />

---

## 💻 Software Ecosystem (Supported Firmwares)

### 1. RetroPicoOS (MicroPython)

A custom-built micro-operating system and file manager written in **MicroPython** specifically designed for the *Motherboard + I2C Addon* combo.

- **File Manager**: Lists and sorts `.py` scripts directly on the OLED screen.
- **Dynamic Execution**: Navigate using the physical buttons and execute any script directly into memory using `exec()`.
- **Cross-Storage Copying**: Duplicate files on the fly from internal Flash memory to the MicroSD card (and vice versa).
- **Diagnostics**: Calculates and displays total and available Flash storage at startup.

### 2. Porting & Emulation (C/C++)

The retroPico is a highly versatile development platform. Thanks to its integrated VGA port supporting monochrome or 8-color (basic RGB) output, it acts as an ideal hardware base for porting existing emulators designed for the Raspberry Pi Pico (8/16-bit consoles, vintage computers, etc.).

For instance, its architecture natively supports Matt Evans' project, which runs a Macintosh 128K/Plus emulator on the RP2040:

- **Original Project Link**: [pico-mac (pico-umac) by evansm7](https://github.com)
- **Video Demonstration**: You can watch Jeff Geerling's full video detailing the installation and performance of this emulator on the RP2040: [Macintosh on a microcontroller (YouTube)]([https://youtube.com](https://www.youtube.com/watch?v=-gOS22wEpmU)).
- **Mono Mode Configuration**: Switch to mono mode by changing the solder spots on **SJ1, SJ2, and SJ3**.

### 3. Retro Gaming Platform

The core philosophy behind this project was to create a flexible learning environment and a solid foundation for retro emulation. A quick web search for "**rp2040 retro emulator**" will yield a multitude of incredible community projects that would be too long to list here.

---

## 📂 Repository Structure

```text
├── hardware/
│   ├── main-board-retroPico/  # Schematics and Gerbers for the RP2040 motherboard (v1.4)
│   └── addon-i2c/             # Schematics and Gerbers for the IO extension module (v1.1)
├── firmware/                  # Custom-compiled Micropython version supporting larger Qflash sizes
├── testcode/                  # MicroPython scripts to validate individual hardware components
└── games/                     # MicroPython games designed to run on the I2C Addon board
```

---

## 🎓 Accessibility & Raspberry Pi Pico Compatibility

If you are new to programming or electronics, don't be intimidated! Even though the **RetroPico** integrates multiple components onto a single circuit board (VGA, Wi-Fi, MicroSD, etc.), **its core is a standard Raspberry Pi Pico**.

There is actually **very little difference** between this board and a standard Pi Pico:
- **Same Chip:** The main microcontroller is the RP2040. Any code written for a standard Pico will run here.
- **Same Foundations:** The programming logic, pin (GPIO) usage, and environment remain identical.

### 📚 Resources for Beginners

Since the architecture is identical, you can fully rely on the official Raspberry Pi Foundation guides and tutorials to learn how to program your RetroPico.

To take your first steps, we highly recommend the official guide:  
👉 **[Getting started with the Raspberry Pi Pico (Raspberry Pi Projects)](https://raspberrypi.org)**

This guide will teach you step-by-step how to:
1. Install and configure the **Thonny** IDE.
2. Connect your board to your computer and flash the **MicroPython** firmware.
3. Write your first scripts to control inputs and outputs.

Once you understand the basics of blinking an LED or reading a button using that guide, the **RetroPico** ecosystem and its diagnostic tools (`testcode/`) will allow you to go much further (graphics, sound, games, and networking) without changing your workflow!

---

## 🚀 Quick Start with RetroPicoOS (GUI Interface)

The **RetroPicoOS** application allows you to browse the file system of either the onboard Flash or the SD card (if inserted). It enables file transfers between Flash and SD card storage, and can launch applications from either source. If you save the program as `main.py` in the root Flash directory, it will execute automatically whenever the RetroPico boots up. 

*Important Note: You will need the I2C Extension Addon, as the OS requires the OLED screen and the 3 tactile buttons for menu navigation.*

1. Flash the official MicroPython firmware (Raspberry Pi Pico / RP2040 version) onto your retroPico.
2. Copy the required libraries (ssd1306.py, pcf8574.py, and sdcard.py) into the /lib folder of your board.
3. Upload the RetroPicoOS script named as main.py to the root of the Flash storage.
4. Plug in the RetroPico I2C Addon module, insert a FAT32-formatted MicroSD card, and power it up!

---

## 🎮 Game Library: RetroPicoOS Games

To immediately test the hardware capabilities of the RetroPico v1.4 + I2C Addon combo, the repository includes a suite of retro games written in MicroPython. They utilize the OLED screen for graphics and the PCF8574 expander to read button inputs.
* 🚀 RetroPico_SpaceInvader.py: The all-time arcade classic. Survive waves of alien invaders!
* 🛡 RetroPico_SpaceCombat.py: A space combat game focused on maneuvering and dodging enemy fire.
* 🌕 RetroPico_MoonLander_V2.py: Perfectly balanced physics. Control your thrusters to land your module safely.
* 🧱 RetroPico_Breakout.py: A dynamic brick-breaking game using the physical buttons to move the paddle.
* 🏓 RetroPico_PongGame.py: The timeless virtual tennis match.
* 💥 RetroPico_Artillery.py: Calculate your firing angle and power to obliterate the enemy target.
* 🌀 RetroPico_GameofLife.py: A smooth graphical simulation of Conway's famous Game of Life.
* 🕹 RetroPico_Pinball.py: A compact pinball adaptation tailored for the OLED screen.

### 🕹️ How to Play?
1. Copy the game .py files of your choice onto a **MicroSD card (formatted in FAT32)** or directly into the internal Flash memory of the RP2040.
2. Turn on the console and select your active storage device (FLASH or SD).
3. Scroll through the list using the **Up (P4)** and **Down (P6)** buttons.
4. Press **Select (P5)** on your chosen game: RetroPicoOS will dynamically load the code and launch the session!

---

## 📜 License
The hardware design files (schematics, layouts, Gerbers) and software in this project are licensed under **the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0).**
❌ **Commercial use of this project (including reselling bare PCBs, component kits, or pre-assembled retroPico boards) is strictly prohibited without prior written permission from the author.**
Please review the full [LICENSE](LICENSE) file for more details.
