import json
import requests
import re
from datetime import datetime


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

    def getTeamRecord(self):
        return f"{self.seasonWins}-{self.seasonLosses}"
        
    def __str__(self):
        return f"Name: {self.name} Scored: {self.pointsScored}"


class NBAGame:
    def __init__(self, gameData):
        self.__homeTeam = NBATeam(gameData, isHomeTeam=True)
        self.__visitingTeam = NBATeam(gameData, isHomeTeam=False)
        
        self.__hasStarted = False if gameData['statusNum'] == 1 else True
        self.__highlightInfo = gameData['nugget']['text']

        self.__startDateTime = NBAGame.transformDateTimeToReadable(
                                    gameData['startTimeUTC']
                               )
        

    @staticmethod
    def transformDateTimeToReadable(nbaFormatDateTime):
        '''Transform the request format datetime
        to a human readable format for presentation
        '''
        # TODO: add in time localisation for user
        dtObj = datetime.strptime(nbaFormatDateTime, '%Y-%m-%dT%X.%fZ')
        return dtObj.strftime('%H:%M %a %d-%m-%y')

    def __str__(self):
        return f"{self.__homeTeam} - {self.__visitingTeam}"

    def print(self):
        #print(f'GAME STARTED: {self.__hasStarted}')
        print(f'{self.__startDateTime}')
        print('{0} vs {2}\n({1}) ({3})'.format(
            self.__homeTeam.name,
            self.__homeTeam.getTeamRecord(),
            self.__visitingTeam.name,
            self.__visitingTeam.getTeamRecord(),
        ))
        if self.__hasStarted:
            print(f'{self.__homeTeam.pointsScored} - {self.__visitingTeam.pointsScored}')
            print(self.__highlightInfo)


class NBAGameDay:
    def __init__(self):
        self.games = []
        self.numGames = -1
        self.initialized = False

    @staticmethod
    def converIsoDateToNbaDate(isoDate):
        return re.sub('-', '', isoDate)

    def __getDataRemote(self, isoDate):
        gameDayDate = NBAGameDay.converIsoDateToNbaDate(isoDate)
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
