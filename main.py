import requests
import json
from config.riot import get_riotapiKey

matchTESTE = 'BR1_2562534854'
match = 'BR1_2560082028'
urlMatch = 'https://americas.api.riotgames.com/lol/match/v5/matches/{}'.format(match)
urlMatchTimeline = 'https://americas.api.riotgames.com/lol/match/v5/matches/{}/timeline'.format(match)
urlSummonersRank = 'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/'
minutes = 10


key = get_riotapiKey()

def getFirstTeamObjetives(teamList):

    finalObj = {
            'result':       '',
            'Firstchampion':   '',
            'Firstdragon':  '',
            'Firstbaron':   '',
            'Firsttower':   '',
            'Firstinhibitor':    '',
            'FirstriftHerald':  ''
    }

    for team in teamList:
        if(team['teamId'] == 100):
            if(team['win'] == True):
                result = 'blue'
                finalObj.update({'result': 'blue'})
            for objetive in team['objectives'].items():

                if(objetive[1]['first'] == True):
                    finalObj.update({'{}'.format('First' + objetive[0]): 'blue'})
        elif(team['teamId'] == 200):
            if(team['win'] == True):
                result = 'red'
                finalObj.update({'result':'red'})
            for objetive in team['objectives'].items():
                if(objetive[1]['first'] == True):
                    finalObj.update({'{}'.format('First' + objetive[0]): 'red'})
    print(finalObj)
    return finalObj

def getTeamsDetails(jsonResponseMatch):
    getFirstTeamObjetives(jsonResponseMatch['info']['teams'])


def getRankParticipants(jsonResponseMatch):
    listParticipants = []

    for participant in jsonResponseMatch['info']['participants']:  ###get summoner id to check its rank
        ranks = []
        objectTierSolo = {
            'QueueType': '',
            'Tier': '',
            'Rank': ''
        }

        objectTierFlex = {
            'QueueType': '',
            'Tier': '',
            'Rank': ''
        }
        requestSummonerRank = requests.get('{}{}'.format(urlSummonersRank, participant['summonerId']),
                                           headers={'X-Riot-Token': key})
        jsonResponseSummonerRank = requestSummonerRank.json()

        for SummonersRank in jsonResponseSummonerRank:
            if SummonersRank['queueType'] == 'RANKED_SOLO_5x5':
                objectTierSolo.update({'QueueType': SummonersRank['queueType'],
                                       'Tier': SummonersRank['tier'],
                                       'Rank': SummonersRank['rank']})
                ranks.append(objectTierSolo)
            if SummonersRank['queueType'] == 'RANKED_FLEX_SR':
                objectTierFlex.update({'QueueType': SummonersRank['queueType'],
                                       'Tier': SummonersRank['tier'],
                                       'Rank': SummonersRank['rank']})

                ranks.append(objectTierFlex)
        listParticipants.append(ranks)

    return listParticipants

def getTeamStats(info):
    finalTeamStats = {
        'goldRedTeamAt10': 0,
        'goldBlueTeamAt10': 0,
        'xpRedTeamAt10': 0,
        'xpBlueTeamAt10': 0,
        'totalCsRedTeamAt10': 0,
        'totalCsBlueTeamAt10': 0,
    }
    totalGoldBlue = 0
    blueTeam = tuple(range(1,5))
    redTeam = range(6,10)

    for minute in range(10):
        print('Minute{}'.format(minute))
        for player in info['frames'][minute]['participantFrames'].items():
            print(player)
            if player[0] in blueTeam:
                print('time azul')
            print(player[1]['totalGold'])

    return finalTeamStats


def getMatch(urlMatch):
    requestMatchTimeLine = requests.get('{}'.format(urlMatchTimeline),
                                        headers={'X-Riot-Token': key}
                                        )

    requestMatch = requests.get('{}'.format(urlMatch),
                                headers={'X-Riot-Token': key}
                                )

    jsonResponseMatchTimeLine = requestMatchTimeLine.json()
    jsonResponseMatch = requestMatch.json()

    with open('timelineMetadata.txt', 'w') as meta:
        json.dump(jsonResponseMatchTimeLine['metadata'], meta)

    with open('matchTimelineInfo.txt', 'w') as info:  ##get matchInfo by timeline events (every 60 seconds)
        json.dump(jsonResponseMatchTimeLine['info'], info)

    with open('matchInfo.txt', 'w') as matchInfo:  ##get matchInfo
        json.dump(jsonResponseMatch['info'], matchInfo)

    #getRankParticipants(jsonResponseMatch) -> done
    #getTeamsDetails(jsonResponseMatch) -> done
    getTeamStats(jsonResponseMatchTimeLine['info'])

if __name__ == '__main__':
    print(getMatch(urlMatch))
