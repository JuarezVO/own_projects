import pandas as pd, json 
from funcs import *

'''
sources:
https://archive.ics.uci.edu/ml/datasets/Poker+Hand
https://raw.githubusercontent.com/goldsmith/poker-hand-ml/master/data/test.csv
https://github.com/BrenoCPimenta/Poker-preflop-hand-rank-scraping-to-csv/blob/master/preflopCrawler.ipynb
'''

hands = pd.read_csv('hands.csv')
games = pd.read_csv('games.csv')
codes = json.load(open('codes.json','r'))

games = games.drop('id',axis=1)
for idx_h,hand in hands[1:3].iterrows():
  games['hand_card_1'] = hand['h1']
  games['hand_card_2'] = hand['h2']
  games['result'] = pd.NA
  for idx_g, game in games.iterrows():
    hand_suits = list(hand[['s1','s2']].values.tolist())
    hand_cards = list(hand[['h1','h2']].values.tolist())
    flop_suits = list(game[['s1','s2','s3']].values.tolist())
    flop_cards = list(game[['c1','c2','c3']].values.tolist())
    
    cards = hand_cards + flop_cards
    suits = hand_suits + flop_suits
    
    games['result'].iloc[idx_g] = result(cards,suits)
  games = games.drop(['s4','c4','s5','c5'],axis=1).to_csv('second_try.csv',index=False)
  quit()
      