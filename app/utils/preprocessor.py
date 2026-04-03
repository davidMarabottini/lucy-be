from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import re
from typing import Any

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None) -> pd.Series:
        def clean_and_lower(text: Any) -> str:
            if pd.isna(text):
                return ''
            text = re.sub(r'[^\w\s]', '', str(text))
            return text.lower()
        
        return pd.Series(X).apply(clean_and_lower)

