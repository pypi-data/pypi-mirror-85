import pandas as pd
import numpy as np
import datetime
import random

import sklearn
import lifelines
from lifelines import AalenAdditiveFitter
from lifelines import CoxPHFitter

#from humailib.ranking_model import HumaiRankingModel

import pandas as pd
import numpy as np
import datetime
import random

import sklearn
import lifelines
from lifelines import AalenAdditiveFitter
from lifelines import CoxPHFitter

#from humailib.ranking_model import HumaiRankingModel

def predict_propensity_to_buy_fast(
    df,
    start_date,
    end_date,
    covariate_columns,
    rm,
    pred_threshold,
    dur_column='last_trans_dur_wks',
    cid_column='Customer_ID',
    batch_size = 1000,
    verbose=False
):
    n = len(df)
    propensities = []
    num_weeks = int( (end_date - start_date) / pd.to_timedelta(7, unit='D') )
    ofs = 0
    while ofs < n:
        print("{:,}/{:,} ({:.2f}%)".format(ofs, n, float(ofs)*100.0/n))

        cols = [c for c in covariate_columns if c != dur_column]
        end = min(n, ofs+batch_size)

        rows = df.iloc[ofs:end,:]
        pred_data = []
        for i in range(end-ofs):
            row = rows.iloc[i,:]
            delta = (start_date - row['last_trans_date']) / pd.to_timedelta(7, unit='D')
           
            for wk in range(num_weeks):
                pred_data.append(tuple([row[cid_column], delta+wk] + row[cols].tolist()))

        df_pred = pd.DataFrame(pred_data, columns=[cid_column,dur_column]+cols)
        rm.predict(df_pred, covariate_columns, pred_threshold=pred_threshold)
        
        for cid, df_propensities in df_pred.groupby(by=cid_column):
            
            pred_propensities = np.float128(df_propensities['pred_ranking'].to_numpy())

            if verbose:
                print("Propensities {}: {}".format(row[cid_column], pred_propensities))

            propensities.append(tuple([cid] + pred_propensities.tolist()))
            
        ofs = batch_size + ofs
    
    dates=[start_date+pd.to_timedelta(i*7, unit='D') for i in range(0, num_weeks) ]
    columns=['propensity_to_buy_{}'.format(date.strftime("%Y%m%d")) for date in dates]
    df_out = pd.DataFrame(propensities, columns=[cid_column]+columns)
    
    return df_out
        

def predict_propensity_to_buy(
    df,
    start_date,
    end_date,
    covariate_columns,
    rm,
    pred_threshold,
    dur_column='last_trans_dur_wks',
    cid_column='Customer_ID',
    verbose=False
):
    
    n = len(df)
    propensities = []
    num_weeks = int( (end_date - start_date) / pd.to_timedelta(7, unit='D') )
    for i in range(0, len(df)):
        row = df.iloc[i,:]
        #print("Customer characteristics:\n{}".format(row[compare_cols]))
        
        if i % 1000 == 0:
            print("{:,}/{:,} ({:.2f}%)".format(i, n, float(i)*100.0/n))
            
        delta = (start_date - row['last_trans_date']) / pd.to_timedelta(7, unit='D')
        #print("delta in wks: {}".format(delta))
            
        pred_data = []
        for wk in range(0, num_weeks):
            pred_data.append(row[covariate_columns])

        df_pred = pd.DataFrame(pred_data, columns=covariate_columns)
        df_pred[dur_column] = [delta+i for i in range(0,num_weeks)]
        rm.predict(df_pred, covariate_columns, pred_threshold=pred_threshold)
        #print(df_pred.head())
        
        pred_propensities = np.float128(df_pred['pred_ranking'].values)
        
        if verbose:
            print("Propensities {}: {}".format(row[cid_column], pred_propensities))
        
        propensities.append(tuple([row[cid_column]] + pred_propensities.tolist()))
    
    dates=[start_date+pd.to_timedelta(i*7, unit='D') for i in range(0, num_weeks) ]
    columns=['propensity_to_buy_{}'.format(date.strftime("%Y%m%d")) for date in dates]
    df_out = pd.DataFrame(propensities, columns=[cid_column]+columns)
    
    return df_out
        

def predict_propensity_to_buy_and_lifecycle(
    df, 
    start_date,
    end_date,
    lhood_columns, 
    prior_columns, 
    rm, 
    cph, 
    pred_threshold, 
    dur_column='last_trans_dur_wks',
    cid_column='Customer_ID', 
    delay_until_max=True, 
    verbose=False
):
    
    n = len(df)
    data = []
    prediction_week_range = int( (end_date - start_date) / pd.to_timedelta(7, unit='D') )
    
    for i in range(0, len(df)):
        row = df.iloc[i,:]
        
        if i % 1000 == 0:
            print("{:,}/{:,} ({:.2f}%)".format(i, n, float(i)*100.0/n))
            
        #if verbose:
        #    print(row)
        
        aa = np.modf((start_date - row['last_trans_date']) / pd.to_timedelta(7, unit='D'))
        weeks_to_start = int(aa[1])
        offset = aa[0]
        
        weeks = weeks_to_start + prediction_week_range
        
        ## Get PRIOR
        pred = cph.predict_survival_function(
            row[prior_columns], 
            times=[offset+wk for wk in range(0,weeks)]
        )
        
        prior = np.float128(pred.iloc[:,0].values)
        
        if verbose:
            print("Prior: {}".format(prior))
        
        ## Get LIKELIHOOD
        frame = []
        for wk in range(0, weeks):
            frame.append(row[lhood_columns])

        df_pred = pd.DataFrame(frame, columns=lhood_columns)
        #print(df_pred.head())
        df_pred[dur_column] = [offset+wk for wk in range(0,weeks)]
        #print(df_pred.head())
        rm.predict(df_pred, lhood_columns, pred_threshold=pred_threshold)
        #print(df_pred.head())
        
        lhood = np.float128(df_pred['pred_ranking'].values)
        
        if verbose:
            print("Likelihood: {}".format(lhood))
        
        m = max(lhood)
        if verbose:
            print("lhood hl {}".format([i for i,j in enumerate(lhood) if j==m]))
        if delay_until_max:
            
            idx = random.choice( [i for i,j in enumerate(lhood) if j==m] )
            if verbose:
                print("  chosen idx {}".format(idx))
            prior[:idx] = 1.0
        
        ## Calculate POSTERIOR
        posterior = lhood * prior
    
        if verbose:
            print("Posterior: {}".format(posterior))
        
        #print(df_lhood.iloc[i,:])
        
        pp = posterior
        sgn = [0]
        sgn.extend(np.sign(np.diff(pp)))

        # jb - just bought
        # nt - neutral
        # go - growing opportunity
        # hl - highest likelihood
        # dc - declining
        # ls - loss
        jb = 0
        m = max(pp[1:])
        hl = [i for i,j in enumerate(pp[1:]) if j==m]
        
        if verbose:
            print("hl {}".format(hl))

        # We want to replace any declining segments that happen before the max,
        # to be remarked as neutral.
        #sgn = [0 if (i < hl and x < 0) else x for (i,x) in zip(range(0,len(sgn)), sgn)]
        #print(sgn)

        stage = np.array(['nt'] * len(pp))
        stage = ['go' if s > 0 else m for s,m in zip(sgn,stage)]
        stage = ['dc' if s < 0 else m for s,m in zip(sgn,stage)]
        stage = ['ls' if (i > hl[-1] and i > row['death_from']) else m for s,i,m in zip(sgn,range(0,len(sgn)), stage)]
        stage[jb] = 'jb'
        for hhll in hl:
            stage[hhll] = 'hl'
        if hl == jb:
            stage[hl] = 'hl+jb'

        data.append(tuple([
            row[cid_column]] + \
            lhood.tolist()[-prediction_week_range:] + \
            stage[-prediction_week_range:] + \
            posterior.tolist()[-prediction_week_range:]
        ))
        
        #print(row[cid_column])
        #print(stage)
    
    dates=[start_date+pd.to_timedelta(i*7, unit='D') for i in range(0, prediction_week_range) ]
    columns=['propensity_to_buy_{}'.format(date.strftime("%Y%m%d")) for date in dates]
    columns.extend(['lifecycle_stage_{}'.format(date.strftime("%Y%m%d")) for date in dates])
    columns.extend(['posterior_propensity_{}'.format(date.strftime("%Y%m%d")) for date in dates])
    df_out = pd.DataFrame(data, columns=[cid_column]+columns)
        
    print("{:,}/{:,} ({:.2f}%)".format(i, n, 100))
        
    return df_out
