import json
import requests


BASE_URL = 'http://data.nba.com'


class NBATeam:
    def __init__(self, gameInfo, isHomeTeam):
        teamKey = 'hTeam' if isHomeTeam else 'vTeam'
        # TODO: add method to extract full team name
        # extract the request info
        self.name = gameInfo[teamKey]['triCode']
        self.pointsScored = gameInfo[teamKey]['score']
        self.seasonWins = gameInfo[teamKey]['win']
        self.seasonLosses = gameInfo[teamKey]['loss']

        
    def __str__(self):
        return f"Name: {self.name} Scored: {self.pointsScored}"


class NBAGame:
    def __init__(self, gameData):
        self.__homeTeam = NBATeam(gameData, isHomeTeam=True)
        self.__visitingTeam = NBATeam(gameData, isHomeTeam=False)
        
        self.__hasStarted = False if gameData['statusNum'] == 1 else True
        self.__startDateTime = gameData['startTimeUTC'] # TODO: transform into local date and time
        self.__highlightInfo = gameData['nugget']['text']


    def __str__(self):
        return f"{self.__homeTeam} - {self.__visitingTeam}"

    def print(self):
        print(f'GAME STARTED: {self.__hasStarted}')
        print(f'{self.__homeTeam.name} vs {self.__visitingTeam.name}')
        if self.__hasStarted:
            print(f'{self.__homeTeam.pointsScored} - {self.__visitingTeam.pointsScored}')
            print(self.__highlightInfo)


class NBAGameDay:
    def __init__(self):
        self.games = []
        self.numGames = -1
        self.initialized = False

    def __getDataRemote(self, gameDayDate):
        requestURL = f'{BASE_URL}/data/10s/prod/v1/{gameDayDate}/scoreboard.json'
        response = requests.get(requestURL)
        if response.status_code != 200:
            raise ConnectionError(
                f'Failed to connect to {requestURL}'
            )
        
        requestData = json.loads(response.content)
        return requestData

    def __getDataLocalFile(self, filename):
        with open(filename) as dataFile:
            fileData = json.load(dataFile)
        return fileData

    def __initData(self, gameDayData):
        self.numGames = gameDayData['numGames']
        for game in gameDayData['games']:
            self.games.append(NBAGame(game))

        self.initialized = True

    def initDataLocalFile(self,filename):
        gameDayData = self.__getDataLocalFile(filename)
        self.__initData(gameDayData)

    def initDataRemote(self, date):
        gameDayData = self.__getDataRemote(date)
        self.__initData(gameDayData)

    def print(self):
        if not self.initialized:
            raise ValueError(
                'Object not initialized'
            )
        print(f"Num of Games: {self.numGames}\n")
        for i, game in enumerate(self.games):
            print(f'Game {i+1} of {self.numGames}')
            game.print()
            print(f'\n')
