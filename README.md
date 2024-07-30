
# Data Collection with RTMaps (IMU+Biopac+Clicker+AV) DMS WIP
*History (Created): 2024-07-29 12:37*

## The RTMaps Diagram
![]([F:\Seeing Machines Test-track Development\4.Test track Diagrams\Seein Machine Test-track Study 1 Screenshot.png](https://github.com/yyt1208732230/SM2024_RTMaps_Datacollection/blob/main/4.Test%20track%20Diagrams/Seein%20Machine%20Test-track%20Study%201%20Screenshot.png))

This diagram includes data collection for a Bluetooth IMU, a Logitech presenter (left & right arrow listener), and an ECG/EDA Biopac physiological data collection system.

- **Sensors**: Physical devices required for the collection process (hardware + physical ports).
- **Servers**: Software servers required to run on the data collection computer for collecting/capturing signals from the DIY apparatus.
- **Receiver**: Data receiver components.
- **Decoders**: Data decoder components.
- **Monitors & Debuggers**: Development environment components for real-time visualization of monitoring data quality and their sample rates. Please disable these during the final data collection.
- **Recorders**: File recording for piloting studies and testing. Disable them and only record .rec files for final data collection.

## The Environment Set-up in the Automated Vehicle with RTMaps

### Main Components:
- Head movement IMU
- Biopac
- Clicker/Presenter
- Wizard of Oz Conversational Agent with Node.js (optional)

### Environment Requirements:
- Anaconda (recommended)
- Python 3
-  Mosquitto MQTT server
- Port listeners:
  - Bluetooth (head movement IMU)
  - 1 LAN port (Biopac)
  - Port 1883 (MQTT)
  - (WIP) Port 8080 (optional WoZ demo of Node.js environment, can be modified) -- *NOT IN THIS VERSION*
- (WIP) Node.js -- *NOT IN THIS VERSION*

## The Process of Setting Up in a New Computer/Existing Automated Vehicle Environment (for Windows)

### 1. RTMaps Configuration
1. Install RTMaps 4.9.0

   [Folder location: `External Disk:\Installation\`]

2. Copy the license files (.lic) to the RTMaps license folder (e.g., `C:\Program Files\Intempora\RTMaps 4\license`)

   [Folder location: Copy license files from `External Disk:\Seeing Machines Test-track Development\Program Files_Intempora_RTMaps\license\`]

### 2. Connect All the Sensors
- A Bluetooth dongle for WIT-IMU
- A Bluetooth dongle for Logitech Clicker
- The system of RTMaps MP150

### 3. Run the Required Servers
1. Ensure Anaconda/Miniconda is installed correctly.
2. Activate the Python environment `SM2024_Biopac_IMU_Clicker` with Anaconda/Miniconda:
   - **Navigate to the Directory**  
     Open the Conda terminal and navigate to the directory where the `./2.Anaconda Envs/SM2024_Biopac_IMU_Clicker.yaml` file is located.
   - **Create the Environment from the env.yaml File**
     ```sh
     conda env create -f SM2024_Biopac_IMU_Clicker.yaml
     ```
   - **Activate the Python Environment**
     ```sh
     conda activate SM2024_Biopac_IMU_Clicker
     ```
3. Turn on the data capturing server (MQTT):
   - Ensure the correct configuration of Mosquitto (see [here](https://github.com/yyt1208732230/Zoe_IMUs)).
   - Turn on WIT-IMU power, then run the Python script in the Conda terminal for the IMU:
     ```sh
     python ./Zoe_IMUs-main/WIT_BWT901CL/bt2mqtt_publisher_imu_WITt901cl.py
     ```
   - Check the clicker default control of the keyboard [here](https://www.keyboardtester.com/tester.html) (left&right arrow), then run the Python script in the Conda terminal for the clicker:
     ```sh
     python ./Zoe_IMUs-main/Clicker/mark_logger.py
     ```
    - Make sure scripts are running and signals are sending through MQTT protocal (recommand testing with MQTTbox).
		```
		IMU topic = "imu/wit/all"
		Clicker topic = "clicker/all"
		```
 4. Run the RTMaps diagram for data collection!
