from __future__ import absolute_import
from core.timeLogger import TimeLogger
from inputs import get_key
from utils import config

def main():
    cfg = config.read_config()
    timeLogger = TimeLogger(cfg)
    listening = True
    while listening:
        kbEvents = get_key()
        if kbEvents:
            for kbEvent in kbEvents:
                if kbEvent.code == 'KEY_F6' and kbEvent.state == 0:
                    timeLogger.log_time()
                elif kbEvent.code == 'KEY_F7' and kbEvent.state == 0:
                    timeLogger.create_file()
                elif kbEvent.code == 'KEY_F8' and kbEvent.state == 0:
                    timeLogger.close_file()
                elif kbEvent.code == 'KEY_ESC' and kbEvent.state == 0:
                    listening = False


if __name__ == "__main__":
    main()
