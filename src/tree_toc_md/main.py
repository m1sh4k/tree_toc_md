#!/usr/bin/env python3
import os
import sys

from tree_toc_md.build_tok import build_toc


def main():
    if len(sys.argv) < 2 or '-h' in sys.argv:
        print("Usage: python toc_gen.py <directory> [-e] [-o|-g]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  -e          Include H1 headings from files", file=sys.stderr)
        print("  -h          Help (this message)", file=sys.stderr)
        print("  -w          Obsidian format (Wikilinks)", file=sys.stderr)
        print("  -g          GitHub/Gitea format (default)", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]
    use_h1 = '-e' in sys.argv

    if '-g' in sys.argv:
        format_type = 'github'
    elif '-o' in sys.argv:
        format_type = 'obsidian'
    else:
        format_type = 'github'

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
        sys.exit(1)

    abs_dir = os.path.abspath(directory)
    print(build_toc(abs_dir, use_h1, format_type, root_path=os.getcwd()))


if __name__ == "__main__":
    main()

