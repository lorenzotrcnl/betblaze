import sys
sys.path.append('/Users/lorenzotarcinale/repo/betblaze')

import os
import pandas as pd

def aggregate_files(inputPATH, outputPATH):
    inputPATH_ = inputPATH
    outputPATH_ = outputPATH
    frames = [pd.read_csv(os.path.join(inputPATH_, file)) for file in os.listdir(inputPATH_) if file.endswith(".csv")]

    if not frames: 
        print(f"{inputPATH_} empty!")
        return

    result = pd.concat(frames, ignore_index=True)
    result.to_csv(outputPATH_, index=False)
    print("files aggregated!")
