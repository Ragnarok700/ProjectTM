"""
ProjectTM
summonerinfo.py
Serves as the Model for the Application by making API calls to get player data

Attributions:

Title: Riot Games API
Author: Riot Games
Source: https://developer.riotgames.com/terms
License: Riot Games Community License

Title: What Is My MMR?
Author: Josh (https://www.patreon.com/whatismymmr)
Source: https://dev.whatismymmr.com/
License: Creative Commons Attribution 2.0 Generic (CC BY 2.0)
"""

# Imports
from riotwatcher import LolWatcher, ApiError
from enum import Enum
from typing import Union

import utils
import requests

##### GLOBAL CONSTANTS #####

# Summoner LolWatcher API keys
LP_KEY = "leaguePoints"
ICON_ID_KEY = "profileIconId"
LEVEL_KEY = "summonerLevel"
SUMMONER_NAME_KEY = "summonerName"
TIER_KEY = "tier"
DIVISION_KEY = "rank"

# Summoner WhatIsMyMMR API keys
MMR_RANKED_KEY = "ranked"
MMR_NORMAL_KEY = "normal"
MMR_ARAM_KEY = "ARAM"
MMR_AVG_KEY = "avg"

##### Gathering Summoner Data #####

# List of Possible Summoner Rankings (from lowest to highest)
class Tier(Enum):
    UNRANKED = 0
    IRON = 1
    BRONZE = 2
    SILVER = 3
    GOLD = 4
    PLATINUM = 5
    DIAMOND = 6
    MASTER = 7
    GRANDMASTER = 8
    CHALLENGER = 9

# List of Possible Summoner Tier Divisions (from lowest to highest ranked)
class Division(Enum):
    UNRANKED = 0
    IV = 1
    III = 2
    II = 3
    I = 4

# Enum of possible role options
class Role(Enum):
    FILL = 0
    TOP = 1
    JUNGLE = 2
    MID = 3
    ADC = 4
    SUPPORT = 5

# Convert a string to a role enum if the string represents a role
def str_to_role(role_str: str):
    if (role_str == 'FILL'):
        return Role.FILL
    elif (role_str == 'TOP'):
        return Role.TOP
    elif (role_str == 'JUNGLE'):
        return Role.JUNGLE
    elif (role_str == 'MID'):
        return Role.MID
    elif (role_str == 'ADC'):
        return Role.ADC
    elif (role_str == 'SUPPORT'):
        return Role.SUPPORT
    else:
        raise Exception(f"role_str 'Role.{role_str}' is not a valid role")

# Enum of possible matchmaking rating (MMR) types
class GameMode(Enum):
    RANKED = 0
    NORMAL = 1
    ARAM = 2

# Encapsulates Summoner data and provides getters for fetching summoner info
class Summoner:
    __slots__ = ["__name", "__icon_id", "__level","__tier", "__division", "__MMR_ranked", "__MMR_normal", "__MMR_ARAM", "__LP"]

    # Constructor for the Summoner Class
    def __init__(self, __name: str, __icon_id: int, __level: int, __tier: Tier, __division: Division,__MMR_ranked: int, __MMR_normal: int, __MMR_ARAM: int, __LP: int):
        self.__name = __name
        self.__icon_id = __icon_id
        self.__level = __level
        self.__tier = __tier
        self.__division = __division
        self.__MMR_ranked = __MMR_ranked
        self.__MMR_normal = __MMR_normal
        self.__MMR_ARAM = __MMR_ARAM
        self.__LP = __LP

    # toString of the Summoner Class
    def __str__(self):
        return f'Summoner: {self.__name}\n\t' + \
            f'icon_id: {self.__icon_id}\n\t' + \
            f'level: {self.__level}\n\t' + \
            f'tier: {self.__tier.name}\n\t' + \
            f'division: {self.__division.name}\n\t' + \
            f'mmr_ranked: {self.__MMR_ranked}\n\t' + \
            f'mmr_normal: {self.__MMR_normal}\n\t' + \
            f'mmr_ARAM: {self.__MMR_ARAM}\n\t' + \
            f'LP: {self.__LP}'

    # Get a Summoner's MMR based on the Gamemode enum
    def getGameModeMMR(self, gamemode: GameMode) -> int:
        if gamemode == GameMode.RANKED:
            return self.__MMR_ranked
        elif gamemode == GameMode.NORMAL:
            return self.__MMR_normal
        else:
            return self.__MMR_ARAM

    # Get's the Summoner's highest MMR based on a list of Gamemode enums
    def getMaxMMR(self, gamemode_list: list):
        if len(gamemode_list) < 1 or len(gamemode_list) > 3:
            return -1
        max = -1
        for arg in gamemode_list:
            new_max = self.getGameModeMMR(arg)
            if new_max > max:
                max = new_max
        return max

    ### Public Accessors ###

    def getName(self) -> str:
        return self.__name

    def getIcon(self) -> int:
        return self.__icon_id

    def getLevel(self) -> int:
        return self.__level

    def getMMR_ranked(self) -> int:
        return self.__MMR_ranked

    def getLP(self) -> int:
        return self.__LP

    def getMMR_normal(self) -> int:
        return self.__MMR_normal

    def getMMR_ARAM(self) -> int:
        return self.__MMR_ARAM

    # Comparison function for Summoner MMR
    # return 1 if self > other
    # return 0 if self = other
    # return -1 if self < other
    def cmp_mmr(self, other, gamemode_list: list):
        self_mmr = self.getMaxMMR(gamemode_list)
        other_mmr = other.getMaxMMR(gamemode_list)
        if self_mmr > other_mmr:
            return 1
        elif self_mmr < other_mmr:
            return -1
        else:
            return 0

"""
Encapsulates the tournament participants registration data
"""
class Player:
    __slots__ = ["__name", "__discord_name", "__role_primary", "__role_secondary", "__assigned_role", "__summoner_data"]

    # Constructor for the Player class
    def __init__(self, name: str, primary_role: Role, secondary_role: Role, summoner_data: Summoner, discord: str=""):
        self.__name = name
        self.__discord_name = discord
        self.__role_primary = primary_role
        self.__role_secondary = secondary_role
        self.__assigned_role = primary_role
        self.__summoner_data = summoner_data

    # toString of the Player Class
    def __str__(self):
        return f'Player Name: {self.__name} -- {self.__assigned_role.name}\n\t' + \
            f'Summoner Name: {self.__summoner_data.getName()}\n\t' + \
            f'Icon ID: {self.__summoner_data.getIcon()}\n\t' + \
            f'Primary Role: {self.__role_primary.name}\n\t' + \
            f'Secondary Role: {self.__role_secondary.name}'

    ### Public Accessors ###

    def getSummoner(self):
        return self.__summoner_data

    def getName(self) -> str:
        return self.__name

    def getPrimaryRole(self) -> Role:
        return self.__role_primary

    def getSecondaryRole(self) -> Role:
        return self.__role_secondary

    def getSummonerData(self) -> Summoner:
        return self.__summoner_data

    def getAssignedRole(self) -> Role:
        return self.__assigned_role

    def setAssignedRole(self, role: Role):
        self.__assigned_role = role

    def getDiscord(self) -> str:
        return self.__discord_name

    # Comparison function for Player that calls the comparison function of their Summoner (account)
    # return 1 if self > other
    # return 0 if self = other
    # return -1 if self < other
    def cmp_mmr(self, other, gamemode_list: list):
        return self.__summoner_data.cmp_mmr(other, gamemode_list)

# Sorts players by their max MMR depending on a list of Gamemode enums
def sort_players_by_mmr(players: list, gamemode_list: list, descending: bool=True) -> list:
    players.sort(key=lambda player: player.getSummonerData().getMaxMMR(gamemode_list), reverse=descending)
    return players

# PROSPECTIVE ****
# Takes a list of players and a specific algorithm for diving players into teams to make teams
def setupMakeTeams(players: list, algorithm):
    return algorithm(players)

# Converting the String data into Enum
def get_rank_tuple(tier: str, division: str) -> (Tier, Division):
    enum_tier = Tier.IRON   # Start with Iron because Unranked is not applicable
    enum_div = Division.I   # Start with division I because there is no null division (value of 0)

    # Get Tier
    if (tier == Tier.BRONZE.name):
        enum_tier = Tier.BRONZE
    elif (tier == Tier.SILVER.name):
        enum_tier = Tier.SILVER
    elif (tier == Tier.GOLD.name):
        enum_tier = Tier.GOLD
    elif (tier == Tier.PLATINUM.name):
        enum_tier = Tier.PLATINUM
    elif (tier == Tier.DIAMOND.name):
        enum_tier = Tier.DIAMOND
    elif (tier == Tier.MASTER.name):
        enum_tier = Tier.MASTER
    elif (tier == Tier.GRANDMASTER.name):
        enum_tier = Tier.GRANDMASTER
    elif (tier == Tier.CHALLENGER.name):
        enum_tier = Tier.CHALLENGER

    # Get Division
    if (division == Division.II.name):
        enum_div = Division.II
    elif (division == Division.III.name):
        enum_div = Division.III
    elif (division == Division.IV.name):
        enum_div = Division.IV

    return (enum_tier, enum_div)

'''
Rank Comparison Function
Compares two ranks first by tier, then by division
@return < 0 if rank1 < rank2, > 0 if rank1 > rank2, 0 if rank1 == rank2
'''
def compare_rank(rank1: (Tier, Division), rank2: (Tier, Division)):
    # First, compare the tiers
    if (rank1[0].value < rank2[0].value):
        return -1
    elif (rank1[0].value > rank2[0].value):
        return 1

    # Next, compare the divisions
    else:
        if (rank1[1].value < rank2[1].value):
            return -1
        elif (rank1[1].value > rank2[1].value):
            return 1
        # Both players' tiers and divisions are equal
        else:
            return 0

'''
Get Highest Rank Function
Gets the highest rank from list of a player's rank dictionaries
When pulling player data from Riot Games API, each player has multiple ranks.
This function gets the highest of those ranks.
@return the largest rank dictionary, or empty dictionary if list is empty
'''
def get_highest_rank(rank_data: list) -> dict:
    if len(rank_data) == 0:
        return {}               # Player is Unranked
    elif len(rank_data) == 1:
        return rank_data[0]     # Player has only one rank
    else:                       # Player has more than one rank, find highest rank
        # Initialize temp highest rank
        max_rank_data = rank_data[0]

        # Iterate through ranked data to compare with current max rank
        for rank in rank_data[1:]:
            if compare_rank(get_rank_tuple(rank[TIER_KEY], rank[DIVISION_KEY]), get_rank_tuple(max_rank_data[TIER_KEY], max_rank_data[DIVISION_KEY])) > 0:
                max_rank_data = rank
        return max_rank_data

'''
Create Summoner Function
Creates a summoner by fetching summoner data from Riot Games API using RiotWatcher library
@return Summoner instance or None if summoner cannot be fetched by API
'''
def create_summoner(name: str, region: str, api_key: str) -> Union[Summoner, None]:
    # Initialize RiotWatcher and region input
    watcher = LolWatcher(api_key)
    my_region = region

    # Make API calls to fetch summoner data, soft fail if summoner data cannot be fetched
    try:
        summoner_by_name = watcher.summoner.by_name(my_region, name)    # Summoner Name
        level = int(summoner_by_name[LEVEL_KEY])                        # Summoner Level
        icon_id = int(summoner_by_name[ICON_ID_KEY])                    # Summoner Icon ID
        summoner_ranked_data = watcher.league.by_summoner(my_region, summoner_by_name['id'])    # Summoner Ranked Data

        # Make API call to fetch summoner matchamking rating (MMR) data
        request = requests.get(f'https://na.whatismymmr.com/api/v1/summoner?name={name}')   # API Call
        MMR_dict = request.json()
        mmr_ranked = MMR_dict[MMR_RANKED_KEY][MMR_AVG_KEY]
        mmr_normal = MMR_dict[MMR_NORMAL_KEY][MMR_AVG_KEY]
        mmr_aram = MMR_dict[MMR_ARAM_KEY][MMR_AVG_KEY]

        # If Ranked 5v5 MMR does not exist, set to -1
        if (mmr_ranked == None):
            mmr_ranked = -1

        # If Normal 5v5 MMR does not exist, set to -1
        if (mmr_normal == None):
            mmr_normal = -1

        # If ARAM MMR does not exist, set to -1
        if (mmr_aram == None):
            mmr_aram = -1

        # Return Unranked Summoner object if the summoner is Unranked
        if (len(summoner_ranked_data) == 0):
            return Summoner(name, icon_id, level, Tier.UNRANKED, Division.UNRANKED, mmr_ranked, mmr_normal, mmr_aram, 0)

        # Otherwise, create and return the Ranked Summoner Object
        highest_rank_data = get_highest_rank(summoner_ranked_data)

        tier, division = get_rank_tuple(highest_rank_data[TIER_KEY], highest_rank_data[DIVISION_KEY])
        LP = int(highest_rank_data[LP_KEY])

        return Summoner(name, icon_id, level, tier, division, mmr_ranked, mmr_normal, mmr_aram, LP)

    # Soft fail case for summoner name that does not exist
    except ApiError as err:
        print("Encountered an error fetching user data.")

    return None

# FOR TESTING PURPOSES ONLY
def test(api_key):
    players = []
    # s1 = create_summoner('Doublelift', 'na1', api_key)
    # players += [Player("Doublelift", Role.TOP, Role.MID, s1)]
    s1 = create_summoner('Pasteur4992', 'na1', api_key)
    players += [Player("Pasteur4992", Role.TOP, Role.SUPPORT, s1)]
    s2 = create_summoner('bean217', 'na1', api_key)
    players += [Player("bean217", Role.JUNGLE, Role.TOP, s2)]
    s3 = create_summoner('Willie', 'na1', api_key)
    players += [Player("Willie", Role.MID, Role.TOP, s3)]
    s4 = create_summoner('Jason Woodrue', 'na1', api_key)
    players += [Player("Jason Woodrue", Role.JUNGLE, Role.MID, s4)]
    s5 = create_summoner('DaaoX', 'na1', api_key)
    players += [Player("DaaoX", Role.TOP, Role.JUNGLE, s5)]
    s6 = create_summoner('jujubears', 'na1', api_key)
    players += [Player('jujubears', Role.ADC, Role.SUPPORT, s6)]
    s7 = create_summoner('Taito', 'na1', api_key)
    players += [Player('Taito', Role.ADC, Role.TOP, s7)]
    s8 = create_summoner('barrakada', 'na1', api_key)
    players += [Player('barrakada', Role.SUPPORT, Role.ADC, s8)]
    s9 = create_summoner('FrostedWolf1', 'na1', api_key)
    players += [Player('FrostedWolf1', Role.JUNGLE, Role.MID, s9)]
    s10 = create_summoner('Yen LoL', 'na1', api_key)
    players += [Player('Yen LoL', Role.MID, Role.JUNGLE, s10)]
    '''
    teams = tournament_5v5.tournament_5v5(players, [GameMode.NORMAL, GameMode.RANKED])
    i = 1
    for team in teams.values():
        print(f"\n\n### TEAM {i} ###")
        i += 1
        for player in team:
            print(player)
    '''

# FOR TESTING PURPOSES ONLY
def main():
    api_key = utils.read_key()
    print(api_key)
    print("##### TESTING #####")
    test(api_key)
    '''
    s1 = create_summoner('Doublelift', 'na1', api_key)
    p1 = Player("Doublelift", Role.TOP, Role.MID, s1)
    s2 = create_summoner('bean217', 'na1', api_key)
    p2 = Player("bean217", Role.TOP, Role.MID, s2)
    s3 = create_summoner('Willie', 'na1', api_key)
    p3 = Player("Willie", Role.TOP, Role.MID, s3)
    s4 = create_summoner('Jason Woodrue', 'na1', api_key)
    p4 = Player("Jason Woodrue", Role.TOP, Role.MID, s4)
    print(s1)
    print(s1.getMaxMMR([GameMode.NORMAL, GameMode.RANKED]))
    print(s2)
    print(s2.getMaxMMR([GameMode.NORMAL, GameMode.RANKED]))
    print(s3)
    print(s3.getMaxMMR([GameMode.NORMAL, GameMode.RANKED]))
    print(s4)
    print(s4.getMaxMMR([GameMode.NORMAL, GameMode.RANKED]))
    print(s2.cmp_mmr(s4, [GameMode.NORMAL, GameMode.RANKED]))
    print("SORTING BY MMR")
    sorted_players = sort_players_by_mmr([p1, p2, p3, p4], [GameMode.NORMAL, GameMode.RANKED])
    for p in sorted_players:
        print(p)
    '''


if __name__ == "__main__":
    main()