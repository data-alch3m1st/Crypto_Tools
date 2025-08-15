# cryptoData_PDFscraper
# v3.0.1

import pdfplumber
import re
import os
import sys
import pandas as pd

# Build the functions:

def extract_text_from_pdf(pdf_path):
    text = ''
    page_texts = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_texts[i+1] = page.extract_text()
            text += page.extract_text()
    return text, page_texts

def find_crypto_data(text, page_texts):
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
    
    # Find the first page where each matched string appears:
    first_page_appearances = {}
    
    for key, values in [
        ('Ethereum Address', eth_wallets)
        , ('Bitcoin Address (All)', btc_wallets)
        , ('Tron Address', tron_wallets)
        , ('Ethereum Txn Hash', eth_tx_hashes)
        , ('Bitcoin (or Tron) Txn Hash', btc_tron_tx_hashes)
        # , ('Tron Txn Hash', tron_tx_hashes)
    ]:
        for value in values:
            for page, page_text in page_texts.items():
                if value in page_text and value not in first_page_appearances:
                    first_page_appearances[value] = page
                    
    return {
        'Ethereum Address': eth_wallets
        , 'Bitcoin Address (All)', btc_wallets
        , 'Tron Address': tron_wallets
        , 'Ethereum Txn Hash': eth_tx_hashes
        , 'Bitcoin (or Tron) Txn Hash': btc_tron_tx_hashes
        # , 'Tron Txn Hash': tron_tx_hashes
    }, first_page_appearances
    
def search_pdf_for_crypto_data(pdf_path):
    results = []
    sys.stderr = open(os.devnull, 'w')
    text, page_texts = extract_text_from_pdf(pdf_path)
    sys.stderr = sys.__stderr__
    crypto_data, first_page_appearances = find_crypto_data(text, page_texts)
    
    for key, value in crypto_data.items():
        for item in set(value):
            results.append({
                'Datapoint': item
                , 'Type': key
                , 'Document': os.path.basename(pdf_path)
                , 'Count': value.count(item)
                , 'First Page Appearance': first_page_appearances.get(item, None)
            })
    return results

# And of course - put the output in a dataframe!
def main(pdf_path):
    result = search_pdf_for_crypto_data(pdf_path)
    df = pd.DataFrame(results)
    return df

# Now, load the pdf and turn it into a dataframe:
pdf_path = './input/sample.pdf'
df = main(pdf_path)

# Can sort by 'Count' (ascending=False) to show most frequent match, or by 'First Page Appearance' (ascending=True) to show matches in an ordinal manner;
