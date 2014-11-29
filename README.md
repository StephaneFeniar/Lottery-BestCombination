How to choose your lottery numbers ? 
========================================================
![Imgur](http://i.imgur.com/TaNSZee.png)

## Goal 

If you play at the lottery the same numbers as many others players, you will have to split the prize in case of winning.

The goal of this analysis is to reduce this risk by playing the less played combination.

#### How ?

The idea is to analyze the results of the past draws : numbers drawn and proportion of winners 

Basically, if there was more winners than usual when the draw was 1-12-14-22-32, we can deduce this combination and similar ones are often played.

#### Context

This analysis has been inspired by [Using ML To Pick Your Lottery Numbers](http://nbviewer.ipython.org/url/www.onewinner.me/en/devoxxML.ipynb) of [C.Bourguignat](https://twitter.com/chris_bour)

The goal is the same *(reduce the probability to share the winnings)* but the approach is different.

## Illustrative example

An introductive example is available here. It explains the methodology by using a fake lottery.

## Application to a real lottery: EuroMillions
![Let's pick the best numbers](http://i.imgur.com/bIOUoRB.png)

#### Scope of the analysis
Euromillions consist of picking 5 numbers among 50 + 2 stars among 10 stars.

In order to keep this analysis comparable to the Using ML analysis, we'll **focus only on the 5 numbers**.

#### Results
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


