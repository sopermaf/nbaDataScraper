'''
This program should be able to
retrieve info on a particular
NBA team and include info on upcoming
games as well as their record
'''
import json
import sys
from nbaObjects import NBAGameDay
import datetime

def getTonightsGames():
    tonightsGames = NBAGameDay()
    tonightData = datetime.datetime.now()
    tonightDataArg = tonightData.date().isoformat()
    tonightsGames.initDataRemote(tonightDataArg)
    return tonightsGames

def getPreviousNightGames():
    previousNightGames = NBAGameDay()
    yesterdayDate = datetime.datetime.now() - datetime.timedelta(days=1)
    nbaDataArg = yesterdayDate.date().isoformat()
    previousNightGames.initDataRemote(nbaDataArg)
    return previousNightGames

def displayYesterdayAndToday():
    todayGames = getTonightsGames()
    yesterGames = getPreviousNightGames()

    print("***RESULTS FROM LAST NIGHT***")
    yesterGames.print()
    print("**UPCOMING GAMES***")
    todayGames.print()

if __name__=="__main__":
    if len(sys.argv) < 2:
        displayYesterdayAndToday()
    else:
        dayData = NBAGameDay()
        retrievalMethod = sys.argv[1] # -f || -r
        retrievalRef = sys.argv[2] # filename or date YYYYMMDD
        if retrievalMethod == '-f':
            dayData.initDataLocalFile(retrievalRef)
        elif retrievalMethod == '-r':
            dayData.initDataRemote(retrievalRef)
        else:
            raise ValueError(
                'INVALID ARGS'
            )
        dayData.print()
