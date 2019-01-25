from collections import namedtuple

START = '▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼'
END = '▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲'

Tag = namedtuple('Tag', ['START', 'END'])
CommentSymbol = namedtuple('CommentSymbol', ['OPENING', 'CLOSING'])

FILE_EXTENSION_COMMENT_SYMBOL = {
    ('.py', '.rb'): CommentSymbol('#', ''),
    ('.html',): CommentSymbol('<!--', ' -->'),
    ('.js', '.c', '.cs', '.cpp', '.go', '.hbs'): CommentSymbol('//', ''),
}

FILE_EXTENSIONS_TO_PROCESS = {
    '.py',
    '.html',
    '.c',
    '.cpp',
    '.cs',
    '.rb',
    '.go',
    '.js',
}

_supported_file_extensions = {fe for fes in FILE_EXTENSION_COMMENT_SYMBOL for fe in fes}
unsupported_file_extensions = FILE_EXTENSIONS_TO_PROCESS - _supported_file_extensions
if unsupported_file_extensions:
    raise NotImplementedError(f'File extensions are not supported yet {unsupported_file_extensions}')

EXCLUDE_DIRS = {
    r'\.idea',
    r'\.git',
    r'\__pycache__',
    r'\.mypy_cache',
    r'datastore',
    r'dist',
    r'docs',
}
