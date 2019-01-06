from re import sub

from config import CommentSymbol, Tag


def delete_line_processor(line: str, comment_symbol: CommentSymbol, tag: Tag) -> str:
    """Delete the line"""
    return ''


def comment_line_processor(line: str, comment_symbol: CommentSymbol, tag: Tag) -> str:
    """Comment out line."""
    # Do not comment commented line
    if line.strip().startswith(comment_symbol.OPENING):
        return line
    return f'{comment_symbol.OPENING}{line}{comment_symbol.CLOSING}'


def uncomment_line_processor(line: str, comment_symbol: CommentSymbol, tag: Tag) -> str:
    """Uncomment line."""
    if tag.START in line or tag.END in line:
        return line
    # Remove opening tag
    line = line.replace(comment_symbol.OPENING, '', 1)
    # Remove ending tag
    return sub(f'{comment_symbol.CLOSING}', '', line)


def check_line_processor(line: str, comment_symbol: CommentSymbol, tag: Tag) -> str:
    """Delete the line"""
    return line


LINE_PROCESSORS = {
    'delete': delete_line_processor,
    'comment': comment_line_processor,
    'uncomment': uncomment_line_processor,
    'check': check_line_processor,
}
