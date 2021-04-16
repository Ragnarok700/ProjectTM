from summonerinfo import *

class InvalidPlayerListException(Exception):
    __slots__ = ["__message"]

    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return f'Error: {self.__message}'

def tournament_5v5_team_contains_role(team: list, role: Role):
    for player in team:
        if player.getPrimaryRole() == role:
            return True
    return False

# TODO: fix this for tomorrow
def tournament_5v5_check_collisions(team: list):
    roles_covered = {Role.FILL:0, Role.TOP:0, Role.JUNGLE:0, Role.MID:0, Role.ADC:0, Role.BOT:0}
    fill_players = [player for player in team if player.getPrimaryRole() == Role.FILL]
    for player in team:
        roles_covered[player.getPrimaryRole()] += 1


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
    teams_issues = {}
    for i in range(1, num_teams+1):
        teams[f'Team{i}'] = [players.pop(0)]
        teams_issues[f'Team{i}'] = []
    # zig-zag back and forth adding the next highest player TODO: fix this for tomorrow
    for i in range(4):
        if (i % 2 == 0):
            # add backwards
            for j in range(num_teams, 0, -1):
                player = players.pop(0)
                if not tournament_5v5_team_contains_role(teams[f'Team{j}'], player.getPrimaryRole()):
                    teams[f'Team{j}'] += [player]
                elif not tournament_5v5_team_contains_role(teams[f'Team{j}'], player.getSecondaryRole()):
                    teams[f'Team{j}'] += [player]
                else:
                    teams_issues[f'Team{j}'] += [player]
        else:
            # add forwards
            for j in range(1, num_teams+1):
                player = players.pop(0)
                if not tournament_5v5_team_contains_role(teams[f'Team{j}'], player.getPrimaryRole()):
                    teams[f'Team{j}'] += [player]
                elif not tournament_5v5_team_contains_role(teams[f'Team{j}'], player.getSecondaryRole()):
                    teams[f'Team{j}'] += [player]
                else:
                    teams_issues[f'Team{j}'] += [player]
    # now check that each team is compatible
