*We'll use the methodology introduced in the LoToTo example**, *i.e*:

1.  Analyse each draw result in order to estimate the playing frequency of all combinations
2.  For each combination, we'll aggregate the 100 estimated playing frequency by into a single more accurate estimation.

### Data Preparation

#### Draws results Data

After each draw, the EuroMillions organizers communicate publicly the results. A website recover them since 2004 (745  draws) and sell them for 2 euros [here](http://www.loterieplus.com/euromillions/services/telechargement-resultat.php) 

I make available  the results of the last 100 draws here, with only the variable useful for this analysis *i.e* for each of the 100 draws:
*  N1, N2, N3 , N4, N5 : 5 numbers of the draw *(in an ascending order)*
*  Number of players on each rank:
  + Rank1:   5 matches & 2  good stars
  + Rank2:   5 matches & 1  good star
  + Rank3:   5 matches & 0  good star
  + Rank4:   4 matches & 2  good stars
  + Rank5:   4 matches & 1  good star
  + Rank6:   4 matches & 0  good star
  + Rank7:   3 matches & 2  good stars
  + Rank9:   3 matches & 1  good star
  + Rank10:  3 matches & 0  good star
  + Rank8:   2   matches & 2  good stars
  + Rank12:  2   matches & 1  good star
  + Rank11:  1  match & 2  good stars
  + Nb Tickets: number of tickets played (no matter the number of matches and/or good stars)


```r
setwd('C:/Users/sfeniar/Desktop/em')

#Data import
Draws = read.table("euromillions_sample.csv", header=TRUE,sep = ";")
head(Draws)
```

```
  DRAW_ID N1 N2 N3 N4 N5 RANK1 RANK2 RANK3 RANK4 RANK5 RANK6 RANK7 RANK8
1       1  2 14 21 36 46     0     0     7    34   615  1215  1340 20089
2       2 13 25 32 38 46     2     3    13    43   976  2515  1874 28407
3       3  1  6 13 17 26     0     6    11    98  1334  2298  3520 44519
4       4 10 13 20 33 41     0     5    10    88  1619  3041  4207 59447
5       5 10 15 17 40 45     1     2     7    37   728  1488  1552 24674
6       6  3  9 20 30 42     1     9    24   147  2617  5699  6351 88855
   RANK9 RANK10 RANK11  RANK12 NB_TICKETS
1  27820  56355 109548  411040   20418538
2  41816 102769 151524  610112   33768050
3  50062  84941 206660  624396   22520918
4  65557 122853 287234  911202   37061903
5  32263  65960 128733  504141   23174733
6 115019 242327 460652 1654248   75524187
```

Since we decided to focus on numbers and not on the stars we need to aggregate all the ranks associated to the same number of matches

**Problem:** some numbers are missing and we can't compute the number of players with 2,1 or 0 matches without them.
Hopefully we can estiamte these numbers by using the [Winning Probability](http://en.wikipedia.org/wiki/EuroMillions#Prize_structure)

* Number of players with:
  + 2   matches & 0 good star : can be estimated as twice the number of players in the Rank12 
  + 1   match & 1 good star : can be estimated as 18 times the number of players in the Rank11 *
  + 1   match & 0 good star : : can be estimated as 36 times the number of players in the Rank11 
  + 0   match (no matter the number of good star) : can be estimated as the total number of players - the number of player with at least 1 match.
  
*A better estimation mechanism could be used,  *([See Next-Steps](https://github.com/StephaneFeniar/Lottery-BestCombination/blob/master/README.md#next-steps))**


```r
#Compute for each draw, the number of tickets for each number of matches
Draws$NB_TICKETS_5_MATCHES = Draws$RANK1 + Draws$RANK2 + Draws$RANK3
Draws$NB_TICKETS_4_MATCHES = Draws$RANK4 + Draws$RANK5 + Draws$RANK6
Draws$NB_TICKETS_3_MATCHES = Draws$RANK7 + Draws$RANK9 + Draws$RANK10
Draws$NB_TICKETS_2_MATCHES = Draws$RANK8 + Draws$RANK12 + 2 * Draws$RANK12
Draws$NB_TICKETS_1_MATCH = Draws$RANK11 + 18 * Draws$RANK11 + 36 * Draws$RANK11
Draws$NB_TICKETS_0_MATCH = Draws$NB_TICKETS - Draws$NB_TICKETS_5_MATCHES - Draws$NB_TICKETS_4_MATCHES - Draws$NB_TICKETS_3_MATCHES -
                          Draws$NB_TICKETS_2_MATCHES - Draws$NB_TICKETS_1_MATCH
Draws = Draws[1:2,-(7:18)] 
head(Draws)
```

```
#Compute for each draw, the number of tickets for each number of matches
Draws$NB_TICKETS_5_MATCHES = Draws$RANK1 + Draws$RANK2 + Draws$RANK3
Draws$NB_TICKETS_4_MATCHES = Draws$RANK4 + Draws$RANK5 + Draws$RANK6
Draws$NB_TICKETS_3_MATCHES = Draws$RANK7 + Draws$RANK9 + Draws$RANK10
Draws$NB_TICKETS_2_MATCHES = Draws$RANK8 + Draws$RANK12 + 2 * Draws$RANK12
Draws$NB_TICKETS_1_MATCH = Draws$RANK11 + 18 * Draws$RANK11 + 36 * Draws$RANK11
Draws$NB_TICKETS_0_MATCH = Draws$NB_TICKETS - Draws$NB_TICKETS_5_MATCHES - Draws$NB_TICKETS_4_MATCHES - Draws$NB_TICKETS_3_MATCHES -
                          Draws$NB_TICKETS_2_MATCHES - Draws$NB_TICKETS_1_MATCH
Draws = Draws[1:2,-(7:18)] 
head(Draws)
```

```
  DRAW_ID N1 N2 N3 N4 N5 NB_TICKETS NB_TICKETS_5_MATCHES
1       1  2 14 21 36 46   20418538                    7
2       2 13 25 32 38 46   33768050                   18
  NB_TICKETS_4_MATCHES NB_TICKETS_3_MATCHES NB_TICKETS_2_MATCHES
1                 1864                85515              1253209
2                 3534               146459              1858743
  NB_TICKETS_1_MATCH NB_TICKETS_0_MATCH
1            6025140           13052803
2            8333820           23425476
```

Let's now replace the numbers by frequencies in order to have comparable draws.

```r
Draws$FREQ_TICKETS_5_MATCHES = Draws$NB_TICKETS_5_MATCHES / Draws$NB_TICKETS
Draws$FREQ_TICKETS_4_MATCHES = Draws$NB_TICKETS_4_MATCHES / Draws$NB_TICKETS
Draws$FREQ_TICKETS_3_MATCHES = Draws$NB_TICKETS_3_MATCHES / Draws$NB_TICKETS
Draws$FREQ_TICKETS_2_MATCHES = Draws$NB_TICKETS_2_MATCHES / Draws$NB_TICKETS
Draws$FREQ_TICKETS_1_MATCH = Draws$NB_TICKETS_1_MATCH / Draws$NB_TICKETS
Draws$FREQ_TICKETS_0_MATCH = Draws$NB_TICKETS_0_MATCH / Draws$NB_TICKETS
Draws = Draws[,-(7:13)] 
head(Draws)
```

```
  DRAW_ID N1 N2 N3 N4 N5 FREQ_TICKETS_5_MATCHES FREQ_TICKETS_4_MATCHES
1       1  2 14 21 36 46        0.0000003428257          0.00009128959
2       2 13 25 32 38 46        0.0000005330483          0.00010465514
  FREQ_TICKETS_3_MATCHES FREQ_TICKETS_2_MATCHES FREQ_TICKETS_1_MATCH
1            0.004188106             0.06137604            0.2950819
2            0.004337206             0.05504443            0.2467960
  FREQ_TICKETS_0_MATCH
1            0.6392624
2            0.6937172
```


### Estimation of the playing frequency of each combination

As we saw in the LoToTo example, for each draw, we will split the frequency of tickets with *m* matches to all the combinations having m matches with the draw, in order to estimate the playing frequency of each of these combinations.

No matter the draw, the number of combination with m matched numbers =
$\binom{45}{5-m} \times  \binom{m}{5}$

Then we know that for each draw there is:
* 1 combination having 5 matches 
* 225 combinations having 4  matches 
* 9 900 combinations having 3 matches 
* 141 900 combinations having 2 matches 
* 749 975 combinations having 1 match 
* 1 221 759 combinations having 0 match

So for each draw  we estimated the:
*  playing frequency of each combination with 0 match: = Frequency of tickets with 0 match / 1221759 
*  playing frequency of each combination with 1 match: = Frequency of tickets with 1 match / 749975
*  playing frequency of each combination with 2 matches: = Frequency of tickets with 2 matches / 141900
*  playing frequency of each combination with 3 matches: = Frequency of tickets with 3 matches / 9900
*  playing frequency of each combination with 4 matches: = Frequency of tickets with 4 matches / 225
*  playing frequency of each combination with 4 matches: = Frequency of tickets with 5 matches / 1



```r
Draws$FREQ_COMB_0 = Draws$FREQ_TICKETS_0_MATCH / 1221759 
Draws$FREQ_COMB_1 = Draws$FREQ_TICKETS_1_MATCH / 744975 
Draws$FREQ_COMB_2 = Draws$FREQ_TICKETS_2_MATCHES / 141900
Draws$FREQ_COMB_3 = Draws$FREQ_TICKETS_3_MATCHES / 9900
Draws$FREQ_COMB_4 = Draws$FREQ_TICKETS_4_MATCHES / 225
Draws$FREQ_COMB_5 = Draws$FREQ_TICKETS_5_MATCHES / 1

Draws = Draws[,-(7:12)] 
Draws = as.matrix(Draws)
head(Draws)
```

```
  DRAW_ID N1 N2 N3 N4 N5     FREQ_COMB_0     FREQ_COMB_1     FREQ_COMB_2
1       1  2 14 21 36 46 0.0000005232312 0.0000003960963 0.0000004325302
2       2 13 25 32 38 46 0.0000005678020 0.0000003312809 0.0000003879100
      FREQ_COMB_3     FREQ_COMB_4     FREQ_COMB_5
1 0.0000004230410 0.0000004057315 0.0000003428257
2 0.0000004381016 0.0000004651340 0.0000005330483
```


For exemple on the 1st draw, 6.14% of the tickets had 2 matches  and we know that 141 900 combinations shared 2 numbers with this draw, so we will estimate that each of these 141 900 combinations has been played by  SDFZEFDS (0.0614 /141900) of the tickets.
We just need to know which combination shared 2 numbers with this 1st draw and then we can assign them a estimated playing frequency equal to SDFZEFDS 

#### Number of Match between each draw and each combination

Before estimating the playing frequency of each combination we need to compute the number of match between each combinations and each draw.

The result is stored in a big matrix:
*  100 rows: 1 row per draw
*  2 118 760 columns : 1 column per combination 

```r
#Compare a single draw to a single combination
Comparison <- function(draw, combination) 
{ f <- function(x, y) { sum(x %in% y) }
  apply(combination, 2, f, x = draw)
}

# Compare all the draws to all the combinations, by using the previous function.
ComputeMatches = function(Draws, Combinations){
 Matches = matrix(nrow=nrow(Draws), ncol=ncol(Combinations))
  for(d in 1:nrow(Draws)) {Matches[d,] = Comparison( Draws[d,2:6], Combinations)}
  return(Matches)  
}
```


```r
Matches <- ComputeMatches(Draws, Combinations) 
Matches[1:2,1:10] # Number of matches between the first 5 draws and the first 10 combinations
```

```
     [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8] [,9] [,10]
[1,]    1    1    1    1    1    1    1    1    1     2
[2,]    0    0    0    0    0    0    0    0    1     0
```
#### Playing frequency assignment based on the number of matches

We know know for each draw:
*  how to estimate the playing frequency of a combination based on the number of matches
*  the number of matches between the draw and each combination

So we can compute for each draw, the estimated playing frequency of each combination

```r
#Compute for each draw, the estimated playing frequency of each combiation
ComputePlayingFrequency = function(Draws, Matches){
  PlayingFrequency = matrix(nrow=nrow(Matches), ncol=ncol(Matches)) 
  for(d in 1:nrow(Draws)) {
    PlayingFrequency[d,] = Draws[d,7+Matches[d,]]
  }
  return(PlayingFrequency)  
}
```

ComputeGamingProbability = function(Tirage, SharedNumbers){
  GamingProbability = matrix(nrow=nrow(SharedNumbers), ncol=ncol(SharedNumbers)) 
  for(t in 1:nrow(Tirage)) {
    GamingProbability[t,] = Tirage[t,6+SharedNumbers[t,]]
  }
  return(GamingProbability)  
}




```r
PlayingFrequency  <- ComputePlayingFrequency(Draws, Matches)
PlayingFrequency [1:2,1:3] # 2 estimations (based on the first 2 draws) of the playing frequency of the 3 first combinations 
```

```
                [,1]            [,2]            [,3]
[1,] 0.0000003960963 0.0000003960963 0.0000003960963
[2,] 0.0000005678020 0.0000005678020 0.0000005678020
```


#### Agregation of the estimations

Like we did on the LoToTo example, we can aggregate the 100 estimations into a single stronger estimations like a RandomForest aggregate several decision trees.


```r
#ProbaCombinason
PlayingFrequencyAggregated = colMeans(PlayingFrequency)
PlayingFrequencyAggregated[1:3]
```

```
[1] 0.0000004819491 0.0000004819491 0.0000004819491
```


```r
#10 Most frequently played combinations (Don't play them :o )
Combinations[,order(-PlayingFrequencyAggregated)[1:10]]
```

```
     [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8] [,9] [,10]
[1,]    1    1    1    1    1    1    1    1    1     1
[2,]    2    2    2    2    2    2    2    2    2     2
[3,]    3    3    3    3    3    3    3    3    3     3
[4,]    4    4    4    4    4    4    4    4    4     4
[5,]   14    5    6    7    8    9   10   11   12    13
```

```r
# 10 Less frequently played combinations (Play these one instead :) )
Combinations[,order(PlayingFrequencyAggregated)[1:10]]
```

```
     [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8] [,9] [,10]
[1,]    1    1    1    1    1    1    1    1    1     1
[2,]    2    2    2    2    2    2    2    2    2     2
[3,]    3    3    3    3    3    3    3    3    3     3
[4,]    4    4    4    4    4    4    4    4    4     4
[5,]   13    5    6    7    8    9   10   11   12    14
```
