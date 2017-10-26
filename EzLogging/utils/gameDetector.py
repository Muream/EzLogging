import subprocess
import json
import collections
import os
from EzLogging.core.config import Config

class GameDetector(object):

    def __init__(self):
        self.gamesListFile = os.path.join(config.configFolder, "games.json")

    @classmethod
    def get_processes(self):
        """List all the running processes."""
        cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        processes = []

        for line in proc.stdout:
            process = line.split(' ')[0]
            processes.append(process)
        return processes

    @classmethod
    def running_games(self):
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

    @classmethod
    def add_game(self, process, game):
        """Add a game to the list of known games."""
        games = get_games()
        if process not in games:
            games[process] = game
        with open(self.gamesListFile, "w") as f:
            f.write(json.dumps(games, sort_keys=True,
                            indent=4, separators=(',', ': ')))

    @classmethod
    def get_games(self):
        """read the list of known games."""
        if not os.path.isfile(self.gamesListFile):
            open(self.gamesListFile, 'a').close()

        with open(self.gamesListFile, "r") as f:
            fileContent = f.read()
        try:
            games = json.loads(fileContent)
        except ValueError:
            games = {}

        collections.OrderedDict(sorted(games.items()))
        return games
