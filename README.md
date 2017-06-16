# Blynk Plugin for CraftBeerPi 3.0

This plugin is designed to integrate your CraftBeerPi controller with the Blynk service.  Blynk is a platform which allows data to be sent to and retrieved from an online service, and then allows you to design mobile apps utilizing drag-and-drop widgets to display the data and interact with the device in real-time.  It is fully customizable, you can pick as much or as little data as you wish to be displayed on the screen.  There are apps for iPhone/iPad and Android devices.

From the perspective of CraftBeerPi, you are able to display current temperatures and set points, device states (on or off), the current step in a brewing process, and graphs of any data (both real-time and historical).

This initial release of the plugin is read only.  It will allow viewing of all of the data mentioned above, but will not allow changes to settings or device states to be made.  Turning on pumps or other devices, changing set points and more is planned for a later release.

For more about Blynk, visit their website at (Blink.cc)[http://www.blink.cc].

## Installation

To begin using this plugin, two steps are required.  Installing the mobile app and creating a project, and installing the plugin into CraftBeerPi and configuring it.

### Step 1: Mobile App

1. From the Google Play Store or the Apple App Store, download the free Blynk app and launch it.
2. You will be required to create an account to use Blynk, but it is free.  Click the option to Create New Project, and you will be asked for the following information:
    - Project Name:  This can be anything, for example the name of your brewery.  It will show up at the top of your app
    - Device:  Pick one of the Raspberry Pi options that is the closest to the model you are using
    - Connection Type:  Choose how your Raspberry Pi is connected to the internet, most likely either WiFi or Ethernet
    - Theme:  Pick Dark or Light, whichever looks best to you
    - Click the Create Project button to finish
3. You will now be looking at a blank canvas.  This is where you will design your app.  Swipe from right-to-left and you will see the Widget Box, which is a list of all the display options you can pick from for your app.  When you click on one it will be added to your app, and the cost listed will come out of your energy meter.  You can return a widget if you decide you don't like it by dragging it up to the top of the screen until you see a recycle icon.
4. Place several widgets on the screen to represent the data you want to see from your brewing setup.  Here are some examples of widgets you can use for different data types in CraftBeerPi:
    - Temperatures:  Guage, Value Display, Labeled Value, LCD, Graph, History Graph
    - Set Points:  Everything for temperatures, plus the Sliders
    - Actors (Heating elements, pumps, agitators, etc):  Button, LED
    - Current Step Display:  Value Display, Labeled Value, LCD
    - Last Updated Display:  Value Display, Labeled Value, LCD
5. Once your widgets are placed, you must configure them so they know which data to link to on CraftBeerPi.  When you click on one you will see the settings for that widget.  The settings available will vary for each widget, but here are the most important ones:
    - Text box at top:  This is the label that will appear above the widget to let you know what it's used for, so put in a descriptive name like "Boil Kettle" or "Pump".  The name doesn't have to match what the device is named in CraftBeerPi
    - Color wheel:  Choose a color to differentiate this widget or catagories of widgets from one another.
    - PIN:  This is how Blynk links this widget with data in CraftBeerPi.  Refer to the following table:
    - Scale (two boxes that by default have a 0 and 1 in them):  This will control how the data is scaled by the widget.  The first number should be the lowest you expect the data to go, and the second number should be the highest.  For example, a kettle temp guage could be scaled from 0 to 212 degrees F (or 0 to 100 degrees C). 
    - Refresh interval:  It is best to set this to Push, because the Blynk plugin sends data to the Blynk cloud on its own set interval.
6. Now that your app has been created, it is time to head over to CraftBeerPi to finish the install

### Step 2: CraftBeerPi configuration

1. Install the Blynk plugin in CraftBeerPi by clicking on the System menu and then Add-on.  Find the Blynk plugin and click the Download button.  When the download is complete, you'll see a notification.  You must now reboot the Raspberry Pi so that the plugin will be loaded into the system.
2. After the reboot we will need to configure CraftBeerPi to login to your Blynk account.  Click the System menu and then Parameter.  Select the blynk_authentication_token option, and enter your token that you received in an email from Blynk.
3. More to come
