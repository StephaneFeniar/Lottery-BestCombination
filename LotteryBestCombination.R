### Data import
setwd('C:/Users/Stéphane/Documents/Euromillions')
Draws = read.table("euromillions_results_300_draws.csv", header=TRUE,sep = ";")
# Draws = Draws[1:100,] /!\ If less than 8 GB of memory, keep just 100 draws.

### Data Preparation
Grid= c(1:50)
Combinations = t(combn(Grid,5)) # 2 118 760 combinations based on the 5 numbers from 1 to 50.

# Compute for each draw, the number of tickets for each number of matches
Draws$NB_TICKETS_5_MATCHES = Draws$RANK1 + Draws$RANK2 + Draws$RANK3
Draws$NB_TICKETS_4_MATCHES = Draws$RANK4 + Draws$RANK5 + Draws$RANK6
Draws$NB_TICKETS_3_MATCHES = Draws$RANK7 + Draws$RANK9 + Draws$RANK10
Draws$NB_TICKETS_2_MATCHES = Draws$RANK8 + Draws$RANK12 + 2 * Draws$RANK12
Draws$NB_TICKETS_1_MATCH = Draws$RANK11 + 18 * Draws$RANK11 + 36 * Draws$RANK11
Draws$NB_TICKETS_0_MATCH = Draws$NB_TICKETS - Draws$NB_TICKETS_5_MATCHES - Draws$NB_TICKETS_4_MATCHES - 
  Draws$NB_TICKETS_3_MATCHES-Draws$NB_TICKETS_2_MATCHES-Draws$NB_TICKETS_1_MATCH

# Replace the numbers by frequencies in order to have comparable draws.
Draws$FREQ_TICKETS_5_MATCHES = Draws$NB_TICKETS_5_MATCHES / Draws$NB_TICKETS
Draws$FREQ_TICKETS_4_MATCHES = Draws$NB_TICKETS_4_MATCHES / Draws$NB_TICKETS
Draws$FREQ_TICKETS_3_MATCHES = Draws$NB_TICKETS_3_MATCHES / Draws$NB_TICKETS
Draws$FREQ_TICKETS_2_MATCHES = Draws$NB_TICKETS_2_MATCHES / Draws$NB_TICKETS
Draws$FREQ_TICKETS_1_MATCH = Draws$NB_TICKETS_1_MATCH / Draws$NB_TICKETS
Draws$FREQ_TICKETS_0_MATCH = Draws$NB_TICKETS_0_MATCH / Draws$NB_TICKETS

### Compute the number of matches between each Draw and each Combination.

DrawsNumbers = as.matrix( Draws[,c('N1', 'N2', 'N3', 'N4', 'N5')] )
NbDraws = nrow(DrawsNumbers)
NbCombinations = nrow(Combinations)

DrawsNumbersSparse = matrix(0, nrow=NbDraws, ncol=50)
for(i in 1:NbDraws) {DrawsNumbersSparse[i,DrawsNumbers[i,]] = 1}


CombinationsSparse = matrix(0, nrow=NbCombinations, ncol=50)
for(i in 1:NbCombinations) {CombinationsSparse[i,Combinations [i,]] = 1}

Matches = CombinationsSparse %*% t(DrawsNumbersSparse)
rm(CombinationsSparse)

### Estimations of the playing frequency of each combination

#Divide the frequency of tickets with m matches by the number combinations having m matches
Draws$FREQ_COMB_0 = Draws$FREQ_TICKETS_0_MATCH / 1221759 
Draws$FREQ_COMB_1 = Draws$FREQ_TICKETS_1_MATCH / 744975 
Draws$FREQ_COMB_2 = Draws$FREQ_TICKETS_2_MATCHES / 141900
Draws$FREQ_COMB_3 = Draws$FREQ_TICKETS_3_MATCHES / 9900
Draws$FREQ_COMB_4 = Draws$FREQ_TICKETS_4_MATCHES / 225
Draws$FREQ_COMB_5 = Draws$FREQ_TICKETS_5_MATCHES / 1


DrawsCombFrequency  = as.matrix( Draws[,c('FREQ_COMB_0',
                                          'FREQ_COMB_1', 
                                          'FREQ_COMB_2', 
                                          'FREQ_COMB_3', 
                                          'FREQ_COMB_4',
                                          'FREQ_COMB_5')] )

ComputePlayingFrequency = function(DrawsCombFrequency, Matches){ 
  PlayingFrequency = matrix(nrow=nrow(Matches), ncol=ncol(Matches)) 
  for(t in 1:ncol(Matches)) { PlayingFrequency[,t] = DrawsCombFrequency[t,Matches[,t]+1] } 
  return(PlayingFrequency)
}

PlayingFrequency = ComputePlayingFrequency (DrawsCombFrequency, Matches)

### Aggregation of the estimations

PlayingFrequencyAggregated = rowMeans(PlayingFrequency)

# Most frequently played combination (Don't play it :o )
Combinations[order(-PlayingFrequencyAggregated)[1],]

# Less frequently played combination (Play this one instead :) )
Combinations[order(PlayingFrequencyAggregated)[1],]
