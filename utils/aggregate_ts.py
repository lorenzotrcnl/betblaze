import sys
sys.path.append('/home/larrys-linux/betblaze')

import os
import pandas as pd
from datetime import datetime, timedelta

inputPATH_ = "./data/ts"
outputPATH_ = f"{input}/odds_{(datetime.now()-timedelta(days=1)).strftime('%D')}.csv"

frames = [pd.read_csv(os.path.join(inputPATH_, file)) for file in os.listdir(inputPATH_) if file.endswith(".csv")]

if not frames: 
    print(f"{inputPATH_} empty!")
else:
    result = pd.concat(frames, ignore_index=True)
    result.to_csv(outputPATH_, index=False)
    print("files aggregated!")