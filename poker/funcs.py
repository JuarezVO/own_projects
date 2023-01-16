import pandas as pd, json
from collections import Counter

# hands = pd.read_csv('hands.csv')
# games = pd.read_csv('games.csv',index_col='id')
# codes = json.load(open('codes.json','r'))

def create_hands():
  '''Creates all possible pre-flop hands'''
  
  idx = 0
  out = {}
  nh = 1
  for h1 in range(1,14):
    for h2 in range(nh,14):
      ns = 1
      for s1 in range(1,5):
        for s2 in range(ns,5):
          if h1 == h2 and s1 == s2:
            continue
          else:
            suite = 's' if s1 == s2 else 'o'
            out[idx] = {'h1':h1,'h2':h2,'s1':s1,'s2':s2,'suite':suite}
            idx+=1
        ns+=1
    nh+=1
  out = pd.DataFrame.from_dict(out,orient='index')
  out.to_csv('hands.csv',index=False)

def checks_sequences(cards: list):
  '''
  Checks if there is any kind of sequence. It doesn't matter if it is suited or not.

  Inputs:
  :param list cards: list of cards to check for sequence.

  Returns:
  sequence: bool, if a sequence was found;
  sequence_start: int, card value corresponding to the beggining of the sequence;
  sequence_end: int, card value corresponding to the end of the sequence.
  '''

  work_cards = sorted(cards)
  if work_cards[-1] == 13 and work_cards[0] == 1 and work_cards[-2] == 12 and work_cards[-3] == 11:
    work_cards[0] = 14 
  else:
    work_cards[0]
  work_cards = sorted(work_cards)

  n_sequence = 0
  sequence_list = [work_cards[idx+1] - i == 1 for idx,i in enumerate(work_cards[:-1])]
  for idx_seq,seq in enumerate(sequence_list):
    if seq:
      n_sequence+=1
      if n_sequence >= 4:
        sequence = True 
        sequence_end = work_cards[idx_seq+1]
        sequence_start = work_cards[idx_seq-3]
      # else:
      #   sequence = False
      #   sequence_start = None
      #   sequence_end = None
    else: 
      n_sequence = 0
      sequence = False
      sequence_start = None
      sequence_end = None
  
  return sequence, sequence_start, sequence_end

def find_index(value,sequence):
  last_index = -1
  indexes = []
  while True:
    try:
      last_index = sequence.index(value, last_index + 1)
      indexes.append(last_index)
    except ValueError:
      break
  return indexes

def result(cards, suits):
  cards_count = Counter(cards)
    
  high = []
  pair = []
  trip = []
  quad = []

  # counts pair, three or four of a kind
  for crd, count in cards_count.items():
    if count == 1:
      high.append(crd)
    elif count == 2:
      pair.append(crd)
    elif count == 3:
      trip.append(crd)
    elif count == 4:
      quad.append(crd)

  # checks for sequences and the suits
  flush = max([i[1] for i in Counter(suits).items()])
  flush_suit = [i[0] for i in Counter(suits).items() if i[1] == flush][0]
  sequence, sequence_start, sequence_end = checks_sequences(cards)
  if sequence:
    sequence_idx = [find_index(i,cards)  for i in range(sequence_start,sequence_end+1)]
    sequence_suits = [suits[j] for i in sequence_idx for j in i]
    flush = max([i[1] for i in Counter(sequence_suits).items()])
    flush_suit = [i[0] for i in Counter(sequence_suits).items() if i[1] == flush][0]

  # DEFINES THE RESULT
  result_key = []

  # checks for straights and flushes
  if sequence_start == 10 and sequence_end == 14 and flush >= 5:
    result = f'royal_straight_flush: {sequence_start} to {sequence_end} of {flush_suit}'
    result_key.append(9)
  elif sequence and sequence_end < 14 and flush >=5:
    result = f'straight_flush: {sequence_start} to {sequence_end} of {flush_suit}'
    result_key.append(8)
  elif sequence and flush < 5:
    result = f'straight: {sequence_start} to {sequence_end}'
    result_key.append(4)
  elif not sequence and flush >= 5:
    result = f'flush: of {flush_suit}'
    result_key.append(5)

  # check for pairs and two_pairs
  elif pair and not trip and not quad:
    if len(pair) == 1:
      result = f'pair: pair of {pair[0]}'
      result_key.append(1)
    elif len(pair) == 2:
      result = f'two_pairs: pairs of {pair[0]} and {pair[1]}'
      result_key.append(2)
    elif len(pair) >= 3:
      pair1 = pair[0] if pair[0] == 1 else pair[-2]
      pair2 = pair[-1]
      result = f'two_pairs: pairs of {pair1} and {pair2}'
      result_key.append(2)

  # check for full house
  elif pair and trip and not quad:
    trip1 = trip[0] if trip[0] == 1 else trip[-1] 
    pair1 = pair[0] if pair[0] == 1 else pair[-1] 
    result = f'full_house: pair of {pair1} and three of {trip1}'
    result_key.append(6)
  
  #check for four of a kind
  elif quad:
    result = f'four_kind: four of {quad[0]}'
    result_key.append(7)
  
  #check for three of a kind
  elif trip and not pair and not quad:
    trip1 = trip[0] if trip[0] == 1 else trip[-1]
    result = f'three_kind: three of {trip1}'
    result_key.append(3)

  else:
    work_cards = sorted(cards)
    work_cards[0] = 14 if work_cards[0] == 1 else work_cards[0]
    high = max(work_cards)
    result = f'high_card: {high}'
    result_key.append(0)

  return max(result_key)
  
