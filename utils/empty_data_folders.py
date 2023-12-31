import sys
sys.path.append('/home/larrys-linux/betblaze')

import os
import pandas as pd
from datetime import datetime, timedelta

inputPATH_ = ["./data/ts", "./data/closings"]

frames = []

# Leggi i file e aggiungi i frame dati alla lista
for folder in inputPATH_:
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            file_path = os.path.join(inputPATH_, file)
            os.remove(file_path)
    
    print(f"{folder} emptied!")