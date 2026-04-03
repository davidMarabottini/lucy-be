from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import io
from email import parser as email_parser
import re
from typing import Dict

def extract_raw_features(raw_email_text: str) -> Dict[str, object]:
    """
    Estrae feature strutturali e testo pulito dal contenuto RAW di un'email.
    """
    msg = email_parser.Parser().parse(io.StringIO(raw_email_text or ""))
    
    features = {
        'subject': msg['subject'] or '',
        'from_header': msg['from'] or '',
        'content_type': msg.get_content_type() if hasattr(msg, 'get_content_type') else '',
        'body_text': '',
        'is_html': False
    }

    body = ''
    if hasattr(msg, 'is_multipart') and msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = part.get('Content-Disposition')
            if ctype == 'text/plain' and not cdisp:
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode(errors='ignore')
            elif ctype == 'text/html':
                features['is_html'] = True
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            try:
                body = payload.decode(errors='ignore')
            except Exception:
                body = str(payload)

    features['body_text'] = body or ''
    
    from_domain_match = re.search(r'@([\w\.-]+)', features['from_header'])
    features['from_domain'] = from_domain_match.group(1).lower() if from_domain_match else 'unknown'
    features['body_length'] = len(features['body_text'])
    
    return features

class RawEmailToFeaturesTransformer(BaseEstimator, TransformerMixin):
    """
    Trasformatore personalizzato per applicare il parsing RAW delle email
    e restituire le feature strutturate in un DataFrame.
    """
    def __init__(self, raw_column_name='origin'):
        self.raw_column_name = raw_column_name 
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X, columns=[self.raw_column_name])
        
        if self.raw_column_name not in X.columns:
            raise ValueError(f"DataFrame non contiene la colonna '{self.raw_column_name}'.")
        list_of_feature_dicts = X[self.raw_column_name].apply(lambda t: extract_raw_features(t or "")).tolist()
        df_parsed = pd.DataFrame(list_of_feature_dicts)
        return df_parsed[['subject', 'content_type', 'body_text', 
                          'is_html', 'from_domain', 'body_length']]