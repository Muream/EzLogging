import subprocess

def game_detector():
    games = ['RocketLeague.exe', 'Overwatch.exe', 'csgo.exe']
    runningGames = []
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if any(game in line for game in games):
            runningGames.append(str(line).split('.')[0])

    if len(runningGames) == 0:
        return ['NoGame']
    else:
        return runningGames

game_detector()
