#!/usr/bin/python3
"""
I assume that files that will be processed by this script will not be so big so for simplicity and convinience
I'm loading whole file into memory.
# TODO rewrite it and create README
"""
import argparse
import os
import re
from collections import defaultdict
from typing import Dict, Set, List, Pattern, DefaultDict, Tuple

OPENING = '# ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼'
ENDING = '# ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲'

FILE_EXTENSIONS_TO_PROCESS = {
    '.py',
    '.html',
    'js',
    'hbs',
}

EXCLUDE_DIRS = {
    r'\.idea',
    r'\.git',
}


def has_required_extension(file_name: str, ) -> bool:
    _, file_extension = os.path.splitext(file_name)
    return file_extension in FILE_EXTENSIONS_TO_PROCESS


def get_exclude_regex(raw_regexes: Set[str]) -> Pattern:
    return re.compile('|'.join(raw_regexes))


def save_file(path: str, lines: List[str]) -> None:
    with open(path, 'w') as f:
        f.writelines(lines)


def delete_line_processor(line: str) -> None:
    return None


def comment_line_processor(line: str) -> str:
    return f'# {line}'


def uncomment_line_processor(line: str) -> str:
    return line.replace('# ', '', 1)


LINE_PROCESSORS = {
    'delete': delete_line_processor,
    'comment': comment_line_processor,
    'uncomment': uncomment_line_processor,
}


class ClosingTagNotFoundException(Exception):
    pass


def clean(path: str, line_processor: callable) -> Dict[str, List[tuple]]:
    exclude = get_exclude_regex(EXCLUDE_DIRS)
    processed_lines: DefaultDict[str, List[Tuple[int, str]]] = defaultdict(list)

    for root, _, file_names in os.walk(path):
        if exclude.search(root):
            continue
        for file_name in file_names:

            if has_required_extension(file_name):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as f:

                    process_line = False
                    lines_to_save: List[str] = []
                    for line_number, line in enumerate(f.readlines()):

                        if OPENING in line:
                            process_line = True

                        if process_line:
                            processed_lines[file_path].append((line_number, line))
                            processed_line = line_processor(line)
                            if processed_line:
                                lines_to_save.append(processed_line)
                        else:
                            lines_to_save.append(line)

                        if ENDING in line:
                            process_line = False

                # If here process_line flag is still True then raise exception caouse it means that there is no closing tag.
                if process_line:
                    raise ClosingTagNotFoundException(f'In file: {file_path} there is no closing tag!')

                save_file(file_path, lines_to_save)

    return processed_lines


if __name__ == '__main__':
    parser = argparse
    parser = argparse.ArgumentParser(description='Clean files from tagged code.')
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Path to directory with files to process.',
    )
    parser.add_argument(
        '--processor',
        default='delete',
        help='Line processor. What to do with tagged code?',
    )
    args = parser.parse_args()

    processed_files = clean(args.path, LINE_PROCESSORS[args.processor])

    # TODO: Print it in more elegant fashion
    for processed_file, processed_lines in processed_files.items():
        print(f"\033[1m\033[91m{processed_file}\033[0m\033[0m")
        for processed_line in processed_lines:
            print(f'\t{processed_line[0]}: {processed_line[1]}', end='')

# TODO: Extract config
# TODO: Add proper readme
#