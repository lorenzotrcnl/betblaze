import os
import pandas as pd
from datetime import datetime, timedelta

inputPATH_ = "/home/larrys-linux/betblaze/data/ts"
outputPATH_ = f"{inputPATH_}/odds_{(datetime.now()-timedelta(days=1)).strftime('%d-%m')}.csv"

frames = []

# Leggi i file e aggiungi i frame dati alla lista
for file in os.listdir(inputPATH_):
    if file.endswith(".csv"):
        file_path = f"{inputPATH_}/{file}"
        try:
            frame = pd.read_csv(file_path)
            frames.append(frame)
            # Elimina il file dopo averlo letto ed aggiunto al frame
            os.remove(file_path)
        except pd.errors.EmptyDataError:
            print(f"skipping empty file: {file}")

if not frames:
    print(f"{inputPATH_} empty!")
else:
    # Unisci tutti i frame dati in uno
    result = pd.concat(frames, ignore_index=True)
    result.to_csv(outputPATH_, index=False)
    print("files aggregated!")
