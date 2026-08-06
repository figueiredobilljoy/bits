import re

from pipeline_config import CROP_ALIASES, STATE_ALIASES


def clean_text(value):
    if value is None:
        return None
    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)
    return value or None


def normalize_key(value):
    value = clean_text(value)
    if value is None:
        return None
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or None


def standardize_state(value):
    value = clean_text(value)
    return STATE_ALIASES.get(value, value)


def standardize_crop(value):
    value = clean_text(value)
    return CROP_ALIASES.get(value, value)

