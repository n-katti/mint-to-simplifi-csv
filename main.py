from pathlib import Path
import os
import pandas as pd 

location = Path(__file__).parent

# Input file downloaded directly from Mint
# This file has duplicates, but it lists Mint custom categories
mint_input = location / 'input/transactions.csv'

# Input file downloaded using Monarch's Browser Extension
# This file does not have duplicates, but it is missing Mint custom categories
monarch_input = location / 'input/mint-transactions.csv'


def add_categories_to_monarch(mint_df, monarch_df):
    '''
    Takes in two 
    '''

    # Create two new dataframes, one with categories and one without
    uncat = monarch_df[monarch_df['Category'] == 'Uncategorized']
    cat = monarch_df[monarch_df['Category'] != 'Uncategorized']

    # Join the uncategorized df to the mint import file based
    new_df = pd.merge(uncat, mint_df, how='inner', on=['Date', 'Description', 'Original Description', 'Amount', 'Transaction Type', 'Account Name'], suffixes=['', '_right'])

    # Rename category columns to old (uncategorized) and new (from the mint file)
    new_df = new_df.rename(columns={'Category': 'Old Category', 'Category_right' : 'New Category'})

    # Drop the _right labels and notes columns 
    drop_columns = []
    for x in new_df.columns:
        if '_right' in x:
            drop_columns.append(x)
    new_df.drop(drop_columns, axis=1, inplace=True)

    # Add a new column to flag any duplicates. This join between monarch/mint creates duplicates
    # These will need to be reviewed manually and removed if they're truly duplicates
    new_df['is_duplicate'] = False
    # Identify duplicate rows based on all columns
    duplicate_rows = new_df.duplicated()
    # Update the 'is_duplicate' column for duplicate rows
    new_df.loc[duplicate_rows, 'is_duplicate'] = True

    # Union the two dfs together
    final_df = pd.concat([new_df, cat], ignore_index=True)
    final_df = final_df.sort_values(by='Date', ascending=False)
    output_path = location / f'output/monarch_import_with_categories.csv'
    final_df.to_csv(output_path, index=False)


def merge_monarch_with_mint(monarch_df, mint_df):

    # Columns to check for matching rows. While a join would accomplish the same thing, it would lead to fanning of the output due to duplicates
    columns_to_check = ['Date', 'Description', 'Original Description', 'Amount', 'Transaction Type', 'Account Name']

    # Check which rows are in the mint export and the monarch export
    is_row_in_monarch = mint_df[columns_to_check].apply(tuple, axis=1).isin(monarch_df[columns_to_check].apply(tuple, axis=1))

    # Check which rows are in the mint export and not in the monarch export
    is_row_not_in_monarch = ~mint_df[columns_to_check].apply(tuple, axis=1).isin(monarch_df[columns_to_check].apply(tuple, axis=1))

    in_monarch_not_mint = ~monarch_df[columns_to_check].apply(tuple, axis=1).isin(mint_df[columns_to_check].apply(tuple, axis=1))

    # Get rows from mint that are also in the monarch export
    rows_in_mint_and_monarch = mint_df[is_row_in_monarch]

    # Get rows from monarch that are missing in the mint export
    rows_in_monarch_and_not_mint = monarch_df[in_monarch_not_mint]

    # Concatenate these two together and output to a file called in_mint_and_monarch.csv
    consolidated_final = pd.concat([rows_in_monarch_and_not_mint, rows_in_mint_and_monarch], ignore_index=True)
    consolidated_final['Date'] = pd.to_datetime(consolidated_final['Date'])
    consolidated_final = consolidated_final.sort_values(by='Date', ascending=False)
    output_path = location / f'output/in_mint_and_monarch.csv'
    consolidated_final.to_csv(output_path, index=False)

    # For observation sake, get rows from mint that are not in the monarch export and create an output file called in_mint_not_in_monarch.csv
    rows_not_in_monarch = mint_df[is_row_not_in_monarch]
    output_path = location / f'output/in_mint_not_in_monarch.csv'
    rows_not_in_monarch.to_csv(output_path, index=False)

    return consolidated_final


def split_into_separate_csvs(df):    

    unique_account_names = df['Account Name'].unique()

    for account in unique_account_names:
        new_df = df[df['Account Name'] == account]
        
        output_folder = location / f'output/split files/'

        # Check to see if split files folder exists already 
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = output_folder / f'{account}.csv'

        # If any account names have forbidden characters for file names, this will throw an exception
        try:
            new_df.to_csv(output_path, index=False)
            print(f'{account}.csv file written')
        except Exception as e: 
            print(f'{account} file could not be written: {e}')

with open(mint_input, 'r') as mint, open(monarch_input, 'r') as monarch:
    # Read the CSV files into pandas DataFrames
    mint_df = pd.read_csv(mint)
    monarch_df = pd.read_csv(monarch)

    merged = merge_monarch_with_mint(mint_df=mint_df, monarch_df=monarch_df)
    split_into_separate_csvs(df=merged)

