'''
This program should be able to
retrieve info on a particular
NBA team and include info on upcoming
games as well as their record
'''
import json
from nbaObjects import NBAGameDay

dayData = NBAGameDay()

dayData.initDataLocalFile('mock_data/pastGameData.json')
#dayData.initDataRemote('20191122')

dayData.print()
