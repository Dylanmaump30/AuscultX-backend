import numpy as np
import os
def create_directory(directory):
    os.makedirs(directory, exist_ok=True)


def compute_threshold(amp):
    return max(1.0, np.mean(amp) + 2.0 * np.std(amp))  


