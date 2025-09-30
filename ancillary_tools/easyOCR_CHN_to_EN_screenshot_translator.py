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

# Torch & EasyOCR Imports
import easyocr
from PIL import Image