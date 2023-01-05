import pandas as pd, numpy as np, matplotlib.pyplot as plt

games = pd.read_csv('first_try.csv')

high = round(len(games[games['result'] == 0])/len(games) * 100,2)
pair = round(len(games[games['result'] == 1])/len(games) * 100,2)
tpair = round(len(games[games['result'] == 2])/len(games) * 100,2)
three = round(len(games[games['result'] == 3])/len(games) * 100,2)
straight = round(len(games[games['result'] == 4])/len(games) * 100,2)
flush = round(len(games[games['result'] == 5])/len(games) * 100,2)
full = round(len(games[games['result'] == 6])/len(games) * 100,2)
four = round(len(games[games['result'] == 7])/len(games) * 100,2)
sflush = round(len(games[games['result'] == 8])/len(games) * 100,2)
rsflush = round(len(games[games['result'] == 9])/len(games) * 100,2)


print(f'High: {high}')
print(f'Pair: {pair}')
print(f'two pairs: {tpair}')
print(f'Three of a kind: {three}')
print(f'Straight: {straight}')
print(f'Flush: {flush}')
print(f'full house: {full}')
print(f'Four of a kind: {four}')
print(f'Straight flush: {sflush}')
print(f'Royal straight flush: {rsflush}')