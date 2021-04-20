"""
ProjectTM
tournament_5v5.py
Algorithm for creating League of Legends Summoner's Rift teams
"""

# Import summonerinfo library
from summonerinfo import *

# Custom Exception Class (for errors)
class InvalidPlayerListException(Exception):
    __slots__ = ["__message"]

    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return f'Error: {self.__message}'

# Checks whether a team contains a Role
def tournament_5v5_team_contains_role(team: list, role: Role):
    if role == Role.FILL:
        return True
    for player in team:
        if player.getAssignedRole() == role:
            return True
    return False

# Assigns players to teams from lowest to highest MMR
def tournament_5v5_zigzag_assign(players: list, teams_dict: dict, teams_fills_dict: dict, team_id: int):
    # Get a player
    player = players.pop(0)
    if not tournament_5v5_team_contains_role(teams_dict[f'Team{team_id}'], player.getPrimaryRole()):
        # Team does not contain the player's primary role, add them as primary role
        player.setAssignedRole(player.getPrimaryRole())
        teams_dict[f'Team{team_id}'] += [player]
    elif not tournament_5v5_team_contains_role(teams_dict[f'Team{team_id}'], player.getSecondaryRole()):
        # Team does not contain player's second role, add them as secondary role
        player.setAssignedRole(player.getSecondaryRole())
        teams_dict[f'Team{team_id}'] += [player]
    else:
        # Otherwise, make them fill
        player.setAssignedRole(Role.FILL)
        teams_fills_dict[f'Team{team_id}'] += [player]

# Fills players into a team from highest to lowest MMR, prioritizing Top and Mid (roles)
def tournament_5v5_fix_collisions(team: list, team_fills: list):
    roles_missing = {Role.TOP.name, Role.JUNGLE.name, Role.MID.name, Role.ADC.name, Role.SUPPORT.name}
    for player in team:
        roles_missing.discard(player.getAssignedRole().name)
    # roles_missing now contains all roles that are missing, and is equal in size to the number of fill players
    # team_fills: idx=0 is lower mmr than last index, so go through backwards
    for i in range(len(team_fills)-1, -1, -1):
        player = team_fills[i]
        if roles_missing.__contains__(Role.MID.name):
            # Set player as Mid if it isn't taken
            roles_missing.discard(Role.MID.name)
            player.setAssignedRole(Role.MID)
            team += [player]
        elif roles_missing.__contains__(Role.TOP.name):
            # Set player as Top if it isn't taken
            roles_missing.discard(Role.TOP.name)
            player.setAssignedRole(Role.TOP)
            team += [player]
        else:
            # Otherwise, just pop the next role
            role = roles_missing.pop()
            player.setAssignedRole(str_to_role(role))
            team += [player]

'''
Greedy team balancing algorithm for creating 2 or more teams of 5 players
@pre: Total number of players must be a multiple of 5
@return dict<str, list<Player>>, or None if not a multiple of 5
'''
def create_tournament_5v5(players: list, gamemode_list: list):
    # Check whether the list of players is valid
    size: int = len(players)
    if (size < 10 or size % 5 != 0):
        raise InvalidPlayerListException("Insufficient number of players for PTM.tournament_5v5")
    # Run actual algorithm
    # (1) Sort players by MMR
    players = sort_players_by_mmr(players, gamemode_list, descending=False)
    # (2) Get the number of teams
    num_teams = size // 5
    # (3) Set teams with num_teams highest players as "captains"
    teams = {}
    teams_fills = {}
    for i in range(1, num_teams+1):
        teams[f'Team{i}'] = []
        teams_fills[f'Team{i}'] = []
    # (4) Zig-zag back and forth adding the next highest player
    for i in range(5):
        if (i % 2 == 0):
            # add backwards
            for j in range(num_teams, 0, -1):
                tournament_5v5_zigzag_assign(players, teams, teams_fills, j)
        else:
            # add forwards
            for j in range(1, num_teams+1):
                tournament_5v5_zigzag_assign(players, teams, teams_fills, j)
    # (5) Check that each team is compatible (has no role collisions)
    # Note: Each list in teams and teams_fills are sorted in increasing order
    for i in range(1, num_teams+1):
        tournament_5v5_fix_collisions(teams[f'Team{i}'], teams_fills[f'Team{i}'])
    return teams
