import os
import pandas as pd
from datetime import datetime, timedelta

inputPATH_ = ["/home/larrys-linux/betblaze/data/ts", "/home/larrys-linux/betblaze/data/closings"]

frames = []

# Leggi i file e aggiungi i frame dati alla lista
for folder in inputPATH_:
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            file_path = f"{folder}/{file}"
            os.remove(file_path)
    
    print(f"{folder} emptied!")