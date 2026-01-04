#!/usr/bin/env python3
import os
import sys
import re
import urllib.parse
from typing import Tuple

MAX_LENGTH = 60
TRUNCATE_SUFFIX = "..."
INDENT_STEP = "  "


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


def build_toc(root_dir: str, use_h1: bool, format_type: str, level: int = 0, root_path: str = None) -> str:#pyright: ignore

    lines = []
    indent = INDENT_STEP * level

    try:
        items = os.listdir(root_dir)
    except OSError:
        return ""

    files = sorted(
        [f for f in items if f.endswith('.md') and os.path.isfile(os.path.join(root_dir, f))],
        key=sort_key
    )

    subdirs = sorted(
        [d for d in items if os.path.isdir(os.path.join(root_dir, d)) and not d.startswith('.')],
        key=sort_key
    )

    # ФАЙЛЫ
    for file in files:
        filepath = os.path.join(root_dir, file)
        filename_only = os.path.splitext(file)[0]
        display_name = truncate(extract_display_name(filename_only))

        relative_path = os.path.relpath(filepath, start=root_path)
        relative_path = relative_path.replace('\\', '/')

        if format_type == 'obsidian':
            path_without_md = relative_path[:-3] if relative_path.endswith('.md') else relative_path
            escaped_display = escape_for_wikilink(display_name)
            lines.append(f"{indent}- [[{path_without_md}|{escaped_display}]]")
        else:  # github
            encoded_path = encode_for_github(relative_path)
            lines.append(f"{indent}- [{display_name}]({encoded_path})")

        if use_h1:
            h1 = extract_h1(filepath)
            if h1:
                h1_clean = truncate(h1)
                if format_type == 'obsidian':
                    h1_escaped = escape_for_wikilink(h1_clean)
                    lines.append(f"{indent}{INDENT_STEP}{h1_escaped}")
                else:
                    lines.append(f"{indent}{INDENT_STEP}{h1_clean}")

    # ПАПКИ
    for directory in subdirs:
        dir_path = os.path.join(root_dir, directory)
        display_dirname = truncate(extract_display_name(directory))

        subdir_toc = build_toc(dir_path, use_h1, format_type, level + 1, root_path)

        if subdir_toc:
            if format_type == 'obsidian':
                escaped_dirname = escape_for_wikilink(display_dirname)
                lines.append(f"{indent}- {escaped_dirname}")
            else:
                lines.append(f"{indent}- {display_dirname}")
            lines.append(subdir_toc)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python toc_gen.py <directory> [-h] [-o|-g]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  -h          Include H1 headings from files", file=sys.stderr)
        print("  -o          Obsidian format (default)", file=sys.stderr)
        print("  -g          GitHub/Gitea format", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    use_h1 = '-h' in sys.argv

    # Определяем формат
    if '-g' in sys.argv:
        format_type = 'github'
    elif '-o' in sys.argv:
        format_type = 'obsidian'
    else:
        format_type = 'obsidian'  # по умолчанию

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
        sys.exit(1)

    abs_dir = os.path.abspath(directory)
    print(build_toc(abs_dir, use_h1, format_type, root_path=os.getcwd()))


if __name__ == "__main__":
    main()



