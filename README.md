# Blynk Plugin for CraftBeerPi 3.0

This plugin is designed to integrate your CraftBeerPi controller with the Blynk service.  Blynk is a platform which allows data to be sent to and retrieved from an online service, and then utilizes mobile apps with drag-and-drop widgets to display the data and interact with the device in real-time.  It is fully customizable; you can pick as much or as little data as you wish to be displayed on the screen.  Because of the level of customization possible, this is truly a DIY app building process.  There is not a pre-designed interface for which you will start out with, but rather you will have to build your own, or scan a QR code from another user to clone their app. 

There are apps for iPhone/iPad and Android devices.  The apps are free, but Blynk does offer in-app purchases to add Energy to your account.  The more widgets you add to your app, the more Energy is required, however the starting amount with your free account is usually sufficient to add a handful of widgets before running into this limitation.

From the perspective of CraftBeerPi, you are able to display current temperatures and set points, device states (on or off), the current step in a brewing process, and graphs of any data (both real-time and historical).

This initial release of the plugin is read only.  It will allow viewing of all data mentioned above, but will not allow changes to settings or device states to be made.  Turning on pumps or other devices, changing set points, and receiving alerts or notifications is planned for later releases.

For more info, visit the following sites:
- Blynk website: [Blynk.cc](http://www.blynk.cc/)
- Blynk getting started guide: [Blynk.cc/#getting-started-getting-started-with-the-blynk-app](http://docs.blynk.cc/#getting-started-getting-started-with-the-blynk-app)
- CraftBeerPi website: [CraftBeerPi.com](http://web.craftbeerpi.com/)

## Screenshots

![blynkscreenshots](https://user-images.githubusercontent.com/29404417/27230256-a2387d40-527c-11e7-95a4-9312769ec988.png)

## Installation

To begin using this plugin, two steps are required.  First we will install the mobile app and create a project, then we will install the plugin into CraftBeerPi and configure it.

### Step 1: Mobile App

1. From the Google Play Store or the Apple App Store, download the Blynk app and launch it.
2. You will be required to create an account to use Blynk, but it is free.  Click the option to **Create New Project**, and you will be asked for the following information:
    - **Project Name:**  This can be anything, for example the name of your brewery.  It will show up at the top of your app
    - **Device:**  Pick one of the Raspberry Pi options that is the closest to the model you are using
    - **Connection Type:**  Choose how your Raspberry Pi is connected to the internet, most likely either WiFi or Ethernet
    - **Theme:**  Pick Dark or Light, whichever looks best to you
    - Click the **Create Project** button to finish
    - You should receive an email from Blynk with your Authentication Token. Keep this handy as we will need it later for use in CraftBeerPi
3. You will now be looking at a blank canvas.  This is where you will design your app.  Swipe from right-to-left and you will see the **Widget Box**, which is a list of all the display options you can pick from for your app.  When you click on one it will be added to your app, and the cost listed will come out of your energy meter.  You can return a widget if you decide you don't like it by dragging it up to the top of the screen until you see a recycle icon.
4. Place several widgets on the screen to represent the data you want to see from your brewing setup.  Here are some examples of widgets you can use for different data types in CraftBeerPi:
    - **Temperatures:**  Guage, Value Display, Labeled Value, Level, LCD, Graph, History Graph
    - **Set Points:**  Everything for temperatures, plus the Slider
    - **Actor States (Heating elements, pumps, agitators, etc):**  Button
    - **Actor Power:** LED, Level, Slider
    - **Current Step Display:**  Value Display, Labeled Value, LCD
    - **Last Updated Display:**  Value Display, Labeled Value, LCD
5. Once your widgets are placed, you must configure them so they know which data to link to on CraftBeerPi.  When you click on one you will see the settings for that widget.  The settings available will vary for each widget, but here are the most important ones:
    - **Text box (at top):**  This is the label that will appear above the widget to let you know what it's used for, so put in a descriptive name like "Boil Kettle" or "Pump".  The name doesn't have to match what the device is named in CraftBeerPi
    - **Color wheel:**  Choose a color to differentiate this widget or catagories of widgets from one another.
    - **Pin:**  This is how Blynk links this widget with data in CraftBeerPi.  See Pin Configuration section below for more info.
    - **Scale (two boxes that by default have a 0 and 1 in them):**  This will control how the data is scaled by the widget.  The first number should be the lowest you expect the data to go, and the second number should be the highest.  For example, a kettle temp guage could be scaled from 0 to 212 degrees, or 0 to 100 degrees, depending on whether you're using °F or °C.
    - **Refresh interval:**  It is best to set this to Push, because the Blynk plugin sends data to the Blynk cloud on its own set interval.
6. Once your widgets are configured, you can click the **Play** button in the upper-right corner.  This will start your app and allow it to start receiving data once we have finished configuration. To make modifications later, you will have to first click the **Stop** button.
7. Now that your app has been created, it is time to head over to CraftBeerPi to finish the install.

### Step 2: CraftBeerPi Configuration

1. First, make sure you are running the latest version of CraftBeerPi 3.0.  If not, or if you are not sure, you can perform the update by clicking on the **System** menu and then **System**.  Click the **Pull Update** button, and then **Confirm**.  Once you receive a notification that the update was successful, reboot the Raspberry Pi.
2. Install the Blynk plugin in CraftBeerPi by clicking on the **System** menu and then **Add-on**.  Find the Blynk plugin and click the **Download** button.  When the download is complete, you'll see a notification.  You must now reboot the Raspberry Pi so that the plugin will be loaded into the system.
3. After the reboot we will need to configure CraftBeerPi to login to your Blynk account.  Click the **System** menu and then **Parameter**.  Select the *blynk_authentication_token* option, and enter your token that you received in an email from Blynk.
4. Within sixty seconds the Blynk plugin will try to establish connection between CraftBeerPi and Blynk.  If it's successful, you will see the device status in the Blynk app change to Online. If not, see the Troubleshooting section at the bottom of this page.

## Pin Configuration

The term Pin is used in Blynk to indicate a physical or virtual pin on a hardware device, usually referred to as GPIO.  When a widget has been set to the same Pin that the hardware device is using, the widget will begin displaying the data being sent to Blynk from that device.  To figure out which Pins to use for which Sensors, Kettles, etc. in CraftBeerPi, look at the order in which they appear in the **Hardware** screen of CraftBeerPi, and then add that number to the Offset in the following table.

For example, Sensor #1 in CraftBeerPi will correspond with Pin V11 ( 10 + 1 ).  Kettle #3 Setpoint will correspond with Pin V33 ( 30 + 3 ).

***Note:*** If you set up your Blynk app first and then later delete devices in CraftBeerPi, the numbering will change and you will have to adjust the Pins in Blynk to once again correspond to the correct order of devices in CraftBeerPi.

| CraftBeerPi Name | Blynk Pin(s) | Offset | More Info |
| ---------------- | ------------ | ------ | --------- |
| Last Updated     | V0           | N/A    | Shows the last time CraftBeerPi sent data to Blynk |
| Current Step     | V1           | N/A    | Shows the current brewing step, with the timer value if present |
| Sensors          | V11 - V30    | 10     | Temperature sensor readings |
| Kettle Setpoints | V31 - V50    | 30     | Kettle temperature set points |
| Fermenter Setpoints | V51 - V70 | 50     | Fermenter temperature set points |
| Actor States     | V71 - V90    | 70     | The on/off state of actors. Value range: 0 - 1 |
| Actor Power      | V91 - V109   | 90     | The power level of actors. Value range: 0 - 100 |

## Troubleshooting

If the Blynk plugin encounters any problems while it's running, it will stop and then automatically restart itself in sixty seconds.  This is to try to allow for situations where your internet service may be experiencing issues, or go down completely, so that the Raspberry Pi does not need to be rebooted completely once your service is working again.  Also, after you have first entered your Blynk token, it will try to connect within sixty seconds without having to reboot.

If things are still not working, the first place to check is the log file.  From a terminal window or SSH, type `less ~/craftbeerpi3/logs/blynk.log` and press Enter.  Any connection problems, such as the authentication token being wrong, or the lack of connection with the Blynk Cloud service, should be listed near the bottom of the log.
