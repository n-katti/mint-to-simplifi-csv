# mint-to-simplifi

This repo will help in transitioning from Mint to Simplifi and validating your results to ensure accuracy. The overall steps for this process:
1. Download your data from Mint and Monarch
2. Run main.py to merge the two files together and split into separate accounts
3. Add a manual account in Simplifi
4. Import transactions for that account
5. (Optional) run comparison.py (instructions in the Optional section below)
6. Create an automated connection to that account in Simplify and connect it to the manual account
7. Simplifi attempts to reconcile the categories that you set in Mint with what it offers by default (they have some smarts set up where even if a 1:1 relationship between your Mint category and Simplifi category isn't detected, it will choose the correct category most times. E.g. Alcohol & Bars in Mint will be mapped to Bars in Simplifi)
8. For any completely custom categories, Simplifi will create a category folder called `Mint` and then sub-categories for each of your custom Mint categories. After you complete the process of importing all of your data, you can manage your Simplifi Categories and move things around/remap transactions in a somewhat bulk fashion

## Usage

### This script will output the following three things: 
1. Split CSVs by Account Name that you can use to import directly into Simplifi. These are located in the folder `output/split files`
2. `in_mint_and_monarch.csv` - this is the source that is used to split into the different CSVs. This is the output of taking your Mint export and Monarch export, excluding rows that are in the Mint export and <b>NOT</b> in the Monarch export, maintaining the categories from the Mint export, and adding on any additional rows from the Monarch export that are <b>NOT</b> in the Mint export (there are some Venmo transactions I had from the last few days picked up by Monarch and not Mint)
3. `in_mint_not_in_monarch.csv` - if you're curious, these are the rows that were in the Mint export but <b>NOT</b> in the Monarch export and therefore excluded from the final split files

### Setup 
1. If you don't already have the pandas Python library, run 
`pip install -r requirements.txt`
2. Download your consolidated Mint transactions from Mint. This will be downloaded as `transactions.csv`. Place this file in the `input` folder of the main directory
3. Use the <a href="https://chromewebstore.google.com/detail/mint-data-exporter-by-mon/doknkjpaacjheilodaibfpimamfgfhap">Mint Data Exporter by Monarch Money</a> browser extension (also available on Edge and Firefox) to download another consolidated file of your Mint transactions. This will be downloaded as `mint-transactions.csv`. Also place this file in the `input` folder of the main directory
4. Run main.py which will output the above 3 files in the `output` folder



#### Optional: Validate Your Account Data in Simplify Post-Import/Before Linking Automatic Account vs. Post-Import/After Linking Automatic Account  
1. This is just an additional step to validate the import to Simplifi is working properly after connecting your account
2. For example: 
 - I imported my transactions for an account from Mint, and I had split the transaction in Mint, so it came through as 2 transactions in Simplifi 
 - After I linked my account after the import, Simplifi pulled in yet another line item, as Simplifi could not reconcile the split with my bank
 - In actual terms, I had $100 charge in Mint, that I split into two line items of $50 each. After I linked, Simplify looked for that $100 charge and couldn't find it, so it created a new line item for $100. 
 - In effect, Simplifi now shows $50 + $50 + $100. I want to delete that $100 row manually

 <b>In order to use this file:</b>
 1. Create a manual Simplifi account
 2. Import your transactions for that account 
 3. Export that data from Simplifi and put in the pre-link folder
 4. Now, connect to your financial provider and link the account to the manual account 
 5. Again, export the data for that account from Simplify and put in the post-link folder
 6. Run this script and see what new transactions Simplifi added
 7. Delete those extra tranactions manually (if you want to)