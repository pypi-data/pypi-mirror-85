import pandas as pd
import numpy as np
import plotly.express as px

from pandas.api.types import is_float_dtype, is_numeric_dtype, is_string_dtype
#from humailib.cloud_tools import GoogleBigQuery, GoogleCloudStorage


def instantiate_class(module_name, class_name):
    module = __import__(module_name, globals(), locals(), [class_name])
    class_ = getattr(module, class_name)
    
    return class_


"""
Column type definitions from the data dictionary.
    
https://humai.sharepoint.com/:w:/s/Platform/ET6ZzN-QgiJIpLdbVMkFz0oBe9_UOhSoau0Zvbo7HJ-5lQ?e=OxMlYv
"""
humai_table_field_types = {    
    'transactions' : {
        'datetime' : ['Datetime'],
        'string' : ['Transaction_ID','Branch_ID','Customer_ID','Status','Single_Item_Product_ID'],
        'float' : ['Total_Gross','Discount','Amount_Paid'],
        'int' : ['Total_Num_Items_Purchased']
    },
    'items' : {
        'datetime' : ['Datetime'],
        'string' : ['Transaction_ID','Product_ID','Name'],
        'float' : ['Total', 'Discount'],
    },
    'mailings' : {
        'datetime' : ['Send_Datetime'],
        'string' : ['Broadcast_ID','Campaign_ID'],
        'int' : ['Num_Customers']
    },
    'mailings_events' : {
        'datetime' : ['Activity_Datetime', 'Send_Datetime'],
        'string' : ['Broadcast_ID','Customer_ID','Activity','Description'],
    },
    'customers' : {
        'string' : ['Customer_ID','Email','Name','Address'],
    },
    'customer_ids' : {
        'string' : ['Customer_ID','Email','Person']
    },
    'products' : {
        'string' : ['Name','Product_ID','SKU'],
        'float' : ['Price'],
    },
    'customer_characteristics' : {
        'string' : ['Customer_ID']
    },
    'product_characteristics' : {
        'string' : ['Customer_ID','Product_ID']
    },
    'predictions' : {
        'string' : ['Customer_ID'],
        'datetime' : ['Date','date_to_email'],
        #'int' : ['Time_Of_Day']
    },
}


def convert_table_columns(
    df, 
    table_type = 'transactions', 
    datetime_format='%Y-%m-%d %H:%M:%S'
):
    
    """
    Convert table column types to table column type definitions as specified in the data dictionary:
    
    https://humai.sharepoint.com/:w:/s/Platform/ET6ZzN-QgiJIpLdbVMkFz0oBe9_UOhSoau0Zvbo7HJ-5lQ?e=OxMlYv
    """
    
    types = humai_table_field_types[table_type]
    if 'datetime' in types:
        columns_as_datetime(df, columns=types['datetime'], datetime_format=datetime_format)
    if 'string' in types:
        columns_as_str(df, columns=types['string'], uppercase=False, drop_empty=False)
    if 'float' in types:
        columns_as_float(df, columns=types['float'], na_replace_value=None, drop_na=False)
    if 'int' in types:
        columns_as_int(df, columns=types['int'], na_replace_value=None, drop_na=False)

    for c in df.columns: print("  {} -> {}".format(c, df[c].dtype))
        
        
def load_table(
    gbq, 
    dataset_table,
    table_type,
    datetime_columns = None,
    datetime_format = '%Y-%m-%d %H:%M:%S', 
    flush_cache = True,
):
    """
    Load table and convert column types
    """    
         
    print("[load_table] Loading table...")
    df = gbq.download_table_to_pandas(dataset_table, flush_cache=flush_cache)

    if df is None:
        return None
    
    print("[load_table] Converting table columns...")
    if datetime_columns is not None:
        columns_as_datetime(df, columns=datetime_columns, datetime_format=datetime_format)
    convert_table_columns(df, table_type=table_type, datetime_format=datetime_format)    
    
    return df


def load_csv(
    gcs,
    filename,
    table_type,
    datetime_columns = None,
    datetime_format='%Y-%m-%d %H:%M:%S',
    flush_cache = True
):
    """
    Load CSV from GCS and convert column types.
    """
    
    print("[load_table] Loading table...")
    df = gcs.download_csv(filename, flush_cache=flush_cache)
    
    if df is None:
        return None
    
    print("[load_table] Converting table columns...")
    if datetime_columns is not None:
        columns_as_datetime(df, columns=datetime_columns, datetime_format=datetime_format)
    convert_table_columns(df, table_type=table_type, datetime_format=datetime_format)
    
    return df


def load_and_merge_tables(
    gbq, 
    dataset,
    table_type,
    date_ranges,
    table_name = None,
    datetime_columns = None,
    datetime_format = '%Y-%m-%d %H:%M:%S', 
    flush_cache = True,
):
    """
    1. Load tables by date range. 
    2. Remove duplicate rows.
    3. Convert column types
    """    
    
    print("[load_and_merge_tables] Loading tables...")
    df = None
    for date_range in date_ranges:
        
        if table_name is not None:
            table = "{}.{}_{}".format(dataset, table_name, date_range)
        else:
            table = "{}.{}_{}".format(dataset, table_type, date_range)

        df_tmp = gbq.download_table_to_pandas(
            table,
            flush_cache=flush_cache
        )
        if df_tmp is not None:
            if df is None:
                df = df_tmp.copy()
            else:
                df = df.append(df_tmp)

    if df is None:
        return None
    
    print("[load_and_merge_tables] {:,} rows total.".format(len(df)))
    print("[load_and_merge_tables] Dropping duplicate rows...")
    df.drop_duplicates(inplace=True)
    print("[load_and_merge_tables] {:,} rows left.".format(len(df)))
    
    print("[load_and_merge_tables] Converting table columns...")
    if datetime_columns is not None:
        columns_as_datetime(df, columns=datetime_columns, datetime_format=datetime_format)
    convert_table_columns(df, table_type=table_type, datetime_format=datetime_format)
    
    return df


def merge_dataframes(dataframes, on, overwrite_cols=False):
    
    df_out = None
    for df in dataframes:
        if df_out is None:
            df_out = df
        else:
            if not overwrite_cols:
                cols_to_keep = [on] + [c for c in df.columns if c not in df_out]
                df_out = df_out.merge(
                    df[cols_to_keep],
                    on=on,
                    how='left',
                    copy=False,
                )
            else:
                df_out = df_out.merge(
                    df,
                    on=on,
                    how='left',
                    copy=False,
                )
                
    return df_out

    
def force_string(value):
    return 'S' + str(value)#'S' + str(value)


def column_stats(df, col_name, n=-1):
    """
    Print out column statistics.
    """
    
    isna = df[col_name].isna().sum()
    print("NaNs: {:,} out of {:,} ({:.2f}%)".format(isna, len(df), 100.0*isna/len(df)))
    print("== Describe ==")
    print(df[col_name].describe())
    
    if n == -1:
        n = df[col_name].nunique()
        
    if not is_float_dtype(df[col_name]):
        print("== Value counts ==")
        print(df[col_name].value_counts()[:n])
        print("\n  Total unique values: {:,}\n".format(df[col_name].nunique()))
        
    print("== Head ==")
    print(df[col_name].head(n=7))
    
    
def column_hist(df, col_name):
    
    fig = px.histogram(df, x=col_name)
    fig.update_layout(
        title="Histogram of '{}'".format(col_name),
        xaxis_title=col_name,
        yaxis_title='Number of customers'
    )
    #fig.show()
    
    return fig
    
          
def columns_as_str(df, columns, uppercase=False, drop_empty=False, replace_na_value=''):
          
    """
    Convert columns to string, and convert to uppercase if specified.

    Note: This is done inplace.
    """
    
    if columns is None:
        columns = df.columns

    if not isinstance(columns, list):
        raise Exception("Expecting columns to be a list.")
    
    for c in columns:
        if c in df:
            if uppercase:    
                df.loc[:,c] = df[c].astype(str, skipna=True).str.upper()
            else:
                df.loc[:,c] = df[c].astype(str, skipna=True)

            if drop_empty:
                df.loc[:,c].replace(to_replace='', value=np.nan, inplace=True)
                df.dropna(subset=[c], inplace=True)
            else:
                df.loc[:,c].fillna(replace_na_value, inplace=True)

        else:
            print("Column '{}' doesn't exist.".format(c))

            
def columns_as_datetime(df, columns, datetime_format='%Y-%m-%d %H:%M:%S'):
    
    """
    Convert columns to time-zone-agnostic datetime.

    Note: This is done inplace.
    """
    
    if columns is None:
        columns = df.columns

    if not isinstance(columns, list):
        raise Exception("Expecting columns to be a list.")

    for c in columns:
        if c in df:
            df.loc[:,c] = pd.to_datetime(df[c], format=datetime_format, utc=True).dt.tz_convert(None)
        else:
            print("Column '{}' doesn't exist.".format(c))


def columns_as_float(df, columns, na_replace_value=None, drop_na=True):
    
    """
    Convert columns to float.

    Note: This is done inplace.
    """
    
    if columns is None:
        columns = df.columns
        
    if not isinstance(columns, list):
        raise Exception("Expecting columns to be a list.")

    if na_replace_value is None:
        na_replace_value = np.nan
        
    for c in columns:
        if c in df and not is_float_dtype(df[c]):
            
            if is_string_dtype(df[c]):
                df.loc[:,c].replace({
                    '' : np.nan, 'nan' : np.nan, 'NaN' : np.nan, 'None' : np.nan
                }, inplace=True)
                
            if drop_na:
                df.dropna(subset=[c], how='any', inplace=True)
            else:
                df.loc[:,c].fillna(na_replace_value, inplace=True)
                
            df.loc[:,c] = df[c].astype('float64', skipna=False)
        else:
            if c not in df:
                print("Column '{}' doesn't exist.".format(c))

        

def columns_as_int(df, columns, na_replace_value=None, drop_na=True):
    
    """
    Convert string/float columns to integer.

    Note: This is done inplace.
    """
    
    if not drop_na and na_replace_value is None:
        na_replace_value = -1.0

    columns_as_float(df, columns, na_replace_value, drop_na)
    
    for c in columns:
        if c in df:
            df.loc[:,c] = df[c].astype('int64', skipna=False)
        else:
            print("Column '{}' doesn't exist.".format(c))
            
            
def agg_first(series):
    return series.iloc[0]

def agg_last(series):
    return series.iloc[-1]

def agg_nth(series, **kwargs):
    n = kwargs['n']
    if n >= len(series):
        return np.nan
    
    return series.iloc[n]

def agg_list(series):
    return "{}".format(list(series.to_numpy()))

def agg_umode(series):
    modes = series.mode()
    return modes.iloc[0]

    
def aggregate_columns(df, agg_type, agg_column, columns, copy_agg_column=False, **kwargs):
    
    """
    Aggregate values of columns, collapsing them.

    Note: This is not done inplace.
    """
    
    if agg_column not in df:
        print("[aggregate_columns] '{}' does not exist!!".format(agg_column))
        return None
    
    for c in columns:
        if c not in columns:
            print("[aggregate_columns] '{}' does not exist!!".format(c))
    
    aggregators = {
        'mean' : pd.DataFrame.mean,
        'sum'  : pd.DataFrame.sum,
        'min'  : pd.DataFrame.min,
        'max'  : pd.DataFrame.max,
        'std'  : pd.DataFrame.std,
        'mode' : agg_umode,
        'first': agg_first,
        'last' : agg_last,
        'nth'  : agg_nth,
        'list' : agg_list,
    }
    
    if agg_type in aggregators:
        func = aggregators[agg_type]
    else:
        raise NameError(f'[aggregate_columns] Need to add {agg_type} to transform function')
        
    cols = [c for c in columns if c in df]
    return df.groupby(by=agg_column)[cols].agg(func, **kwargs)


def transactions_cleanup(df, datetime_column, tid_column = 'Transaction_ID', cid_column = 'Customer_ID', datetime_format='%Y-%m-%d %H:%M:%S'):
    
    """
    Perform common transaction data cleanup.

    Note: This is done inplace.
    """
    
    df.loc[:,datetime_column] = pd.to_datetime( df[datetime_column], format=datetime_format)
    df.loc[:,datetime_column].dropna(inplace=True)

    # Get transactions date range
    print('Date range from {0} to {1}'.format(df[datetime_column].min(), df[datetime_column].max())) 
    
    # Remove column 'Unnamed: 0' if it exists
    if 'Unnamed: 0' in df:
        df.drop('Unnamed: 0', axis=1, inplace=True)
        print("Removed unnamed index column")

    print("Before dropping empty Transaction IDs: {:,}".format(len(df)))

    # Drop Transaction_ID's that are empty
    df.loc[:,tid_column].replace('', np.nan, inplace=True)
    df.dropna(subset=[tid_column], inplace=True)

    print("After: {:,}".format(len(df)))
    
    print("Before dropping empty Customer IDs: {:,}".format(len(df)))

    # Drop [cid]'s that are empty
    df.loc[:,cid_column].replace('', np.nan, inplace=True)
    df.dropna(subset=[cid_column], inplace=True)

    print("After: {:,}".format(len(df)))


def email_ensure_zero_or_one_activity_per_broadcast(
    df, cid_column = 'Customer_ID', activity_column = 'Activity', 
    activity_datetime_column = 'Activity_Datetime',
    verbose=True
):

    """
    Ensure each email sent to each customer has only one event: either a delivery, an open, a click, or a transaction,
    in that order. Keep only the first (in time) occurrence of it.

    Note: This is done inplace.
    """
    
    conv_table = {
        'DELIVERY' : 0,
        'OPEN' : 1,
        'UNSUBSCRIBE' : 2,
        'CLICK' : 3,
        'TRANSACTION' : 4
    }
    
    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] converting activities to ordinals...")
    
    df.loc[:,'activity_id'] = df[activity_column].apply(
        lambda x: conv_table.get(x,len(conv_table))
    )
 
    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] get max...")

    result = df.groupby(by=[cid_column, 'Broadcast_ID'])['activity_id'].max()
    
    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] determining which rows to keep...")
        
    df.loc[:,'keep'] = df.apply(lambda x: 1 if result[x[cid_column],x['Broadcast_ID']] == x['activity_id'] else 0, axis=1)

    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] dropping...")
    df.drop(index=df[df.keep == 0].index, inplace=True)
    
    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] sorting and keeping only the first occurence of the activity...")
        
    df.sort_values(by=[cid_column, 'Broadcast_ID', activity_datetime_column], inplace=True)
    df.drop_duplicates(subset=[cid_column, 'Broadcast_ID'], keep='first', inplace=True)

    del df['keep']
    del df['activity_id']



def email_keep_activities(df, activities):
    
    """
    Keep only certain email activities, remove the rest.

    Note: This is done inplace.
    """
    
    keep = df.Activity.isin(activities)
    df.drop(index=df[~keep].index, inplace=True)
    
    
def email_activity_stats(df, activity_column='Activity'):
    
    n = []
    n.append(len(df[df[activity_column] == 'DELIVERY']))
    n.append(len(df[df[activity_column] == 'OPEN']))
    n.append(len(df[df[activity_column] == 'CLICK']))
    n.append(len(df[df[activity_column] == 'TRANSACTION']))
    n.append(len(df[df[activity_column] == 'UNSUBSCRIBE']))
    n.append(len(df) - np.sum(n))
    N = np.sum(n)
    
    stats = {
        'Delivered' : n[0],
        'Delivered_perc' : 100.0 * n[0]/N,
        'Opens' : n[1],
        'Opens_perc' : 100.0 * n[1]/N,
        'Clicks' : n[2],
        'Clicks_perc' : 100.0 * n[2]/N,
        'Transactions' : n[3],
        'Transactions_perc' : 100.0 * n[3]/N,
        'Unsubscribes' : n[4],
        'Unsubscribes_perc' : 100.0 * n[4]/N,
        'Other' : n[5],
        'Other_perc' : 100.0 * n[5]/N,
        'Total' : np.sum(n)
    }

    return stats


def print_email_activity_stats(df, activity_column='Activity'):
    
    stats = email_activity_stats(df, activity_column=activity_column)
    
    print("Deliveries:   {:,} ({:.2f} %)".format(stats['Delivered'], stats['Delivered_perc']))
    print("Opens:        {:,} ({:.2f} %)".format(stats['Opens'], stats['Opens_perc']))
    print("Clicks:       {:,} ({:.2f} %)".format(stats['Clicks'], stats['Clicks_perc']))
    print("Transactions: {:,} ({:.2f} %)".format(stats['Transactions'], stats['Transactions_perc']))
    print("Unsubscribes: {:,} ({:.2f} %)".format(stats['Unsubscribes'], stats['Unsubscribes_perc']))
    print("Other:        {:,} ({:.2f} %)".format(stats['Other'], stats['Other_perc']))
    print("Total:        {:,}".format(stats['Total']))
    
    
def transaction_stats(
    df,
    cid_column='Customer_ID',
    datetime_column='Datetime',
    max_bins=100
):
    
    df.loc[:,'rank'] = df.sort_values(by=[cid_column, datetime_column]). \
        groupby(by=[cid_column])[datetime_column].rank(method='dense')
    #df.loc[:,'trans'] = 1
    
    n_trans = df.sort_values(by=[cid_column, datetime_column]).groupby(by=[cid_column])['rank'].max()
    #n_trans = df.sort_values(by=[cid_column, datetime_column]).groupby(by=[cid_column])['trans'].sum()

    df_n_trans = pd.DataFrame()
    df_n_trans.loc[:,cid_column] = n_trans.index
    df_n_trans.loc[:,'n_trans'] = n_trans.to_numpy()

    hist_n_trans = df_n_trans['n_trans'].value_counts()

    df_trans_hist = pd.DataFrame()
    df_trans_hist['n_trans'] = hist_n_trans.index
    df_trans_hist['count'] = hist_n_trans.values
    df_trans_hist.sort_values(by=['n_trans'], inplace=True)
    print(df_trans_hist.head(max_bins))
    
    fig = column_hist(df_n_trans, 'n_trans')
    
    del df['rank']
    
    print("Period {} to {}".format(df[datetime_column].min(), df[datetime_column].max()))
    print("Total sales: {:,} ({:,} customers)".format(len(df), df[cid_column].nunique()))
    print("Order segment 3+: {:,} customers".format(df_trans_hist[df_trans_hist['n_trans'] > 2]['count'].sum()))
    
    return fig, df_trans_hist


def keep_subset_customers(df, cid_column, k):
    import random
    
    print("{:,} unique customers".format(df[cid_column].nunique()))
    
    cids = list(df[cid_column].unique())
    to_keep_cids = random.sample(cids, k=k)
    to_keep_cids_map = {cid:1 for cid in to_keep_cids}

    df.loc[:,'keep'] = df[cid_column].apply(lambda x: to_keep_cids_map.get(x,0))
    df_keep = df.drop(index=df[df.keep == 0].index)
    
    print("{:,} unique customers after sampling".format(df_keep[cid_column].nunique()))
    
    return df_keep


def mann_whitney_test(dfA, dfB, column, group_A_name='grp_A', group_B_name='grp_B', scale = 1.0, unit='', verbose=False):
    
    from scipy.stats import mannwhitneyu as mw
    
    try:
        dfa = dfA[~dfA[column].isnull()]
        dfb = dfB[~dfB[column].isnull()]
        
        p = mw(dfa[column], dfb[column])[1]
        
        na = len(dfa)
        nb = len(dfb)
        
        if verbose:
            print('{}: sum/mean (scale={})/median (scale={}) \n A={:,}/{:.3f}{}/{:.3f}{} (n={:,}), B={:,}/{:.3f}{}/{:.3f}{} (n={:,}), p={:.3f}'.format(
                column, scale, scale,
                int(dfa[column].sum()),
                dfa[column].mean() * scale,
                unit,
                dfa[column].median() * scale,
                unit,
                na, 
                int(dfb[column].sum()),
                dfb[column].mean() * scale, 
                unit,
                dfb[column].median() * scale,
                unit,
                nb, 
                p
            ))
        
        data = []
        data.append((
            column,
            
            #int(dfa[column].sum()),
            dfa[column].mean() * scale,
            dfa[column].median() * scale,
            na,
            
            #int(dfb[column].sum()),
            dfb[column].mean() * scale,
            dfb[column].median() * scale,
            nb,
            
            p
        ))
        
        df_out = pd.DataFrame(data, columns=[
            f'driver',
            #f'sum_{group_A_name}',
            f'mean_{group_A_name}',
            f'median_{group_A_name}',
            f'size_{group_A_name}',
            
            #f'sum_{group_B_name}',
            f'mean_{group_B_name}',
            f'median_{group_B_name}',
            f'size_{group_B_name}',
            
            f'mann_whitney_p_value',
        ])
        
        #print(df_out.head())
        
        return df_out, p
            
    except:
        
        return None, np.nan
    
    return None, np.nan
