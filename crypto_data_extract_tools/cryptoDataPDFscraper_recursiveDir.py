# v5.0.4

# Imports
import os
import re
import pandas as pd
import pdfplumber
from tqdm import tqdm
import sys

import warnings
warnings.simplefilter('ignore')


# Functions:

# This will use pdfplumber to extract the text first; 
def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Set up the regex for each specific datapoint:
def find_crypto_data(text):
    # Regular expressions for Ethereum, Bitcoin and Tron wallets and tx hashes (Solana to come in later version;)
    evm_wallet_regex = r'\b0x[a-fA-F0-9]{40}\b'
    btc_wallet_regex = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}|\b[bB][cC]1[pPqP][a-zA-Z0-9]{38,58}'
    tron_wallet_regex = r'T[a-zA-Z0-9]{33}'
    evm_tx_hash_regex = r'0x[a-fA-F0-9]{64}'
    btc_tron_tx_hash_regex = r'(?:^|[^0x])[a-fA-F0-9]{64}(?:$|[a-fA-F0-9])'
    # tron_tx_hash_regex = r'[a-fA-F0-9]{64}'
    
    evm_wallets = re.findall(evm_wallet_regex, text)
    btc_wallets = re.findall(btc_wallet_regex, text)
    tron_wallets = re.findall(tron_wallet_regex, text)
    evm_tx_hashes = re.findall(evm_tx_hash_regex, text)
    btc_tron_tx_hashes = [match.strip() for match in re.findall(btc_tron_tx_hash_regex, text)]
    # tron_tx_hashes = re.findall(tron_tx_hash_regex, text)
    
    return {
        'EVM Address': evm_wallets
        , 'Bitcoin Address (all)': btc_wallets
        , 'Tron Address': tron_wallets
        , 'EVM Txn Hash': evm_tx_hashes
        , 'Bitcoin (or Tron) Txn Hash': btc_tron_tx_hashes
        , 'Tron Txn Hash':  tron_tx_hashes
    }
    

# Set up the recursive dir search and tailor the output format (df w/ cols: 'Datapoint, 'Type', 'Document', 'Count')

def search_folder_for_crypto_data:
    results = []
    pdf_count = 0
    positive_match_pdfs = set()
    pdf_files = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
                # pdf_path = os.path.join(root, file)
                
                
                # Redirect stderr to suppress CropBox warnings
                sys.stderr = open(os.devnull, 'w')
                text = extract_text_from_pdf(pdf_path)
                sys.stderr = sys.__stderr__
                crypto_data = find_crypto_data(text)
                folder_name = os.path.basename(root)
                for key, value in crypto_data.items():
                    for item in set(value):
                        results.append({
                            'Datapoint': item
                            , 'Type': key
                            , 'Folder': folder_name
                            , 'Document': file
                            , 'Count': value.count(item)
                        })
    return results

# And of course... --> Put the output into a dataframe! ;) 

def main(folder_path):
    results = search_folder_for_crypto_data(folder_path)
    df = pd.DataFrame(results)
    return df 

folder_path = './folder/'

df = main(folder_path)
df.shape