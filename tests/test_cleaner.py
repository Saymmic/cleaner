import os
from unittest.mock import patch, mock_open, call, MagicMock

import pytest

import cleaner
from tests.data import FILE_BEFORE_PROCESSING, FILE_AFTER_DELETE_PROCESSOR, FILE_AFTER_COMMENT_PROCESSOR, FILE_WITHOUT_CLOSING_TAG


@pytest.mark.parametrize(
    'line_processor_name, line, processed_line',
    [
        ('delete', 'I really like python language!', None),
        ('comment', 'I really like python language!', '# I really like python language!'),
        ('uncomment', '# I really like python language!', 'I really like python language!'),

    ]
)
def test_line_processors(line_processor_name, line, processed_line):
    line_processor = cleaner.LINE_PROCESSORS[line_processor_name]
    assert processed_line == line_processor(line)


def test_clean__include_only_defined_extensions_and_exclude_dirs():
    def mock_walk(path: str):
        return [
            ('root_dir', [], ['mango.py', 'bannana.js', 'raspberry.html', 'lenmon.txt']),
            ('test/excluded_dir', [], ['blackberry.py', 'cherry.js']),
        ]

    line_processor = lambda line: None
    path = '.'
    with patch('builtins.open', mock_open(read_data='Some data about fruits, irrelevant')) as mocked_open, \
            patch('os.walk', mock_walk), \
            patch('cleaner.FILE_EXTENSIONS_TO_PROCESS', {'.py', '.js'}), \
            patch('cleaner.EXCLUDE_DIRS', {'excluded_dir'}):
        cleaner.clean(path, line_processor)

    assert mocked_open.call_args_list == [
        call('root_dir/mango.py', 'r'),
        call('root_dir/mango.py', 'w'),
        call('root_dir/bannana.js', 'r'),
        call('root_dir/bannana.js', 'w'),
    ]


@pytest.mark.parametrize(
    'line_processor_name, file_data, expected_result',
    [
        ('delete', FILE_BEFORE_PROCESSING, FILE_AFTER_DELETE_PROCESSOR),
        ('comment', FILE_BEFORE_PROCESSING, FILE_AFTER_COMMENT_PROCESSOR),
        ('uncomment', FILE_AFTER_COMMENT_PROCESSOR, FILE_BEFORE_PROCESSING),

    ]
)
def test_clean(line_processor_name, file_data, expected_result):
    def mock_walk(path: str):
        return [
            ('root_dir', [], ['mango.py']),
        ]

    line_processor = cleaner.LINE_PROCESSORS[line_processor_name]
    path = '.'
    with patch('builtins.open', mock_open(read_data=file_data)), \
            patch('os.walk', mock_walk), \
            patch('cleaner.save_file', MagicMock()) as save_file_mock, \
            patch('cleaner.FILE_EXTENSIONS_TO_PROCESS', {'.py', '.js'}), \
            patch('cleaner.OPENING', '# ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼'), \
            patch('cleaner.ENDING', '# ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲'):
        cleaner.clean(path, line_processor)

    expected = [l + '\n' for l in expected_result.split('\n')][:-1]  # Split wihotut deleting delimiter
    assert (save_file_mock.call_args_list == [call('root_dir/mango.py', expected)])


def test_clean__rise_exception_where_no_closing_tag():
    def mock_walk(path: str):
        return [
            ('root_dir', [], ['mango.py']),
        ]

    line_processor = lambda line: None
    path = '.'
    with patch('builtins.open', mock_open(read_data=FILE_WITHOUT_CLOSING_TAG)), \
            patch('os.walk', mock_walk), \
            patch('config.FILE_EXTENSIONS_TO_PROCESS', {'.py', '.js'}), \
         patch('cleaner.save_file', MagicMock()) as save_file_mock, \
            patch('config.OPENING', '# ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼'), \
            patch('config.ENDING', '# ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲'), \
            pytest.raises(cleaner.ClosingTagNotFoundException):
        cleaner.clean(path, line_processor)
    save_file_mock.assert_not_called()
