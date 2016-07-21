EzLogging
===

Installation
---
download and unzip this:
https://www.dropbox.com/s/9pftzlz1m9jtdov/EzLogging.zip?dl=0

**you need ffmpeg for Autolog to work: https://ffmpeg.org/download.html**


How to use
---

there are 2 .exe files included, EzLogging.exe and AutoLog.exe
start one of them to start the configuration and follow the instructions

* The start record hotkey should be the same as the one in your recording software
* The stop record hotkey should be the same as the one in your recording software
* The log time hotkey can be anything you want

**EzLogging**:

* press your start record hotkey when you want to start recording
* press your log time hotkey to log the time of the recording
note that if you press this hotkey two times in a short period of time  
**AutoLog** will be smart and will merge the clips into one longer clip  
(cf: **AutoLog** for more info)
* press your stop record hotkey when you want to stop recording

**AutoLog**:

* Use it when you want to cut out the clips you logged with **EzLogging**
* **AutoLog** will detect if there's some overlap in the clips.  
in the **Config**, you set two values telling **AutoLog** when to cut Before and After  
the timing logged with **EzLogging**.  
As an example let's say Before is set to 20 seconds and After is set to 10.  
your clips will last 30 seconds. If you press the log time two times in 30 seconds  
the clips will be merged together (you can repeat this as long as you want,  
allowing you to log longer clips than you would have otherwise)
