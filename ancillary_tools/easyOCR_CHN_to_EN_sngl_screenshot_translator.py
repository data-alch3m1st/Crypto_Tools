# Imports (core & functional)

import os
import re
import random
from glob import glob
from deeptranslate import GoogleTranslator

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm
import sys

import warnings
warnings.simplefilter('ignore')

# Torch & EasyOCR Imports (Need to import numerous PyTorch packages to avoid errors:)
import easyocr
from PIL import Image
import cv2

import torch
import torchvision
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, TensorDataset


# OCR Reader Initialization (with Chinese support)
reader = easyocr.Reader(['ch_sim','en'])                       
translator = GoogleTranslator(source='chinese (simplified)', target='english')

# Functions:
def extract_and_translate(image_path):
    """Extracts Chinese text from an image and translates it to English.

    Args:
        image_path (str): The file path of the image containing Chinese text.

    Returns:
        pd.DataFrame: A DataFrame containing the original Chinese text and its English translations.
    """
    
    # Read image and perform OCR
    results = reader.readtext(image_path, detail=0)
    
    # Filter out empty strings
    chinese_texts = [text.strip() for text in results if text.strip()]
    
    # Translate each line
    translations = []
    for text in chinese_texts:
        try:
            translated_text = translator.translate(text)
            translations.append(translated_text)
        except Exception as e:
            translations.append(f"Translation Error: {str(e)}")
            
    # Create Dataframe
    df = pd.DataFrame({
        'Original Chinese Text': chinese_texts
        , 'Translated English Text': translations
    })
    
    return df

# Example usage:
image_path = './sample_screenshots/chinese_screenshot1.png' # Replace with your image path
df_result = extract_and_translate(image_path)
df_result
