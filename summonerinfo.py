'''
Attributions:

Title: Riot Games API
Author: Riot Games
Source: https://developer.riotgames.com/terms
License: Riot Games Community License

Title: What Is My MMR?
Author: Josh (https://www.patreon.com/whatismymmr)
Source: https://dev.whatismymmr.com/
License: Creative Commons Attribution 2.0 Generic (CC BY 2.0)
'''

# Imports
from riotwatcher import LolWatcher, ApiError
from enum import Enum
from typing import Union
import utils

# Global Variables

#try:
#    watcher = LolWatcher(api_key)
#
#    my_region = 'na1'
#
#    me = watcher.summoner.by_name(my_region, 'Doublelift')
#    print(me)
#
#    # all objects are returned (by default) as a dict
#    my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
#    print(my_ranked_stats)
#except:
#    print("RIOT API KEY NOT VALID")

##### CONSTANTS #####

# Summoner LolWatcher API keys
SUMMONER_NAME_KEY = "summonerName"
TIER_KEY = "tier"
DIVISION_KEY = "rank"

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

class Division(Enum):
    IV = 0
    III = 1
    II = 2
    I = 3

# Encapsulates Summoner data and provides getters for fetching summoner info
class Summoner:
    __slots__ = ["__name", "__level","__tier", "__division", "__MMR_ranked", "__MMR_normal", "__MMR_ARAM", "__LP"]

    def __init__(self, __name: str, __level: int, __tier: Tier, __division: Division, __LP: int, __MMR_ranked: int, __MMR_normal: int, __MMR_ARAM: int ):
        self.__name = __name
        self.__level = __level
        self.__tier = __tier
        self.__division = __division
        self.__MMR_ranked = __MMR_ranked
        self.__MMR_normal = __MMR_normal
        self.__MMR_ARAM = __MMR_ARAM
        self.__LP = __LP

    def getName(self) -> str:
        return self.__name

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

"""
Compares two ranks first by tier, then by division
@return < 0 if rank1 < rank2, > 0 if rank1 > rank2, 0 if rank1 == rank2
"""
def compare_rank(rank1: (Tier, Division), rank2: (Tier, Division)):
    if (rank1[0].value < rank2[0].value):
        return -1
    elif (rank1[0].value > rank2[0].value):
        return 1
    else:
        if (rank1[1].value < rank2[1].value):
            return -1
        elif (rank1[1].value > rank2[1].value):
            return 1
        else:
            return 0

"""
Gets the highest rank from list of a player's rank dictionaries
@return the largest rank dictionary, or empty dictionary if list is empty
"""
def get_highest_rank(rank_data: list) -> dict:
    if len(rank_data) == 0:
        return {}
    elif len(rank_data) == 1:
        return rank_data[0]
    else:
        max_rank_data = rank_data[0]
        for rank in rank_data[1:]:
            if compare_rank(get_rank_tuple(rank[TIER_KEY], rank[DIVISION_KEY]), get_rank_tuple(max_rank_data[TIER_KEY], max_rank_data[DIVISION_KEY])) > 0:
                max_rank_data = rank
        return max_rank_data

"""
Creates a summoner by fetching summoner data from Riot API using RiotWatcher library
@return Summoner instance or None if summoner cannot be fetched by API
"""
def create_summoner(name: str, region: str, api_key: str) -> Union[Summoner, None]:
    watcher = LolWatcher(api_key)
    my_region = region

    try:
        summoner_by_name = watcher.summoner.by_name(my_region, name)
        summoner_ranked_data = watcher.league.by_summoner(my_region, summoner_by_name['id'])

        if (len(summoner_ranked_data) == 0):
            # create unranked player
            pass

        highest_rank_data = get_highest_rank(summoner_ranked_data)

    except ApiError as err:
        print("Encountered an error fetching user data.")

    return None

def main():
    api_key = utils.read_key()
    print(api_key)
    create_summoner('Doublelift', 'na1', api_key)
    create_summoner('bean217', 'na1', api_key)
    create_summoner('Willie', 'na1', api_key)
    create_summoner('Jason Woodrue', 'na1', api_key)

if __name__ == "__main__":
    main()