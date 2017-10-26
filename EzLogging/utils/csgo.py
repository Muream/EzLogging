from glob import glob
import os
import time

from EzLogging.core.config import config


def get_matching_demo(time_to_match, timeout=10, acceptable_margin=10):
    """Return the closest demo to the time_to_match within an acceptable_margin.
    """
    os.chdir(config.csgo_demos_path)
    latest_demo = None
    found = False
    startTime = time.time()
    time_is_out = False
    while not found and not time_is_out:
        try:
            latest_demo = max(
                glob('*.dem'.format(config.video_format)),
                key=os.path.getctime
            )
        except ValueError:
            print "no demos found."

        if latest_demo:
            latest_demo = os.path.join(config.csgo_demos_path, latest_demo)
            if time_to_match - acceptable_margin <= os.path.getctime(latest_demo) <= time_to_match + acceptable_margin :
                found = True

        currentTime = time.time()
        print currentTime, startTime + timeout
        if currentTime > startTime + timeout:
            time_is_out = True
            print 'time_is_out:', time_is_out
    return latest_demo
