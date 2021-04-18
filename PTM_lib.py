from summonerinfo import *


class InvalidPlayerListException(Exception):
    __slots__ = ["__message"]

    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return f'Error: {self.__message}'


def tournament_5v5_team_contains_role(team: list, role: Role):
    for player in team:
        if player.getAssignedRole() == role:
            return True
    return False


def tournament_5v5_zigzag_assign(players: list, teams_dict: dict, teams_fills_dict: dict, team_id: int):
    player = players.pop(0)
    if not tournament_5v5_team_contains_role(teams_dict[f'Team{team_id}'], player.getPrimaryRole()):
        # team does not contain player's primary, add them as primary
        player.setAssignedRole(player.getPrimaryRole())
        teams_dict[f'Team{team_id}'] += [player]
    elif not tournament_5v5_team_contains_role(teams_dict[f'Team{team_id}'], player.getSecondaryRole()):
        # team does not contain player's second, add them as secondary
        player.setAssignedRole(player.getSecondaryRole())
        teams_dict[f'Team{team_id}'] += [player]
    else:
        # otherwise, make them fill
        player.setAssignedRole(Role.FILL)
        teams_fills_dict[f'Team{team_id}'] += [player]


# TODO: fix this for tomorrow
def tournament_5v5_fix_collisions(team: list, team_fills: list):
    roles_missing = {Role.TOP.name, Role.JUNGLE.name, Role.MID.name, Role.ADC.name, Role.SUPPORT.name}
    for player in team:
        roles_missing.discard(player.getAssignedRole().name)
    # roles_missing now contains all roles that are missing, and is equal in size to the number of fill players
    # team_fills: idx=0 is lower mmr than last index, so go through backwards
    for i in range(len(team_fills)-1, -1, -1):
        player = team_fills[i]
        if roles_missing.__contains__(Role.MID.name):
            # set player as mid if it isn't taken
            roles_missing.discard(Role.MID.name)
            player.setAssignedRole(Role.MID)
            team += [player]
        elif roles_missing.__contains__(Role.TOP.name):
            # set player as top if it isn't taken
            roles_missing.discard(Role.TOP.name)
            player.setAssignedRole(Role.TOP)
            team += [player]
        else:
            # otherwise, just pop the next role
            role = roles_missing.pop()
            player.setAssignedRole(str_to_role(role))
            team += [player]


"""
Greedy team balancing algorithm for creating 2 or more teams of 5 players
@pre: Total number of players must be a multiple of 5
@return dict<str, list<Player>>, or None if not a multiple of 5
"""
def tournament_5v5(players: list, gamemode_list: list):
    # check if list of players is valid
    size: int = len(players)
    if (size < 10 or size % 5 != 0):
        raise InvalidPlayerListException("Insufficient number of players for PTM.tournament_5v5")
    # run actual algorithm
    # (1) sort players by MMR
    players = sort_players_by_mmr(players, gamemode_list, descending=False)
    # (2) get the number of teams
    num_teams = size // 5
    # set teams with num_teams highest players as "captains"
    teams = {}
    teams_fills = {}
    for i in range(1, num_teams+1):
        teams[f'Team{i}'] = [players.pop(0)]
        teams_fills[f'Team{i}'] = []
    # zig-zag back and forth adding the next highest player TODO: fix this for tomorrow
    for i in range(4):
        if (i % 2 == 0):
            # add backwards
            for j in range(num_teams, 0, -1):
                tournament_5v5_zigzag_assign(players, teams, teams_fills, j)
        else:
            # add forwards
            for j in range(1, num_teams+1):
                tournament_5v5_zigzag_assign(players, teams, teams_fills, j)
    # now check that each team is compatible
    #     Note: Each list in teams and teams_fills are sorted in increasing order
    for i in range(1, num_teams+1):
        tournament_5v5_fix_collisions(teams[f'Team{i}'], teams_fills[f'Team{i}'])
    return teams
