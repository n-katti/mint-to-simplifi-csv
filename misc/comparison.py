import pandas as pd
import os
from pathlib import Path
import sys
import shutil

location = Path(__file__).parent
pre_link_location = location / '01. pre-link'
post_link_location = location / '02. post-link'
output_folder = location / '03. outputs'
processed_files = location / '04. processed inputs'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if not os.path.exists(processed_files):
    os.makedirs(processed_files)

pre_link_files = [filename for filename in os.listdir(pre_link_location) if filename != ".gitkeep"]
post_link_files = [filename for filename in os.listdir(post_link_location) if filename != ".gitkeep"]

folder_size_list = [pre_link_files, post_link_files]

for folder in folder_size_list:
    if len(folder) != 1:
        print(f'You have {len(folder)} file(s) in either your pre-link or post-link folder. You need to have exactly 1 in each to compare. Please fix and restart script')
        sys.exit()

pre_path = pre_link_location / pre_link_files[0]
post_path = post_link_location / post_link_files[0]

pre_df = pd.read_csv(pre_path).dropna(axis=1, how='all')
post_df = pd.read_csv(post_path).dropna(axis=1, how='all')
account = pre_df['account'].max()

pre_df['postedOn'] = pd.to_datetime(pre_df['postedOn']).dt.date
post_df['postedOn'] = pd.to_datetime(post_df['postedOn']).dt.date
earliest_date_transaction = pre_df['postedOn'].min()

post_df = post_df[post_df['postedOn'] >= earliest_date_transaction]

# Columns to check for matching rows. While a join would accomplish the same thing, it would lead to fanning of the output due to duplicates
columns_to_check = ['account', 'postedOn', 'payee', 'amount']
is_post_not_in_pre = ~post_df[columns_to_check].apply(tuple, axis=1).isin(pre_df[columns_to_check].apply(tuple, axis=1))
new_rows = post_df[is_post_not_in_pre].reset_index(drop=True)

pre_df_len = len(pre_df)
post_df_len = len(post_df)
len_diff = post_df_len - pre_df_len


try: 
    new_rows_len = len(new_rows)
    print(f'There were {pre_df_len} rows before linking the account. There are now {post_df_len} rows. This is a difference of {len_diff}. This validation has found {new_rows_len} rows that are in the post-link file and not in the pre-link file')

    new_rows.to_csv(output_folder / f'{account} comparison.csv', index=False)

    shutil.move(pre_path,  location / '04. processed inputs')
    shutil.move(post_path, location / '04. processed inputs')

except Exception as e:
    print(e)