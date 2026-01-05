import os
from tree_toc_md.constants import INDENT_STEP

from tree_toc_md.str_formatting import (
    sort_key,
    truncate,
    extract_display_name,
    extract_h1,
    escape_for_wikilink,
    encode_for_github
)

def build_toc(root_dir: str, use_h1: bool, format_type: str, level: int = 0, root_path: str = '') -> str:
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

    # FILES
    for file in files:
        filepath = os.path.join(root_dir, file)
        filename_only = os.path.splitext(file)[0]
        display_name = truncate(extract_display_name(filename_only))

        # Handle root_path logic safely
        start_path = root_path if root_path else root_dir
        relative_path = os.path.relpath(filepath, start=start_path)
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

    for directory in subdirs:
        dir_path = os.path.join(root_dir, directory)
        display_dirname = truncate(extract_display_name(directory))

        # Pass root_path recursively to maintain correct relative links
        current_root_path = root_path if root_path else root_dir
        subdir_toc = build_toc(dir_path, use_h1, format_type, level + 1, current_root_path)

        if subdir_toc:
            if format_type == 'obsidian':
                escaped_dirname = escape_for_wikilink(display_dirname)
                lines.append(f"{indent}- {escaped_dirname}")
            else:
                lines.append(f"{indent}- {display_dirname}")
            lines.append(subdir_toc)

    return "\n".join(lines)
