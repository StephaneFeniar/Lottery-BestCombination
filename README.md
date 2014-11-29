How to choose your lottery numbers ? 
========================================================
![Imgur](http://i.imgur.com/TaNSZee.png)

## Goal 

If you play at the lottery the same numbers as many others players, you will have to split the prize in case of winning.

The goal of this analysis is to reduce this risk by playing the less played combination.

## How ?

The idea is to analyze the results of the past draws : numbers drawn and proportion of winners 

Indeed each result gives us a tiny clue of how players played.

Basically, if there was more winners than usual when the draw was 1-12-14-22-32, we can deduce this combination is often played and we should not play it.

## Context

This analysis has been inspired by [Using ML To Pick Your Lottery Numbers](http://nbviewer.ipython.org/url/www.onewinner.me/en/devoxxML.ipynb) of [C.Bourguignat](https://twitter.com/chris_bour)

========================================================

The goal is the same *(reduce the probability to share the winnings)* but the approach is different.

## Illustrative example

Let's imagine a fake lottery, the **Lototo**:

* 2 numbers to pick among 5 numbers *(from 1 to 5)*.
* 10 possibles combinations : [1-2] [1-3] [1-4] [1-5] [2-3] [2-4] [2-5] [3-4] [3-5] [4-5]

The Lototo organizer know for each combination the frequency of tickets played on it *(played frequency)*:

| 1st Number| 2nd Number| Playing frequency|
|----------:|----------:|-------------------:|
|          1|          2|                0.20|
|          1|          3|                0.15|
|          1|          4|                0.15|
|          1|          5|                0.05|
|          2|          3|                0.15|
|          2|          4|                0.10|
|          2|          5|                0.05|
|          3|          4|                0.05|
|          3|          5|                0.05|
|          4|          5|                0.05|

Some of the 10 combinations are more played than others, because people are not creative:
* Combination [1-2] is the most played *(20% of the tickets)*
* Combinations [2-5] [3-4] [3-5] and [4-5] are the less played *(5% of the tickets)*

If we want to reduce the risk of sharing the winnings, we should played: [2-5], [3-4], [3-5] or [4-5] 

### Estimation of the playing frequency of each combination

**Problem** : these playing frequencies are hidden by the Lototo organizer.

So we should not be able to know which combination is the best one to play.
This is why we're gonna try to estimate these playing frequencies by studying the **public results of the past draws:**

For each draw we have:
*  A draw Id
*  The 2 winning numbers : 1st Number & 2nd Number *(in an ascending order)*
*  The proportion of tickets with 0, 1, and 2 matches

| Draw Id| 1st Number| 2nd Number|  0 match|  1 match|  2 matches|
|------:|----------:|----------:|--------------------------:|--------------------------:|---------------------------------:|
|      1|          1|          4|                       0.25|                       0.60|                              0.15|
|      2|          4|          5|                       0.50|                       0.45|                              0.05|
|      3|          1|          2|                       0.15|                       0.65|                              0.20|


#### Estimation by studying one draw result

For instance let's study the **1st draw**:

| Draw Id| 1st Number| 2nd Number|  0 match| 1 match| 2 matches|
|------:|----------:|----------:|--------------------------:|--------------------------:|---------------------------------:|
|      1|          1|          4|                       0.25|                       0.60|                              0.15|

* 15% of the tickets had 2 matches and [1-4] is the only combination with 2 matches.
<br/>So [1-4] has been played by 15% of the tickets.

* 60% of the tickets had 1 match and 6 combinations had 1 match : [1-2]  [1-3]  [1-5]  [2-4]  [3-4]  [4-5]. 
<br/>So we assume each of them have been played by 10% of the tickets.
  
* 25% of the tickets had no match and 3 combinations had 0 match : [2-3] [2-5] [3-5].
<br/>So we assume each of them have been played by 8.33% of the tickets.

The analysis of the 1st draw result allowed us to have a estimation of the playing frequency of each combination.  

**Let's compare:**
* The real playing frequency *(which is not supposed to be known)*
* Our estimation done by studying the public results of the first draw
* A naive estimation which attibutes an equal frequency of 10% for each combination

| 1st Number| 2nd Number| Real Playing Frequency| Est. using 1st Draw Result| Naive Estimation|
|---------:|----------:|----------------------:|--------------------------:|----------------:|
|         1|          2|                     20|                      10.00|               10|
|         1|          3|                     15|                      10.00|               10|
|         1|          4|                     15|                      15.00|               10|
|         1|          5|                      5|                      10.00|               10|
|         2|          3|                     15|                       8.33|               10|
|         2|          4|                     10|                      10.00|               10|
|         2|          5|                      5|                       8.33|               10|
|         3|          4|                      5|                      10.00|               10|
|         3|          5|                      5|                      10.00|               10|
|         4|          5|                      5|                       8.33|               10|

We can see our estimator is more accurate than the naive one : 
* A better or similar accuracy for 9 combinations out of 10
* An Mean Absolute Error of 4,3 vs 5.0


#### Estimation by studying all draws result

If we do the same with the results of the 3 past draws we obtain these 3 estimators:

| 1st Number| 2nd Number| Real Frequency| Est. using 1st Draw Result| Est. using 2nd Draw Result| Est. using 3rd Draw Result|
|----------:|----------:|--------------:|--------------------------:|--------------------------:|--------------------------:|
|          1|          2|           0.20|                       0.10|                       0.17|                       0.20|
|          1|          3|           0.15|                       0.10|                       0.17|                       0.11|
|          1|          4|           0.15|                       0.15|                       0.08|                       0.11|
|          1|          5|           0.05|                       0.10|                       0.08|                       0.11|
|          2|          3|           0.15|                       0.08|                       0.17|                       0.08|
|          2|          4|           0.10|                       0.10|                       0.08|                       0.11|
|          2|          5|           0.05|                       0.08|                       0.08|                       0.11|
|          3|          4|           0.05|                       0.10|                       0.08|                       0.11|
|          3|          5|           0.05|                       0.08|                       0.08|                       0.05|
|          4|          5|           0.05|                       0.10|                       0.05|                       0.05|

**Let's aggregate these 3 estimators into a single stronger estimator** like a RandomForest aggregate several decision trees.

There is a several way to aggregate these 3 estimators *([See Next-Steps](https://github.com/StephaneFeniar/Lottery-BestCombination/blob/master/README.md#next-steps))*  but here we will simply aggregate them by a simple mean.

| 1st Number| 2nd Number| Real Frequency| Aggregated Est.|
|----------:|----------:|--------------:|---------------:|
|          1|          2|           0.20|            0.16|
|          1|          3|           0.15|            0.13|
|          1|          4|           0.15|            0.11|
|          1|          5|           0.05|            0.10|
|          2|          3|           0.15|            0.11|
|          2|          4|           0.10|            0.10|
|          2|          5|           0.05|            0.09|
|          3|          4|           0.05|            0.10|
|          3|          5|           0.05|            0.07|
|          4|          5|           0.05|            0.07|

We can see our new estimator using all the past draws results is even more accurate than the estimator using only the first draw result: 

* A better accuracy for 8 combinations out of 10 
* An Mean Absolute Error of 2.9 vs 4.3
* The estimator recommends 2 good combinations: [3-5] [4-5] which have a low playing frequency.

Now you're familliar by the approach let's apply it to a real lottery : [EuroMillions](http://en.wikipedia.org/wiki/EuroMillions)

## Application to a real lottery: EuroMillions
![Let's pick the best numbers](http://i.imgur.com/bIOUoRB.png)

### Scope of the analysis
Unlike the Lototo, the Euromillions consist of picking 5 numbers among 50 + 2 stars among 10 stars.

In order to keep this analysis comparable to the Using ML analysis, we will **focus on the 5 numbers only**.

Based on this 5 numbers among 50,  we will have to estimate the playing frequency of 2 118 760 combinations 

### Results Summary
According to the estimation:

* The **most played** combination is : [7-8-9-10-11] *Don't play it :o*
* The **less played** combination is : [1-2-3-4-5] *Play this one instead :)*

**The code of this analysis is available in two languages :**

*  Python : Script and Markdown
*  R : Script and Mardown

## Next Steps

*[This section in under cunstruction]*

![We need to go deeper](https://xen-orchestra.com/blog/content/images/2014/Aug/1386271588578.jpg)

*  Test the results significancy.

*  Improve the way to aggregate the estimations. 
<br/>Exemple: if a combination has 5 matches with a draw, we should only keep the estimation associated to this draw.

*  Perform the analysis in a recursive way:
  1. Do the analysis like we did and recover an estimated  playing frequency for each combination.
  2. Re-do the analysis by using this distribution instead of an equal distribution for improving the way to "split the frequency of tickets with m matches to all the combinations having m matches" 


