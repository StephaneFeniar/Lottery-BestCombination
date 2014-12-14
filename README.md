How to choose your lottery numbers ? 
========================================================
![Imgur](http://i.imgur.com/pgk72hG.png)

## Overview

#### Goal
If you play at the lottery the same combination as many others players, you will have to split the prize in case of winning.

The goal of this analysis is to reduce this risk by playing the less played combination.

#### How ?

The idea is to analyze the results of the past draws : numbers drawn and proportion of winners. 

Basically, each result can ben seen as a tiny clue: if there is more winners than usual when the draw is [1-12-14-22-32], we can deduce this combination and similar ones are often played.

#### Context

This analysis has been inspired by [OneWinner.me](http://www.onewinner.me/fr/faq-fr.html) and [Using ML to pick your Lottery Numbers](http://nbviewer.ipython.org/url/www.onewinner.me/en/devoxxML.ipynb) of [C.Bourguignat](https://twitter.com/chris_bour).

The goal is the same but the approach is different. Instead of using crowdsourcing, we'll analyse past draws results.

## Methodology

An introductive example explaining the methodology is available [here](https://github.com/StephaneFeniar/Lottery-BestCombination/blob/master/Methodology.md).

This lecture is highly recommended if you're not familliar with analyses about lottery numbers.

## Application to a real lottery: EuroMillions
![Let's pick the best numbers](http://i.imgur.com/bIOUoRB.png)

#### Scope of the analysis
Euromillions consist of picking 5 numbers among 50 + 2 stars among 10 stars.

We'll **focus on the numbers** for keeping the analysis comparable to [Using ML to Pick Your Numbers](http://nbviewer.ipython.org/url/www.onewinner.me/en/devoxxML.ipynb).


#### Results summary
According to the estimation:

* The **most played** combination is : [ 7 13 19 22 24] *Don't play it :o*
* The **less played** combination is : [14 20 41 45 49]  *Play this one instead :)*

The code of this analysis is available in two languages :

*  **Python** : [Script](https://github.com/StephaneFeniar/Lottery-BestCombination/blob/master/LotteryBestCombination.py) and [IPython Notebook](http://nbviewer.ipython.org/github/StephaneFeniar/Lottery-BestCombination/blob/master/LotteryBestCombination.ipynb)
*  **R** : [Script](https://github.com/StephaneFeniar/Lottery-BestCombination/blob/master/LotteryBestCombination.R) and [Markdown](https://github.com/StephaneFeniar/Lottery-BestCombination/blob/master/R%20Markdown.MD)

## Next Steps

*[ - - - This section in under construction - - - ]*

![We need to go deeper](http://i.imgur.com/e1wmjmE.png)

*  **Improve the way to aggregate the estimations.** 
<br/>Exemple: if a combination has 5 matches with a draw, we should only keep the estimation associated to this draw.

*  **Perform the analysis in a recursive way:**
  1. Do the analysis like we did and recover an estimated  playing frequency for each combination.
  2. Re-do the analysis by using this distribution instead of an equal distribution for improving the way to "split the frequency of tickets with m matches to all the combinations having m matches" 

*  **Improving the approach by optimizing the global expected winnings.**
<br/> Instead of just reduce the risk of sharing the big prize, we could reduce the risk of sharing all prizes, *i.e* searching a combination which is rarely played and doesn't shared a lots of numbers with most played combinations.




