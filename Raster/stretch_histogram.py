import numpy as np

def stretch(array):
    
    min_percent = 2   # Low percentile
    max_percent = 98  # High percentile
    lo, hi = np.percentile(array, (min_percent, max_percent))

    # Apply linear "stretch" - lo goes to 0, and hi goes to 1
    res_img = (array.astype(float) - lo) / (hi-lo)

    #Multiply by 255, clamp range to [0, 255] and convert to uint8
    res_img = np.maximum(np.minimum(res_img*255, 255), 0).astype(np.uint8)

    return res_img