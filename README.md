# Chron-O-John's Twitch(streamlabs) DMX Alerts
## Description
This Programm enables you to trigger **DMX-Commands** when an event, like new follower or subscribition, happens in your livestream to an **RS485 Serial device**.
So for example you could trigger a light or fog machine when someone subscribes to your channel.
It's highly configurable using the Gui.
## Prerequisits
All you need is this program and a RS485 connection via Comport. 
I've used a no-name cable from Amazon like [this one](https://amzn.to/395AYax)(DE-Affiliate link -Amazon US [here](https://www.amazon.com/DMX-Interface-Computer-Controller-Converter/dp/B07W4G3T7W/ref=sr_1_8?keywords=rs485%20dmx&qid=1580841290&sr=8-8)) which works absolutely ok.
Alternatively you can DIY a DMX-Interface using any RS485 to USB adaptor.
## Screenshot
![screenshot-verion 0.1](https://raw.githubusercontent.com/Chron-O-John/twitch_DMX-Alerts_for_Streamlabs/master/ver0.1.png)
## Things to consider
The user-interface should be pretty self-explaining.
In order to listen for events you have to enter your *Socket API Token*.
Keep in mind that settings are **not saved automatically**!
Also *double, and triple check* if you have entered your token correctly as, right now, the application doesn't check if it is correct.
# Special Thanks
Special thanks go out to Krogman ([here on Twitch](https://www.twitch.tv/krogmann/)) who inspred and motivated me to even start programming this (which is my first coding-project after I finished school 13 years ago)

