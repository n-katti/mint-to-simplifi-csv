# mint-to-simplifi

## Usage

### This script will output the following three things: 
1. Split CSVS by Account Name that you can use to import directly into Simplifi. These are located in the folder `output/split files`
2. `in_mint_and_monarch.csv` - this is the source that is used to split into the different CSVs. This is the output of taking your Mint export and Monarch export, excluding rows that are in the Mint export and <b>NOT</b> in the Monarch export, maintaining the categories from the Mint export, and adding on any additional rows from the Monarch export that are <b>NOT</b> in the Mint export (there are some Venmo transactions I had from the last few days picked up by Monarch and not Mint)
3. `in_mint_not_in_monarch.csv` - if you're curious, these are the rows that were in the Mint export but <b>NOT</b> in the Monarch export and therefore excluded from the final split files

### Setup 
1. If you don't already have the pandas Python library, run 
`pip install -r requirements.txt`
2. Download your consolidated Mint transactions from Mint. This will be downloaded as `transactions.csv`. Place this file in the `input` folder of the main directory
3. Use the <a href="https://chromewebstore.google.com/detail/mint-data-exporter-by-mon/doknkjpaacjheilodaibfpimamfgfhap">Mint Data Exporter by Monarch Money</a> browser extension (also available on Edge and Firefox) to download another consolidated file of your Mint transactions. This will be downloaded as `mint-transactions.csv`. Also place this file in the `input` folder of the main directory
4. Run main.py which will output the above 3 files in the `output` folder
