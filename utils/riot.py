import os
import pandas as pd
import time
import discord

from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError


# Load environment variables
load_dotenv()
LOL_API_KEY = os.getenv('LEAGUE_API')

# global variables
watcher = LolWatcher(LOL_API_KEY)
my_region = 'oc1'


def printplayer(ign):
    player = watcher.summoner.by_name(my_region, ign)
    msg = (
        f"{player['name']} is level {player['summonerLevel']}"
    )
    return msg


def printrank(ign):
    player = watcher.summoner.by_name(my_region, ign)
    rankedstats = watcher.league.by_summoner(my_region, player['id'])
    msg = (
        f"{rankedstats[1]['summonerName']} is hardstuck {rankedstats[1]['tier']} {rankedstats[1]['rank']} in soloqueue HAH!"
    )
    return msg


def printlastmatch(ign):
    print('Retrieving player matches...')
    player = watcher.summoner.by_name(my_region, ign)
    my_matches = watcher.match.matchlist_by_account(
        my_region, player['accountId'])

    # Fetch last match detail
    last_match = my_matches['matches'][0]
    match_detail = watcher.match.by_id(my_region, last_match['gameId'])

    # Lets get some champions static information (11.9.1 is champion version)
    print('Retrieving static data...')
    static_champ_list = watcher.data_dragon.champions('11.9.1', False, 'en_US')

    # Champ static list data to dict for looking up
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']

    # Processing data into 2D array
    print('Processing Data...')
    participants = []
    hasWon = 0
    for row in match_detail['participants']:
        participants_row = {}
        PlayerName = match_detail['participantIdentities'][row['participantId'] -
                                                           1]['player']['summonerName']
        if(PlayerName == ign and row['stats']['win'] == True):
            hasWon = 1
        participants_row['Player'] = PlayerName
        participants_row['Champion'] = champ_dict[str(row['championId'])]
        participants_row['Level'] = row['stats']['champLevel']
        participants_row['KDA'] = str(row['stats']['kills']) + '/' + \
            str(row['stats']['deaths']) + '/' + str(row['stats']['assists'])
        participants_row['Damage Dealt'] = row['stats']['totalDamageDealt']
        participants_row['Total Gold'] = row['stats']['goldEarned']
        participants_row['CS'] = row['stats']['totalMinionsKilled']
        participants.append(participants_row)
    print('... SUCCESS!\n')

    # Create message
    datetime = time.strftime(
        '%A, %B %-d', time.localtime(match_detail['gameCreation']))

    data = '```' + str(pd.DataFrame(participants)) + '```'
    msg = f"{ign} **{'won' if hasWon else 'lost'}** his last game on {datetime}.\nHere are the details:\n{data}"

    return msg


# print(printlastmatch('TheHotDogThing'))