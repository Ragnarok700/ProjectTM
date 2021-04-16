from summonerinfo import *

class InvalidPlayerListException(Exception):
    __slots__ = ["__message"]

    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return f'Error: {self.__message}'

"""
Greedy team balancing algorithm for creating 2 or more teams of 5 players
@pre: Total number of players must be a multiple of 5
@return dict<str, list<Player>>, or None if not a multiple of 5
"""
def tournament_5v5(players: list):
    # check if list of players is valid
    size: int = len(players)
    if (size < 10 or size % 5 != 0):
        raise InvalidPlayerListException("Insufficient number of players for PTM.tournament_5v5")
    # run actual algorithm