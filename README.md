# Autofocus project

## Hardware

### Raspberry

- Model: Raspberry Pi 3 Model B+

- Memory: 1GB LPDDR2 SDRAM

- Processor: ARMv7 Processor rev 4 (v7l)

### ArduCam

- Resolution: 5MP

- Frame Rate: 30fps@1080px, 60fps@720px

- Picture: 2592x1944 Max

- Focus type: Motorized focus

#### Configuration

Enable the camera on the raspberry. Run a terminal type the next command:

    $sudo raspi-config

After that select enable camera.

#### Installation

Install python dependency libraries
    
    $ sudo apt-get install python-opencv

Enable the I2C0 port
    
    $ chmod +x enable_i2c_vc.sh
    
    $ ./enable_i2c_vc.sh

Reboot the raspberry after enabling the i2c port.