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
    # Try retrieve summoner data
    try:
        player = watcher.summoner.by_name(my_region, ign)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(
                err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            return 'That summoner cannot be found.'
        else:
            raise

    msg = (
        f"{player['name']} is level {player['summonerLevel']}"
    )
    return msg


def printrank(ign, queuetype):
    # Try retrieve summoner data
    try:
        player = watcher.summoner.by_name(my_region, ign)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(
                err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            return 'That summoner cannot be found.'
        else:
            raise

    rankedstats = watcher.league.by_summoner(my_region, player['id'])

    msg = 'You either do not have a rank, or you have not used the right queue type, select from either `flex` or `solo`'

    for i in range(len(rankedstats)):
        if (queuetype == 'flex' and rankedstats[i]['queueType'] == 'RANKED_FLEX_SR'):
            msg = (
                f"{rankedstats[i]['summonerName']} is hardstuck {rankedstats[i]['tier']} {rankedstats[i]['rank']} in flex queue!"
            )
        elif (queuetype == 'solo' and rankedstats[i]['queueType'] == 'RANKED_SOLO_5x5'):
            msg = (
                f"{rankedstats[i]['summonerName']} is hardstuck {rankedstats[i]['tier']} {rankedstats[i]['rank']} in solo queue!"
            )

    return msg


def printlastmatch(ign):
    # Try retrieve summoner data
    print('Retrieving player matches...')
    try:
        player = watcher.summoner.by_name(my_region, ign)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(
                err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            return 'That summoner cannot be found.'
        else:
            raise

    # Try retrieve match history
    try:
        my_matches = watcher.match.matchlist_by_account(
            my_region, player['accountId'])
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(
                err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            return 'Could not find any games for that summoner.'
        else:
            raise

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
    msg = f"{ign} **{'won' if hasWon else 'lost'}** their last game on {datetime}.\nHere are the details:\n{data}"

    return msg


# print(printlastmatch('TheHotDogThing'))
