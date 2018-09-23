# EzLogging
EzLogging is meant to be a more flexible alternative to the replay buffer of OBS.  
You can save clips using a hotkey with control on the duration of the clips before AND after the time you hit the key.  
EzLogging also merges intelligently clips that overlap into one bigger clip.

# Installation
* You need Python 3 and Ffmpeg installed on your system.
* Clone or download the repo.
* Run `pip install -r requirements.txt` from the terminal in the root directory.
* Run `python main.py` to start EzLogging or double clic the file if you've set it to be executed with python by default.

# Setup
On the first launch, the settings window will open, if not, open it from File > Settings.  
You need to fill everything except the CS:GO stuff.  
ffmpeg **NEEDS** to be in your PATH.

## Brief explanation of the settings

* Recordings location: Where your recording software saves the videos.
* Recording Format: the format of your videos (defaults to mp4 but you can put in anything).
* Start/Stop Record: Hotkeys to start/stop the recording session. They **NEED** to be the same as your recording software. Not doing so will result in clips being extracted from the recording at the wrong timestamp.
* Log Time: Hotkey used to save the current timestamp. This is the equivalent of the hotkey you'd use for saving the replay buffer in your recording software.
* Time before/after timestamp (s): How much time clips should have before/after the timestamps

# How it works
Start EzLogging alongside your recording software.  
If you've setup your hotkeys properly, EzLogging should start counting how long it's been since you started recording.  
Hitting your `Log Time` hotkey will simply log the current timestamp in a `temp.txt` text file in your recordings folder.  
When you hit the `Stop Record` hotkey, the text file is renamed to match the last video in your recordings folder (which should be the video you just recorded).  
When you want to extract the clips from your recording, simply go to File > Log Clips.  
Based on your settings, the clips will have x seconds before and y seconds after each timestamps.  
If two clips overlap, EzLogging will extract one longer clip instead of exporting both.  
The clips extraction is both very fast and doesn't reduce the quality of your videos since nothing is encoded, just extracted.  
You'll likely realise that the clips don't start and end exactly where they should. This is because EzLogging extracts based on the Keyframes of your video. It finds the closest keyframe to the start and end **outside** of your clip's range, meaning your clips will always be a bit longer (*never shorter!*) than expected. Depending on your recording software settings, you might have up to 10-20s more in your clips. This was never a problem for me.  
The clips are saved in a `Clips` folder in your recordings directory.  
When EzLogging is done with a recording, it moves it in a `Processed` folder.  
Recordings with no associated text files are moved in a `NoTextFile` folder.


# Todo:
* [ ] Sort clips based on the game being currently played
* [ ] Save csgo demos along the clips
* [ ] Make an OBS extension (this would avoid having to start two applications everytime you record)

# Disclaimer
Please note that I wrote this tool for my own personal needs and it might not be suited for you. I'm always opened to feedback and will gladly fix/implement stuff if I find the time.  
Pull requests are very welcomed!