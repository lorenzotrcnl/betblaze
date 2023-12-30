import sys
sys.path.append('/home/larrys-linux/betblaze')

import os
import pandas as pd
from datetime import datetime, timedelta

input_path = "./data/ts"
output_path = f"{input_path}/odds_{(datetime.now()-timedelta(days=1)).strftime('%d-%m')}.csv"

frames = [pd.read_csv(os.path.join(input_path, file)) and os.remove(os.path.join(input_path, file)) for file in os.listdir(input_path) if file.endswith(".csv")]

if not frames:
    print(f"{input_path} empty!")
else:
    result = pd.concat(frames, ignore_index=True)
    result.to_csv(output_path, index=False)
    print("Files aggregated and individual files deleted!")