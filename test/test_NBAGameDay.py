from nbaObjects import NBAGameDay

def test_isoDataConversion():
    nbaGameDate = (NBAGameDay
                   .converIsoDateToNbaDate(
                        '2019-01-01'
                    )
                ) 
    
    assert nbaGameDate == "20190101"