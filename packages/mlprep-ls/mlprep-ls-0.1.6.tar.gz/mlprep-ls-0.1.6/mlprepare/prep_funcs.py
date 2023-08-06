import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import re



def save_obj(obj, name ):
    "Save object as a pickle file to a given path."
    with open(f'{name}.pkl', 'wb') as f:
        pickle.dump(obj, f)

def load_obj(name ):
    "Load object as a pickle file to a given path."
    with open(f'{name}.pkl', 'rb') as f:
        return pickle.load(f)

def ifnone(a:any,b:any)->any:
    "`a` if `a` is not None, otherwise `b`."
    return b if a is None else a

def make_date(df, date_field):
    "Make sure `df[date_field]` is of the right date type."
    field_dtype = df[date_field].dtype
    if isinstance(field_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        field_dtype = np.datetime64
    if not np.issubdtype(field_dtype, np.datetime64):
        df[date_field] = pd.to_datetime(df[date_field], infer_datetime_format=True)

def add_datepart(df, field_name, prefix=None, drop=True, time=False):
    "Helper function that adds columns relevant to a date in the column `field_name` of `df`."
    make_date(df, field_name)
    field = df[field_name]
    prefix = ifnone(prefix, re.sub('[Dd]ate$', '', field_name))
    attr = ['Year', 'Month', 'Day', 'Dayofweek', 'Dayofyear', 'Is_month_end', 'Is_month_start',
            'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    if time: attr = attr + ['Hour', 'Minute', 'Second']
    for n in attr: df[prefix + n] = getattr(field.dt, n.lower())
    # Pandas removed `dt.week` in v1.1.10
    week = field.dt.isocalendar().week if hasattr(field.dt, 'isocalendar') else field.dt.week
    df.insert(3, prefix+'Week', week)
    mask = ~field.isna()
    df[prefix + 'Elapsed'] = np.where(mask,field.values.astype(np.int64) // 10 ** 9,None)
    if drop: df.drop(field_name, axis=1, inplace=True)
    return df

def df_to_type(df, date_type=None, cont_type=None, cat_type=None):
    "Convert datetime columns and categorical columns. Make sure to pass in a list for each data type which contain the name of the columns you want to be of date type or categorical type."
    if cat_type is not None:
        df[cat_type] = df[cat_type].astype('category')
    if date_type is not None:
        for i in date_type:
            df[i] = pd.to_datetime(df[i])
            df = add_datepart(df, i)
    return df  


def split_df(df, dep_var, test_size, split_mode='random', split_var=None, cond=None):
    '''
    Function to split your data. You can split randomly, on a defined variable, or based on a condition.
    Split_mode can take three values: random, on_split_id, on_condition
    '''
    x_cols = list(df.columns)
    x_cols.remove(dep_var)
    
    if split_mode == 'random':
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(df[x_cols], df[dep_var], test_size=test_size)
    elif split_mode == 'on_split_id':
        if split_var is None:
            print('Give name of split_var')
        else:
            # list of unique_id
            unique_id_array = list(df[split_var].unique())

            # split into train and test data based on uid
            test_size=0.33
            cnt_uid = len(unique_id_array)
            len_test = np.round(cnt_uid*test_size).astype(int)
            len_train = cnt_uid - len_test

            test_idx = list(np.random.choice(unique_id_array, len_test, replace=False))
            train_idx = list(set(unique_id_array) - set(test_idx))

            X_train = df[df[split_var].isin(train_idx)].copy()
            y_train = X_train[dep_var]
            X_train = X_train[x_cols]
            X_test = df[df[split_var].isin(test_idx)].copy()
            y_test = X_test[dep_var]
            X_test = X_test[x_cols]
    elif split_mode == 'on_condition':
        if cond is None:
            print('You have to specify cond, for example like so: cond = (df.Fake_Year<1999) | (df.Fake_Month<6)')
        else:
            train_idx = np.where( cond)[0]
            test_idx = np.where(~cond)[0]

            X_train = df.iloc[train_idx]
            y_train = X_train[dep_var]
            X_train = X_train[x_cols]
            X_test = df.iloc[test_idx]
            y_test = X_test[dep_var]
            X_test = X_test[x_cols]
    else:
        print('Something is not working right, did you specify the split_mode?')

    return X_train, X_test, y_train, y_test


def cat_transform(X_train, X_test, cat_type, path=''):
    "Transforms categorical variables to int and saving the mapping into a dictionary. This is done on the training dataset."
    dict_list = []
    dict_inv_list = []
    for i in cat_type:
        dict_ = dict( enumerate(X_train[i].cat.categories ) )
        dict_inv_ = {v: k for k, v in dict_.items()}
        X_train[i] = X_train[i].map(dict_inv_).astype(int)
        X_test[i] = X_test[i].map(dict_inv_).astype(int)
        dict_list.append(dict_)
        dict_inv_list.append(dict_inv_list)
    dict_name = f'{path}dict_list_cat'
    save_obj(dict_list, dict_name)
    dict_inv_name = f'{path}dict_inv_list_cat'
    save_obj(dict_inv_list, dict_inv_name)
    return X_train, X_test, dict_list, dict_inv_list



def cont_standardize(X_train, X_test, y_train, y_test, cat_type=None, id_type=None, transform_y=True, path='', standardizer='StandardScaler'):
    "Function to standardize the continuous variables and save the standardizer. This is done on the train dataset and used for the test dataset. Standardizer can either be StandardScaler or MinMaxScaler. If id_type is defined the function will ignore these columns from standardization. If transform_y is False the function will not transform the target variable."
    cont_type = list(X_train.columns)
    if standardizer =='StandardScaler':
        scaler = StandardScaler()
        if cat_type==None and id_type==None:
            cont_type = cont_type
        elif cat_type==None:
            cont_type.remove(id_type)
        elif id_type==None:
            list(set(cont_type) - set(cat_type))
        elif cat_type==None and id_type==None:
            cont_type = cont_type
        else:
            cont_type = list(set(cont_type) - set(cat_type))
            cont_type.remove(id_type)

        X_train[cont_type] = scaler.fit_transform(X_train[cont_type])
        X_test[cont_type] = scaler.transform(X_test[cont_type])
        scaler_name = f'{path}StandardScaler'
        save_obj(scaler, scaler_name)
        if transform_y:
            scaler_y = StandardScaler()
            y_train = scaler_y.fit_transform(y_train.values.reshape(-1, 1))
            y_test = scaler_y.transform(y_test.values.reshape(-1, 1))
            scaler_y_name = f'{path}StandardScaler_y'
            save_obj(scaler_y, scaler_y_name)
        else:
            pass
        if transform_y:
            return X_train, X_test, y_train, y_test, scaler, scaler_y
        else:
            return X_train, X_test, y_train, y_test, scaler

    elif standardizer =='MinMaxScaler':
        scaler = MinMaxScaler()
        if cat_type==None and id_type==None:
            cont_type = cont_type
        elif cat_type==None:
            cont_type.remove(id_type)
        elif id_type==None:
            list(set(cont_type) - set(cat_type))
        else:
            cont_type = list(set(cont_type) - set(cat_type))
            cont_type.remove(id_type)

        X_train[cont_type] = scaler.fit_transform(X_train[cont_type])
        X_test[cont_type] = scaler.transform(X_test[cont_type])
        scaler_name = f'{path}MinMaxScaler'
        save_obj(scaler, scaler_name)
        if transform_y:
            scaler_y = MinMaxScaler()
            y_train = scaler_y.fit_transform(y_train.values.reshape(-1, 1))
            y_test = scaler_y.transform(y_test.values.reshape(-1, 1))
            scaler_y_name = f'{path}MinMaxScaler_y'
            save_obj(scaler_y, scaler_y_name)
        else:
            pass
        if transform_y:
            return X_train, X_test, y_train, y_test, scaler, scaler_y
        else:
            return X_train, X_test, y_train, y_test, scaler

    else:
        print('standardizer can either be StandardScaler or MinMaxScaler')   
        
def cont_standardize_df(df, cat_type=None, id_type=None, path='', standardizer='StandardScaler'):
    "Function to standardize the continuous variables and save the standardizer. This is done for the whole dataset. Standardizer can either be StandardScaler or MinMaxScaler. If id_type is defined the function will ignore these columns from standardization."
    cont_type = list(X_train.columns)
    if standardizer =='StandardScaler':
        scaler = StandardScaler()
        if cat_type==None and id_type==None:
            cont_type = cont_type
        elif cat_type==None:
            cont_type.remove(id_type)
        elif id_type==None:
            list(set(cont_type) - set(cat_type))
        elif cat_type==None and id_type==None:
            cont_type = cont_type
        else:
            cont_type = list(set(cont_type) - set(cat_type))
            cont_type.remove(id_type)
            
        df[cont_type] = scaler.fit_transform(df[cont_type])
        scaler_name = f'{path}StandardScaler'
        save_obj(scaler, scaler_name)
        
        return df, scaler