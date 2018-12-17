#!/usr/bin/python3
"""
Keep in mind that this script will load whole file that is currently processing into memory.
"""
import argparse
import os
import re
from collections import defaultdict
from typing import Dict, Set, List, Pattern, DefaultDict, Tuple
import config

def delete_line_processor(line: str) -> None:
    """Delete the line"""
    return None


def comment_line_processor(line: str) -> str:
    """Comment out line."""
    # Do not comment commented line
    if line.strip().startswith('#'):
        return line
    return f'# {line}'


def uncomment_line_processor(line: str) -> str:
    """Uncomment line."""
    return line.replace('# ', '', 1)


LINE_PROCESSORS = {
    'delete': delete_line_processor,
    'comment': comment_line_processor,
    'uncomment': uncomment_line_processor,
}


def has_required_extension(file_name: str) -> bool:
    """Check if the file has required extension."""
    _, file_extension = os.path.splitext(file_name)
    return file_extension in config.FILE_EXTENSIONS_TO_PROCESS


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
                with open(file_path, 'r') as f:

                    process_line = False
                    lines_to_save: List[str] = []
                    for line_number, line in enumerate(f.readlines()):

                        if config.OPENING in line:
                            process_line = True

                        if process_line:
                            processed_lines[file_path].append((line_number, line))
                            processed_line = line_processor(line)
                            if processed_line:
                                lines_to_save.append(processed_line)
                        else:
                            lines_to_save.append(line)

                        if config.ENDING in line:
                            process_line = False

                # If here process_line flag is still True then raise exception caouse it means that there is no closing tag.
                if process_line:
                    raise ClosingTagNotFoundException(f'In file: {file_path} there is no closing tag!')

                save_file(file_path, lines_to_save)

    return processed_lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean files from tagged code.')
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Path to directory with files to process.',
    )
    parser.add_argument(
        '-p',
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

# TODO: Commenting processor for different file extensions.
