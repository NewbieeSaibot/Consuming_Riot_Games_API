import pandas as pd
import numpy as np
from riotwatcher import LolWatcher, ApiError

riot_api_key = "RGAPI-33346d0a-02c3-409d-8ca3-18ab1cccd5fa"
watcher =  LolWatcher(riot_api_key)

my_region = "br1"
me = watcher.summoner.by_name(my_region, "tobiasrm")
print(watcher.league.by_summoner(my_region, me['id']))

df = pd.read_csv('./data/cblol.csv',';')

def function_of_god(team, round):
    points = 0
    for i in range(round*4):
        if(i > 0 or i > (round-4)*4):
            if(df['time1'][i] == team and df['vencedor'][i] == 0):
                points += 1
                points += function_of_god(df['time2'][i], round - 1)
            if (df['time2'][i] == team and df['vencedor'][i] == 1):
                points += 1
                points += function_of_god(df['time1'][i], round - 1)
    return points

def evaluate():
    resposta = total = 0
    for i in range(0,len(df),1):
        total += 1
        if(tabela(int(i/4))[df['time1'][i]] > tabela(int(i/4))[df['time2'][i]]):
            if(df['vencedor'][i] == 0):
                resposta += 1
        else:
            if (df['vencedor'][i] == 1):
                resposta += 1
    return resposta,total

def tabela(round):
    times = {'pain': 0, 'fla': 0, 'prg': 0, 'santos': 0,'keyd': 0,'furia': 0,'kabum': 0, 'intz': 0}
    for i in range(round*4):
        if(df['vencedor'][i] == 0):
            times[df['time1'][i]] += 1
        else:
            times[df['time2'][i]] += 1
    return times

def get_last_match(me, region):
    my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])

    # fetch last match detail
    last_match = my_matches['matches'][0]
    match_detail = watcher.match.by_id(my_region, last_match['gameId'])

    participants = []
    for row in match_detail['participants']:
        participants_row = {}
        participants_row['champion'] = row['championId']
        participants_row['spell1'] = row['spell1Id']
        participants_row['spell2'] = row['spell2Id']
        participants_row['win'] = row['stats']['win']
        participants_row['kills'] = row['stats']['kills']
        participants_row['deaths'] = row['stats']['deaths']
        participants_row['assists'] = row['stats']['assists']
        participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
        participants_row['goldEarned'] = row['stats']['goldEarned']
        participants_row['champLevel'] = row['stats']['champLevel']
        participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
        participants_row['item0'] = row['stats']['item0']
        participants_row['item1'] = row['stats']['item1']
        participants.append(participants_row)

    # check league's latest version
    latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
    # Lets get some champions static information
    static_champ_list = watcher.data_dragon.champions(latest, False, 'pt_BR')
    # champ static list data to dict for looking up
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict[row['key']] = row['id']
    for row in participants:
        print(str(row['champion']) + ' ' + champ_dict[str(row['champion'])])
        row['championName'] = champ_dict[str(row['champion'])]

    df = pd.DataFrame(participants)
    print(df)

#get_last_match(me, my_region)
#print(tabela(15))
print(evaluate())

