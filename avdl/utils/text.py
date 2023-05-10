from typing import Iterable


def kv_split(txt: Iterable[str],
             delimiter: str = ':') -> dict[str, str]:
    ''' 
    split each str in txt on the first <delimiter> and output a dict 
    '''
    output = {}
    for t in txt:
        key, val = t.split(delimiter, 1)
        output[key.strip()] = val.strip()
    return output
