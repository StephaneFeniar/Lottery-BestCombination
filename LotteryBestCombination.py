# -*- coding: utf-8 -*-
"""
@author: Stéphane
"""

#Modules
import os
import numpy as np
import pandas as pd
import scipy.sparse
from itertools import combinations
from time import clock

#Working directory
os.chdir('C:/Users/Stéphane/Documents/Euromillions')
os.getcwd()

### 1.Data import
Draws=pd.read_csv('euromillions_results_300_draws.csv', sep=';')
print(Draws.head(5))

### 2.Data Munging

Grid=range(1,51,1)
Combinations = array(list(combinations(Grid, 5)), dtype=np.int8)

# Compute for each draw, the number of tickets for each number of matches
Draws['NB_TICKETS_5_MATCHES'] = Draws['RANK1'] + Draws['RANK2'] + Draws['RANK3']
Draws['NB_TICKETS_4_MATCHES'] = Draws['RANK4'] + Draws['RANK5'] + Draws['RANK6']
Draws['NB_TICKETS_3_MATCHES'] = Draws['RANK7'] + Draws['RANK9'] + Draws['RANK10']
Draws['NB_TICKETS_2_MATCHES'] = Draws['RANK8'] + Draws['RANK12'] + 2 * Draws['RANK12']
Draws['NB_TICKETS_1_MATCH'] = Draws['RANK11'] + 18 * Draws['RANK11'] + 36 * Draws['RANK11']
Draws['NB_TICKETS_0_MATCH'] = Draws['NB_TICKETS'] - Draws['NB_TICKETS_5_MATCHES'] - Draws['NB_TICKETS_4_MATCHES'] - Draws['NB_TICKETS_3_MATCHES'] -Draws['NB_TICKETS_2_MATCHES'] - Draws['NB_TICKETS_1_MATCH']


# Replace the numbers by frequencies in order to have comparable draws.
Draws['FREQ_TICKETS_5_MATCHES'] = Draws['NB_TICKETS_5_MATCHES'] / Draws['NB_TICKETS']
Draws['FREQ_TICKETS_4_MATCHES'] = Draws['NB_TICKETS_4_MATCHES'] / Draws['NB_TICKETS']
Draws['FREQ_TICKETS_3_MATCHES'] = Draws['NB_TICKETS_3_MATCHES'] / Draws['NB_TICKETS']
Draws['FREQ_TICKETS_2_MATCHES'] = Draws['NB_TICKETS_2_MATCHES'] / Draws['NB_TICKETS']
Draws['FREQ_TICKETS_1_MATCH'] = Draws['NB_TICKETS_1_MATCH'] / Draws['NB_TICKETS']
Draws['FREQ_TICKETS_0_MATCH'] = Draws['NB_TICKETS_0_MATCH'] / Draws['NB_TICKETS']

### 3. Compute the number of matches between each Draw and each Combination

DrawsNumbers = array(Draws[['N1', 'N2', 'N3', 'N4', 'N5']], dtype=int8)

nb_draws = DrawsNumbers.shape[0]
nb_combinations = Combinations.shape[0]

DrawsNumbersSparse = np.zeros([nb_draws, 50 ], dtype=int8)
DrawsNumbersSparse[np.arange(nb_draws)[:,newaxis],DrawsNumbers-1] = 1

print("Example of transformation:")
print("Original Version:", DrawsNumbers[0])
print("Sparse Version:", DrawsNumbersSparse[0])

CombinationsSparse = np.zeros([nb_combinations, 50 ], dtype=int8)
CombinationsSparse[np.arange(nb_combinations)[:,newaxis],Combinations-1] = 1

Matches = dot(CombinationsSparse, DrawsNumbersSparse.T )
del CombinationsSparse

### 4. Estimations of the playing frequency of each combination

# Divide the frequency of tickets with m matches by the number combinations having m matches (= \binom{45}{5-m} \times \binom{m}{5})
Draws['FREQ_COMB_0'] = Draws['FREQ_TICKETS_0_MATCH'] / 1221759
Draws['FREQ_COMB_1'] = Draws['FREQ_TICKETS_1_MATCH'] / 744975
Draws['FREQ_COMB_2'] = Draws['FREQ_TICKETS_2_MATCHES'] / 141900
Draws['FREQ_COMB_3'] = Draws['FREQ_TICKETS_3_MATCHES'] / 9900
Draws['FREQ_COMB_4'] = Draws['FREQ_TICKETS_4_MATCHES'] / 225
Draws['FREQ_COMB_5'] = Draws['FREQ_TICKETS_5_MATCHES'] / 1

DrawsCombFrequency = array(Draws[['FREQ_COMB_0',
                                  'FREQ_COMB_1', 
                                  'FREQ_COMB_2', 
                                  'FREQ_COMB_3', 
                                  'FREQ_COMB_4',
                                  'FREQ_COMB_5']])


def ComputePlayingFrequency(DrawsCombFrequency, Matches):
    """Compute for each draw, the estimated playing frequency of each combination based on
    the number of matches and the associated DrawCombFrequency
    """
    PlayingFrequency = np.zeros([Matches.shape[0], Matches.shape[1]])
    for i in range(0, Matches.shape[1]):
        PlayingFrequency[:,i]=DrawsCombFrequency[i, Matches[:,i]]
    return PlayingFrequency

PlayingFrequency = ComputePlayingFrequency(DrawsCombFrequency, Matches)

### 5. Aggregation of the estimations

AggregatedPlayingFrequency = np.mean(PlayingFrequency, axis=1)

### 6. Results analysis

print('Less played combination', Combinations [ argmin(AggregatedPlayingFrequency),], '- Frequency:', min(AggregatedPlayingFrequency))
print('Most played combination', Combinations [ argmax(AggregatedPlayingFrequency),], '- Frequency:', max(AggregatedPlayingFrequency))
print('Ratio:', min(AggregatedPlayingFrequency)/max(AggregatedPlayingFrequency))

less_played_combination_estimations = PlayingFrequency[argmin(AggregatedPlayingFrequency),]
most_played_combination_estimations = PlayingFrequency[argmax(AggregatedPlayingFrequency),]
extreme_combinations_estimations = np.column_stack((less_played_combination_estimations, most_played_combination_estimations))

# Boxplot
figure()
title('Distribution of the estimated played frequency for the less & most played combination')
boxplot(extreme_combinations_estimations, 0, 'rs', 0)
yticks([1, 2], ['Less Played Combination', 'Most Played Combination'])
