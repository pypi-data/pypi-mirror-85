import re

def clean_string(target_str):
    """ Remove ISO control characters and trim input string. Returns None if cleaned string is empty.
    Args:
        target_str (st): string to be cleaned.
    Returns:
        str: cleaned input string.
    """
    if target_str is None:
        return None
    else:
        string_clean = re.sub(r'[\x00-\x1F]+', '', target_str).strip()
        if string_clean == '':
            return None
        else:
            return string_clean

def empty_string_to_null(target_str):
    """ Check if input string is empty, and return null if so (otherwise return input string).
    Args:
        target_str (str): string to check for emptiness.
    Returns:
        str: null if input string is empty else input string.
    """
    if target_str is None:
        return None
    elif re.sub(r'[\x00-\x1F]+', '', target_str).strip() == '':
        return None
    else:
        return target_str