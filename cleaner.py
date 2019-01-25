#!/usr/bin/python3
"""
Keep in mind that this script will load whole file that is currently processing into memory.
"""
import argparse
import os
import re
from collections import defaultdict
from typing import Dict, Set, List, Pattern, DefaultDict, Tuple, Optional
import config
from processors import LINE_PROCESSORS


def has_required_extension(file_name: str) -> bool:
    """Check if the file has required extension."""
    _, file_extension = os.path.splitext(file_name)
    return file_extension in config.FILE_EXTENSIONS_TO_PROCESS


def build_tags(comment_symbols: config.CommentSymbol) -> config.Tag:
    """Build comment tags."""
    return config.Tag(
        f'{comment_symbols.OPENING} {config.START}{comment_symbols.CLOSING}',
        f'{comment_symbols.OPENING} {config.END}{comment_symbols.CLOSING}',
    )


def get_comment_tags(file_name: str) -> Optional[Tuple[config.Tag, config.CommentSymbol]]:
    """Get proper comment tags for given file extension."""
    _, file_extension = os.path.splitext(file_name)
    for file_extensions, comment_symbol in config.FILE_EXTENSION_COMMENT_SYMBOL.items():
        if file_extension in file_extensions:
            return build_tags(comment_symbol), comment_symbol


def get_exclude_regex(raw_regexes: Set[str]) -> Pattern:
    """Compile regexes for excluding paths."""
    return re.compile('|'.join(raw_regexes))


def save_file(path: str, lines: List[str]) -> None:
    """Save lines to file."""
    with open(path, 'w') as f:
        f.writelines(lines)


class ClosingTagNotFoundException(Exception):
    pass


def clean(path: str, line_processor: callable) -> Dict[str, List[tuple]]:
    """Process all tagged lines with given line_processor recursively."""
    exclude = get_exclude_regex(config.EXCLUDE_DIRS)
    processed_lines: DefaultDict[str, List[Tuple[int, str]]] = defaultdict(list)

    for root, _, file_names in os.walk(path):
        if exclude.search(root):
            continue
        for file_name in file_names:
            if has_required_extension(file_name):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r') as f:
                        process_line = False
                        lines_to_save: List[str] = []
                        tag, comment_symbol = get_comment_tags(file_name)
                        for line_number, line in enumerate(f.readlines()):

                            if tag.START in line:
                                process_line = True

                            if process_line:
                                processed_lines[file_path].append((line_number, line))
                                lines_to_save.append(line_processor(line, comment_symbol, tag))
                            else:
                                lines_to_save.append(line)

                            if tag.END in line:
                                process_line = False

                    # If here process_line flag is still True then raise exception cause it means that there is no closing tag.
                    if process_line:
                        raise ClosingTagNotFoundException(f'In file: {file_path} there is no closing tag!')

                    save_file(file_path, lines_to_save)
                except PermissionError:
                    print(f'Permission denied for {file_path}')

    return processed_lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean files from tagged code.')
    parser.add_argument(
        'path',
        type=str,
        help='Path to directory with files to process.',
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '-c',
        '--comment',
        action='store_true',
        help='Comment out tagged code.',
    )
    group.add_argument(
        '-u',
        '--uncomment',
        action='store_true',
        help='Uncomment tagged code.',
    )
    group.add_argument(
        '-d',
        '--check',
        action='store_true',
        help='Check which line will be affected.',
    )
    args = parser.parse_args()

    print(args)
    # TODO: Do it better
    if args.comment:
        line_processor = LINE_PROCESSORS['comment']
    elif args.uncomment:
        line_processor = LINE_PROCESSORS['uncomment']
    elif args.check:
        line_processor = LINE_PROCESSORS['uncomment']
    else:
        line_processor = LINE_PROCESSORS['delete']

    processed_files = clean(args.path, line_processor)

    # TODO: Print it in more elegant fashion
    for processed_file, processed_lines in processed_files.items():
        print(f"\033[1m\033[91m{processed_file}\033[0m\033[0m")
        for processed_line in processed_lines:
            print(f'\t{processed_line[0]}: {processed_line[1]}', end='')

# TODO: Process only changed files option.
# TODO: Fix tests.
# TODO: Write more tests.
# TODO: Logging instead of printing