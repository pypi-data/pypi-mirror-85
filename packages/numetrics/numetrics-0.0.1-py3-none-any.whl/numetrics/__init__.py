import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import statistics


def diagnose(preds_df, TARGET_NAME='target',PREDICTION_NAME='prediction'):

  eras = preds_df.era.unique()

  val1_eras = ['era121','era122','era123','era124','era125','era126','era127','era128','era129','era130','era131','era132']
  val2_eras = ['era197','era198','era199','era200','era201','era202','era203','era204','era205','era206']

  

  num_eras = len(eras)
  num_val1_eras = len(val1_eras)
  num_val2_eras = len(val2_eras)


  num_losses = 0
  num_val1_losses = 0
  num_val2_losses = 0


  num_wins = 0
  num_val1_wins = 0
  num_val2_wins = 0


  profit = 0
  val1_profit = 0
  val2_profit = 0

  loss = 0
  val1_loss = 0
  val2_loss = 0



  eras_corr = []
  val1_eras_corr = []
  val2_eras_corr = []


  eras_less_001 = []
  val1_eras_less_001 = []
  val2_eras_less_001 = []


  num_less_001 = 0
  num_val1_less_001 = 0
  num_val2_less_001 = 0


  # calculate spearman's correlation
  coef, p = spearmanr(preds_df[TARGET_NAME], preds_df[PREDICTION_NAME])
  
  #-------------------------------------------------
  for era in eras:

    data_era = preds_df.loc[preds_df['era'] == era]
    y = data_era[TARGET_NAME]
    new_preds = data_era[PREDICTION_NAME]

    corr_score, p = spearmanr(y,new_preds)

    eras_corr.append(corr_score)
    
    if (corr_score > 0):
      num_wins = num_wins + 1
      profit = profit + corr_score
    else:
      num_losses = num_losses + 1
      loss = loss + corr_score

    if (corr_score < 0.01):
      num_less_001 = num_less_001 + 1
      eras_less_001.append([era,corr_score])
  #-------------------------------------------------


  data = {'Era': eras, 'Score': eras_corr}
  eras_data_df = pd.DataFrame (data, columns = ['Era','Score'])



  print()
  print()
  print()
  print('======================= Metrics For All Eras ============================')
  print('Mean:                            ', round(statistics.mean(eras_corr), 4))
  print('std:                             ', round(statistics.stdev(eras_corr), 4))
  print('Sharpe :                         ', round(statistics.mean(eras_corr)/statistics.pstdev(eras_corr), 4))
  print()
  print('Number of All Eras:              ', num_eras, ' eras')
  print('Number of Wins:                  ', num_wins, ' eras')
  print('Number of Losses:                ', num_losses, ' eras')
  print()
  print('Win Rate:                        ', round(((num_wins/num_eras)*100), 1),'%')
  print('Loss Rate:                       ', round(((num_losses/num_eras)*100), 1),'%')
  print()
  print('Total Profit:                    ', round(profit,3))
  print('Total Loss:                      ', round(loss,3))
  print()
  print('Number of Eras less than 0.01:   ', num_less_001)
  print('=====================================================================')
  print()
  print()
  print()





  #-------------------------------------------------
  for era in val1_eras:
    
    era_data = eras_data_df.loc[eras_data_df['Era'] == era]
    era_corr_score = era_data.iloc[0]['Score']
    val1_eras_corr.append(era_corr_score)

    if (era_corr_score > 0):
      num_val1_wins = num_val1_wins + 1
      val1_profit = val1_profit + era_corr_score
    else:
      num_val1_losses = num_val1_losses + 1
      val1_loss = val1_loss + era_corr_score

    if (era_corr_score < 0.01):
      num_val1_less_001 = num_val1_less_001 + 1
      val1_eras_less_001.append([era,era_corr_score])
  #-------------------------------------------------


  print()
  print()
  print()
  print('======================= Metrics For Val 1 Eras ============================')
  print('Mean:                            ', round(statistics.mean(val1_eras_corr), 4))
  print('std:                             ', round(statistics.stdev(val1_eras_corr), 4))
  print('Sharpe :                         ', round(statistics.mean(val1_eras_corr)/statistics.pstdev(val1_eras_corr), 4))
  print()
  print('Number of All Eras:              ', num_val1_eras, ' eras')
  print('Number of Wins:                  ', num_val1_wins, ' eras')
  print('Number of Losses:                ', num_val1_losses, ' eras')
  print()
  print('Win Rate:                        ', round(((num_val1_wins/num_val1_eras)*100), 1),'%')
  print('Loss Rate:                       ', round(((num_val1_losses/num_val1_eras)*100), 1),'%')
  print()
  print('Total Profit:                    ', round(val1_profit,3))
  print('Total Loss:                      ', round(val1_loss,3))
  print()
  print('Number of Eras less than 0.01:   ', num_val1_less_001)
  print('=====================================================================')
  print()
  print()
  print()


  #-------------------------------------------------

  for era in val2_eras:

    era_data = eras_data_df.loc[eras_data_df['Era'] == era]
    era_corr_score = era_data.iloc[0]['Score']
    val2_eras_corr.append(era_corr_score)

    if (era_corr_score > 0):
      num_val2_wins = num_val2_wins + 1
      val2_profit = val2_profit + era_corr_score
    else:
      num_val2_losses = num_val2_losses + 1
      val2_loss = val2_loss + era_corr_score

    if (era_corr_score < 0.01):
      num_val2_less_001 = num_val2_less_001 + 1
      val2_eras_less_001.append([era,era_corr_score])
  #-------------------------------------------------


  print()
  print()
  print()
  print('======================= Metrics For Val 2 Eras ============================')
  print('Mean:                            ', round(statistics.mean(val2_eras_corr), 4))
  print('std:                             ', round(statistics.stdev(val2_eras_corr), 4))
  print('Sharpe :                         ', round(statistics.mean(val2_eras_corr)/statistics.pstdev(val2_eras_corr), 4))
  print()
  print('Number of All Eras:              ', num_val2_eras, ' eras')
  print('Number of Wins:                  ', num_val2_wins, ' eras')
  print('Number of Losses:                ', num_val2_losses, ' eras')
  print()
  print('Win Rate:                        ', round(((num_val2_wins/num_val2_eras)*100), 1),'%')
  print('Loss Rate:                       ', round(((num_val2_losses/num_val2_eras)*100), 1),'%')
  print()
  print('Total Profit:                    ', round(val2_profit,3))
  print('Total Loss:                      ', round(val2_loss,3))
  print()
  print('Number of Eras less than 0.01:   ', num_val2_less_001)
  print('=====================================================================')
  print()
  print()
  print()


  
  plot = eras_data_df.plot.bar(x='Era')
  plot.set_xlabel('Era')
  plot.set_ylabel('Score')
  plot.set_title('Validation')

  print(eras_data_df)
