# ÆON

<p align="center">
  <img src="preview/demo.gif" alt="demo" width="400"/>
</p>

Welcome to our repository! æon is a browser plugin that does the work of scouring through online videos for you. Simply visit a video page, activate the plugin, and see all of the video's highlights displayed visually for you, with nifty timestamps, the ability to easily jump to any of these key points in the video, and a (usually) precise estimate of where you'll find the original video thumbnail. Spend enough time on the video, and your viewing behaviour will update our servers with the intervals of video that you spent your time watching, helping others in the effort to sift through the online junk that just wastes everybody's time.

### Tech
We use the Microsoft Azure platform to run our virtual machine as well as integrate our API smoothly into a Mongo database, which holds all of the relevant info about individual videos in nicely defined documents. Backend code is written entirely in python, and our beautiful user-interface is done in Javascript ([highcharts.js](https://www.highcharts.com)) and makes use of a modified version of stock visualizations, which helps display viewing frequency.

Thumbnail analysis utilizes Computer Vision to compare the thumbnail image with frames in the video. It finds the most similar frame and indicates where the thumbnail is most likely to appear in the video. 


We hope that you check out our plugin, and that you enjoy saving time with it as much as we do! 🔵
