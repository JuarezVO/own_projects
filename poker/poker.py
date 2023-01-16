import pandas as pd, json, time, numpy as np
from funcs import *
from multiprocessing import Pool, cpu_count
from functools import partial

'''
sources:
https://archive.ics.uci.edu/ml/datasets/Poker+Hand
https://raw.githubusercontent.com/goldsmith/poker-hand-ml/master/data/test.csv
https://github.com/BrenoCPimenta/Poker-preflop-hand-rank-scraping-to-csv/blob/master/preflopCrawler.ipynb
'''

def resolve_game(games, hand_cards, hand_suits):
  game_result = []
  iteraction = 0
  for idx_g, game in games.iterrows():
    print(f'Processo {iteraction} de {len(games)}')
    flop_suits = list(game[['s1','s2','s3']].values.tolist())
    flop_cards = list(game[['c1','c2','c3']].values.tolist())
    
    cards = hand_cards + flop_cards
    suits = hand_suits + flop_suits

    game_result.append(result(cards,suits))
    iteraction+=1
    
  games['result'] = game_result
  return games

if __name__ == '__main__':
  hands = pd.read_csv('hands.csv')
  games = pd.read_csv('games.csv')
  codes = json.load(open('codes.json','r'))
  ncpus = cpu_count() - 1
  pool = Pool(ncpus)

  t1 = time.time()

  for idx_h,hand in hands.iloc[0:4].iterrows():
    hand_suits = list(hand[['s1','s2']].values.tolist())
    hand_cards = list(hand[['h1','h2']].values.tolist())
    
    games_work = games.drop('id',axis=1)
    games_work['hand_card_1'] = hand['h1']
    games_work['hand_card_2'] = hand['h2']
    games_work['hand_suit_1'] = hand['s1']
    games_work['hand_suit_2'] = hand['s2']
    games_work = np.array_split(games_work,cpu_count()-1)

    x = list(map(partial(resolve_game,hand_cards=hand_cards, hand_suits=hand_suits),games_work))
    x = pd.concat(x)
    print(x)
  
    
  print(f'Tempo total: {time.time() - t1}s')


# t1 = time.time()
# n = 0
# for idx_h,hand in hands.iloc[0:4].iterrows():
#   games_result = games.drop('id',axis=1)
#   games_result['hand_card_1'] = hand['h1']
#   games_result['hand_card_2'] = hand['h2']
#   games_result['hand_suit_1'] = hand['s1']
#   games_result['hand_suit_2'] = hand['s2']
#   games_result['result'] = pd.NA
#   for idx_g, game in games_result.iterrows():
#     hand_suits = list(hand[['s1','s2']].values.tolist())
#     hand_cards = list(hand[['h1','h2']].values.tolist())
#     flop_suits = list(game[['s1','s2','s3']].values.tolist())
#     flop_cards = list(game[['c1','c2','c3']].values.tolist())
    
#     cards = hand_cards + flop_cards
#     suits = hand_suits + flop_suits
    
#     games_result['result'].iloc[idx_g] = result(cards,suits)
#   games_result = games_result.drop(['s4','c4','s5','c5'],axis=1).to_csv(f'try_n{n}.csv',index=False)
#   n+=1
# print(f'Tempo total: {time.time() - t1}s')
# quit()
      