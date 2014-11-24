Optimize your lottery winnings by picking the right numbers
========================================================

![Let's pick the best numbers](http://i.imgur.com/bIOUoRB.png)
***

# Overview

## Goal 

The goal of this analysis is to optimize winnings of a lottery by playing the less played combination and reducing the probability to share the winnings.


## How ?

The idea is to:

1. Analyze the pasts  results of the lottery *(number of winners for each draw)*
2. Deduce the playing frequency of each combination. Basically, if there is more winner than usual when the draw is 1-2-3-4-5, we can deduce this combination has a high playing frequency.
3. Play the combination win the lower playing frequency in order to reduce the probability of sharing the winnings


## Context

This analysis has been inspired by [Using ML To Pick Your Lottery Numbers](http://nbviewer.ipython.org/url/www.onewinner.me/en/devoxxML.ipynb) of [C.Bourguignat](https://twitter.com/chris_bour)

The goal is the same *(reduce the probability to share the winnings)* but the approach is different.
A comparaison of these approaches is availabe at the end.

# Approach

## Illustrative example: the LoToTo

Let's imagine a fake lottery. the **LoToTo**:

* 2 numbers to pick among 5 numbers (1, 2, 3, 4, 5) .
* 10 combinations possibles : [1-2] [1-3] [1-4] [1-5] [2-3] [2-4] [2-5] [3-4] [3-5] [4-5]

The Lototo organizer has computed for each combination the proportion of players who played it since the launch of the Lototo:



```r
LoToTo.PlayingFrequency
```

```
      1st Number 2nd Number Players' proportion who played combination
 [1,]          1          2                                       0.20
 [2,]          1          3                                       0.15
 [3,]          1          4                                       0.15
 [4,]          1          5                                       0.05
 [5,]          2          3                                       0.15
 [6,]          2          4                                       0.10
 [7,]          2          5                                       0.05
 [8,]          3          4                                       0.05
 [9,]          3          5                                       0.05
[10,]          4          5                                       0.05
```
Some of the 10 combinations are more played than others, because people are not creative:
* Combination [1-2] is the most played *(20% of the players played this combination)*
* Combinations [2-5] [3-4] [3-5] and [4-5] are the less played *(5% of the players played each of these combination)*
