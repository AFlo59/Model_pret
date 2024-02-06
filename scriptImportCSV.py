## Ajout du csv depuis le drive

import pandas as pd
import shutil
import gdown
import os


output = 'SBAnational.csv'

if not os.path.isfile(output):
    drive_url = 'https://drive.google.com/uc?id=1vdNaWcJgMzUnlaDVA4FuZRFYinO8UsPQ'
    gdown.download(drive_url, output, quiet=False)

shutil.copy(output, 'DuplicateSBAnational.csv') # pour copier le csv et travailler sur un duplicata

df = pd.read_csv('DuplicateSBAnational.csv')

pd.set_option('display.max_rows', 100)