import re
from unidecode import unidecode


def clean_text(text: str) -> str:
    """[This function removes convert all alphabetical
        char into ascii and replace non a-z0-9 with a space]

    Args:
        text (str): [Text that has to be cleaned]

    Returns:
        str: [Cleaned text]
    """
    text = unidecode(text.lower())
    text = re.sub('^[a-z0-9]+', ' ', text)
    return text