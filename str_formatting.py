import re
import urllib.parse
from typing import Tuple
from constants import (
        MAX_LENGTH,
        TRUNCATE_SUFFIX
)


def starts_with_number(name: str) -> Tuple[bool, int]:
    match = re.match(r'^(\d+)\.\s', name)
    if match:
        return True, int(match.group(1))
    return False, 0


def sort_key(name: str) -> Tuple[int, int, str]:
    has_number, number = starts_with_number(name)
    if has_number:
        return (0, number, name)
    return (1, 0, name.lower())


def truncate(text: str, max_length: int = MAX_LENGTH) -> str:
    if len(text) > max_length:
        return text[:max_length] + TRUNCATE_SUFFIX
    return text


def extract_display_name(name: str) -> str:
    match = re.match(r'^\d+\.\s+(.+)$', name)
    if match:
        return match.group(1)
    return name


def extract_h1(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                match = re.match(r'^#\s+(.+)$', line)
                if match:
                    return match.group(1)
    except Exception:
        pass
    return ""


def escape_for_wikilink(text: str) -> str:
    return text.replace('[', '\\[').replace(']', '\\]')


def encode_for_github(filepath: str) -> str:
    parts = filepath.split('/')
    encoded_parts = [urllib.parse.quote(part) for part in parts]
    return "/".join(encoded_parts)
