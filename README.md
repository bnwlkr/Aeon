# ÆON

Welcome to our repository! æon is a browser plugin that does the work of scouring through online videos for you. Simpy visit a video page, activate the plugin, and see all of the video's highlights displayed visually for you, with nifty timestamps and the ability to easily jump to any of these key points in the video. Spend enough time on the video, and your viewing behaviour will update our servers with the intervals of video that you spent your time watching, helping others in the effort to sift through the online junk that just wastes everybody's time.

### Tech
We use the Microsoft Azure platofrm to run our virtual machine as well as integrate our API smoothly into a Mongo database, which holds all of the relevant info about individual videos in nicely defined documents. Backend code is written entirely in python, and our beautiful user-interface is done in Javascript and makes use of a modified version of stock visualizations, which help display viewing frequency.

Thumbnail analysis is a bit of a work in progress, but currently uses Python image processing libraries to compute similarities to frames within the video itself.


We hope that you check out our plugin, and that you enjoy saving time with it as much as we do! 🔵
