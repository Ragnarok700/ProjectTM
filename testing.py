from summonerinfo import *
from tournament_5v5 import *
import utils

api_key = utils.read_key()
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
teams = tournament_5v5(players, [GameMode.NORMAL, GameMode.RANKED])