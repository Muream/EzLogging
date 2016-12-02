import subprocess
import json
import collections
import os


def get_processes():
    """List all the running processes."""
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    processes = []

    for line in proc.stdout:
        process = line.split(' ')[0]
        processes.append(process)
    return processes


def running_games():
    """
    Compares the currently running processes to the list of known games.
    Returns a list with the names of the running games
    """
    games = get_games()
    runningGames = []
    processes = get_processes()
    for process in processes:
        for game, name in games.iteritems():
            if process == game:
                runningGames.append(name)
    if len(runningGames) == 0:
        return ['No Game Running']
    else:
        return runningGames


def add_game(process, game):
    """Add a game to the list of known games."""
    games = get_games()
    if process not in games:
        games[process] = game
    with open("games.json", "w") as f:
        f.write(json.dumps(games, sort_keys=True,
                           indent=4, separators=(',', ': ')))


def get_games():
    """read the list of known games."""
    if not os.path.isfile("games.json"):
        open("games.json", 'a').close()

    with open("games.json", "r") as f:
        fileContent = f.read()
    try:
        games = json.loads(fileContent)
    except ValueError:
        games = {}


    collections.OrderedDict(sorted(games.items()))
    return games
