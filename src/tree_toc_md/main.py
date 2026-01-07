#!/usr/bin/env python3
import argparse
import os
import sys

from tree_toc_md.build_tok import build_toc


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Markdown Table of Contents tree.",
        usage="toc-md -d <dir> [-r <root>] [-e] [-o|-g]"
    )

    parser.add_argument(
        "-d", "--dir",
        default=".",
        help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "-r", "--root",
        default=os.getcwd(),
        help=(
            "Root directory for relative links"
            "(default: current working directory)"
        )
    )
    parser.add_argument(
        "-e", "--extract-h1",
        action="store_true",
        help="Include H1 headings from files"
    )

    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument(
        "-o", "--obsidian",
        action="store_true",
        help="Obsidian format (Wikilinks)"
    )
    format_group.add_argument(
        "-g", "--github",
        action="store_true",
        help="GitHub/Gitea format (default)"
    )

    args = parser.parse_args()

    format_type = 'obsidian' if args.obsidian else 'github'

    if not os.path.isdir(args.dir):
        print(f"Error: Directory '{args.dir}' does not exist", file=sys.stderr)
        sys.exit(1)

    abs_scan_dir = os.path.abspath(args.dir)
    abs_link_root = os.path.abspath(args.root)

    print(build_toc(
        root_dir=abs_scan_dir,
        use_h1=args.extract_h1,
        format_type=format_type,
        root_path=abs_link_root
    ))


if __name__ == "__main__":
    main()
