import csv
from summonerinfo import *
from app import api_key

def parse_player_data(player_data: list) -> Player:
    player_name = player_data[0]
    discord_id = player_data[1]
    summoner_name = player_data[2]
    primary_role = str_to_role(player_data[3].upper())
    secondary_role = str_to_role(player_data[4].upper())
    summoner = create_summoner(summoner_name, 'na1', api_key)
    print(summoner)
    return Player(player_name, primary_role, secondary_role, summoner)

def read_player_data(csvfile):
    print("opened!!")
    csv_reader = csv.reader(csvfile, delimiter=',')
    players = []
    for data in csv_reader:
        # player data = [Player Name, Discord ID, Summoner Name, Primary Role, Secondary Role]
        players += [parse_player_data(data)]
    for player in players:
        print(player)
    return players
