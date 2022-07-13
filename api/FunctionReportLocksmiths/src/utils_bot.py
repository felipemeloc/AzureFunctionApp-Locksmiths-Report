"""
This is a custom module to adapt the format of the data to be printed on Telegram.

This module needs the installation of the following package:
* pandas: return a DataFrame object

Contains the following function:
* trans_one_row: Return string for total queries. Use:

    import utils_bot
    utils_bot.trans_one_row(df= YOUR_DATAFRAME)

* df_to_str: Return string for table; It can be added a title for the table. Use:

    import utils_bot
    utils_bot.df_to_str(df= YOUR_DATAFRAME,
                        title= 'YOUR TITLE')

* df_staff_sales_to_str: Return string for table. The function add the £ simbol for money in the sales project.

    import utils_bot
    utils_bot.df_staff_sales_to_str(o_df = YOUR_DATAFRAME
        )

* df_locksmith_to_str: Return string for table. The function add the £ simbol for money in the locksmith project.
                       The function requeres that the column to be converted to money is define.

    import utils_bot
    utils_bot.df_locksmith_to_str(o_df = YOUR_DATAFRAME,
                                  money_col = 'YOUR_COLUMN_NAME')

"""

import pandas as pd
from tabulate import tabulate

def trans_one_row(df:pd.DataFrame, money=False)->str:
    """Function for convert a SQL query into a string to be printed in the chatbot.
    Function made for dataframes of shape (1,1).

    Args:
        df (pd.DataFrame): Dataframe of shape (1,1)

    Returns:
        str: string for total queries
    """    
    # Validate the dataframe shape
    if df.shape[0] == 1 and df.shape[1] == 1:
        df = df.reset_index(drop=True).fillna(0)
        key = df.columns[0]
        val = df.iloc[0,0]
        # Adapt information to be printed
        if money:
            return f'*{key}*: £{val}'
        else:
            return f'*{key}*: {val}'
    else:
        print('The df should have a shape equal to (1, 1)')
        raise

def df_to_str(df:pd.DataFrame, title:str=None)->str:
    """Function for convert a SQL query into a string to be printed in the chatbot.
    Function made for dataframes of shape (n,2).

    Args:
        df (pd.DataFrame): Dataframe to be transformed. Dataframe of shape (n,2)
        title (str, optional): Table title. Defaults to None.

    Returns:
        str: return string for table
    """    
    # Validate the dataframe shape
    if df.shape[1] == 2:
        if title:
            # Set title added from user
            data =[title]
        else:
            # Set title from columns name
            data = [f'*{df.columns[1]} per {df.columns[0]}*']
        # Adapt information to be printed
        for _, row in df.iterrows():
            r = f'\t- {row[0]:<9}: {row[1]}'
            data.append(r)
        return '\n'.join(data)
    else:
        print('The df should have a shape equal to (n, 2)')
        raise

def df_staff_sales_to_str(o_df:pd.DataFrame)->str:
    df = o_df.copy()
    df['Name'] = df['Name'].str.slice(0,12)
    df['Amount'] = '£' + df['Amount'].astype(str)
    df_str = df_more_two_cols(df)
    return df_str

def df_more_two_cols(df:pd.DataFrame)->str:
    df_str = tabulate(df, showindex=False, headers=df.columns, tablefmt="prety", numalign='rigth')
    return df_str

def clean_locksmith_name(col:pd.Series)->pd.Series:
    return col.str.lower().replace(r'wgtk[\s]*[\-]*', '', regex=True).str.replace(r'\(.*\)', '', regex=True).str.replace(r'[\s]+',' ',regex=True).str.strip().str.capitalize()

def df_locksmith_to_str(o_df:pd.DataFrame, money_col:str=None)->str:
    df = o_df.copy()
    if not df.empty:
        df['Locksmith'] = clean_locksmith_name(df['Locksmith'])
        df = df.groupby('Locksmith', as_index=False).sum().sort_values(df.columns[-1], ascending=False)
        if money_col:
            df[money_col] = '£' + df[money_col].astype(str)
    str_df = df_to_str(df)
    return str_df

def selected_vs_invoice_locksmiths(o_df:pd.DataFrame)->str:
    if not o_df.empty:
        df = o_df.copy()
        df['LocksmithName'] = clean_locksmith_name(df['LocksmithName'])
        df['RecipientName'] = clean_locksmith_name(df['RecipientName'])
        df = df[df['LocksmithName'] != df['RecipientName']][['ReportID', 'NetCost']]
        if not df.empty:
            df['NetCost'] = '£' + df['NetCost'].astype(str)
            str_df = df_to_str(df, title= 'Not matching locksmiths')
            return str_df

def completed_job_revenue_by_locksmith_day(o_df:pd.DataFrame)->str:
    df = o_df.copy()
    if not df.empty:
        df['Locksmith'] = clean_locksmith_name(df['Locksmith'])
        df = df.groupby('Locksmith', as_index=False).sum().sort_values(['Revenue', 'No'], ascending=False)
        df['Revenue'] = '£' + df['Revenue'].astype(str)
    df_str = df_more_two_cols(df)
    return df_str