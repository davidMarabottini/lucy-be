import pandas as pd
from typing import Any

def series_to_ravel(X: Any) -> pd.Series:
    """
    Accetta una Series / array-like e restituisce un vettore 1D (ravel).
    """
    if isinstance(X, pd.Series):
        return X.values.ravel()
    # supporto per numpy array o liste
    try:
        import numpy as np
        arr = np.asarray(X)
        return arr.ravel()
    except Exception:
        raise ValueError("Impossibile convertire X in array ravelable.")