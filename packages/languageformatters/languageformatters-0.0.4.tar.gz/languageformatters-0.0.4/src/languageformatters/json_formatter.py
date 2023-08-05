# Copyright © 2020 Matthew Burkard
#
# This file is part of Language Formatters
#
# Language Formatters is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Language Formatters is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Language Formatters.  If not, see
# <https://www.gnu.org/licenses/>.
import re
from enum import Enum, auto
from random import random, choice
from typing import List, Optional, Tuple

from languageformatters.format_tools import depopulate, add_indents, repopulate


class Spaces(Enum):
    BEFORE = auto()
    AFTER = auto()
    BOTH = auto()
    NONE = auto()


class BracketWrap(Enum):
    INLINE = auto()
    INLINE_STACKED = auto()
    FORCE_LINEBREAK = auto()


def style(sample: str,
          indent: int = 2,
          use_tabs: bool = False,
          bracket_wrap: BracketWrap = BracketWrap.INLINE,
          colon_space: Spaces = Spaces.AFTER,
          comma_space: Spaces = Spaces.AFTER) -> str:
    """Get a styled JSON string.

    :param sample: Un-styled JSON string.
    :param indent: Number of spaces to indent by, default is 4.
    :param use_tabs: Will indent with tabs if True, default is False.
    :param bracket_wrap: Determine how linebreaks are made around
        brackets.
    :param colon_space: How to add spaces around colons.
    :param comma_space: How to add spaces around commas.
    :return: Formatted version of the given JSON string.
    """
    # Depopulate all JSON values and comments.
    num_reg = re.compile(r'(\d+\.?\d*)')
    numbers, num_mark, sample = depopulate(num_reg, sample)
    escaped_escapes = re.compile(r'\\{2}')
    escapes, escapes_mark, sample = depopulate(escaped_escapes, sample)
    quote_reg = re.compile(r'".*?(?<!\\)"')
    quotes, quotes_mark, sample = depopulate(quote_reg, sample)
    block_comment_reg = re.compile(r'/\*.*?\*/', re.S)
    block_comments, block_comment_mark, sample = depopulate(block_comment_reg,
                                                            sample)
    comment_reg = re.compile(r'//.*$')
    comments, comment_mark, sample = depopulate(comment_reg, sample)
    kw_reg = re.compile(r'(null|true|false)')
    key_words, kw_mark, sample = depopulate(kw_reg, sample)
    # Remove all white space.
    sample = re.sub(r'\s', '', sample)
    # Add a newlines around brackets.
    if bracket_wrap == BracketWrap.INLINE:
        sample = re.sub(r'([\[{])(?![]}])', r'\1\n', sample)
        sample = re.sub(r'(?<![\[{])([]}])', r'\n\1', sample)
        sample = re.sub(r'([]}]),(?!\n)', r'\1,\n', sample)
        sample = re.sub(r'(?<!\[)],(?![\n\[])', '],\n', sample)
    elif bracket_wrap == BracketWrap.INLINE_STACKED:
        sample = re.sub(r'{(?![}[])', '{\n', sample)
        sample = re.sub(r'\[(?![\[\]{])', '[\n', sample)
        sample = re.sub(r'(?<![{\]])}', '\n}', sample)
        sample = re.sub(r'(?<![[}])]', '\n]', sample)
        sample = re.sub(r'([]}]),<', r'\1,\n<', sample)
    elif bracket_wrap == BracketWrap.FORCE_LINEBREAK:
        sample = re.sub(r'([[{])(?![]}])', r'\n\1', sample)
        sample = re.sub(r'(?<![[{])([]}])', r'\n\1', sample)
        sample = re.sub(r'([[{])(?=<)', r'\1\n', sample)
        sample = re.sub(r'([]}]),<', r'\1,\n<', sample)
        sample = re.sub(r'(?<!\[)],(?![\n\[])', '],\n', sample)
    # Add a newline after bracket pairs.
    sample = re.sub(r'({}|\[]),(?!\n)', r'\1,\n', sample)
    # Add a newline after the end of any JSON values (All values have
    # already been depopulated so they will end with a ">").
    sample = re.sub(r'(>,)', r'\1\n', sample)
    # Add a spaces for colons.
    if colon_space == Spaces.AFTER:
        sample = re.sub(r':(?=\S)', ': ', sample)
    elif colon_space == Spaces.BEFORE:
        sample = re.sub(r'(?<=\S):', ' :', sample)
    elif colon_space == Spaces.BOTH:
        sample = re.sub(r'(?<=\S):', ' :', sample)
        sample = re.sub(r':(?=\S)', ': ', sample)
    # Add a spaces for commas.
    if comma_space == Spaces.AFTER:
        sample = re.sub(r',(?=\S)', ', ', sample)
    elif comma_space == Spaces.BEFORE:
        sample = re.sub(r'(?<=\S),', ' ,', sample)
    elif comma_space == Spaces.BOTH:
        sample = re.sub(r'(?<=\S),', ' ,', sample)
        sample = re.sub(r',(?=\S)', ', ', sample)
    sample = add_indents(sample, indent, use_tabs)
    # Repopulate all depopulated JSON values.
    sample = repopulate(comments, comment_mark, sample)
    sample = repopulate(block_comments, block_comment_mark, sample)
    sample = repopulate(quotes, quotes_mark, sample)
    sample = repopulate(escapes, escapes_mark, sample)
    sample = repopulate(key_words, kw_mark, sample)
    sample = repopulate(numbers, num_mark, sample)
    return sample


def scramble(sample: str,
             preserve_linebreaks: bool = False,
             preserve_word_breaks: bool = False,
             preserve_blocks: Optional[List[Tuple[str, str]]] = None) -> str:
    """Add random white space in random places in a given JSON string.

    :param sample: The sample to add whitespace to.
    :param preserve_linebreaks: If True linebreaks will be kept as is.
    :param preserve_word_breaks: If True word breaks will be kept as is.
    :param preserve_blocks: Beginning and end sequence to sub strings
        that are not to be changed, default [('"', '"')].
    :return: The sample string with random whitespace.
    """
    preserve_blocks = preserve_blocks or [('"', '"')]
    # Remove all blocks that are to be preserved.
    blk_matches_lists: List[List[str]] = []
    blk_markers: List[str] = []
    for opener, closer in preserve_blocks:
        pattern = re.compile(fr'{opener}.*?{closer}', re.M)
        mat, mark, sample = depopulate(pattern, sample)
        blk_matches_lists.append(mat)
        blk_markers.append(mark)
    # If preserve_linebreaks we don't want to add or remove newlines.
    if preserve_linebreaks:
        pattern = re.compile(r'[ \t]+')
        filler = [' ']
    else:
        pattern = re.compile(r'\s+')
        filler = [' ', '\n', ' \n ']

    def rand(maximum: int) -> int: return round(random() * maximum)

    matches, marker, sample = depopulate(pattern, sample)
    rand_white = [rand(3) * choice(filler) for _ in matches]
    sample = repopulate(rand_white, marker, sample)
    # If we are preserving word breaks add random filler at word breaks.
    if not preserve_word_breaks:
        # Negatives on <> because this pattern has to protect markers.
        pattern = re.compile(r'(?<!<)([\b:,[\]{}])(?!>)')
        pre_white = rand(2) * choice(filler)
        post_white = rand(2) * choice(filler)
        sample = re.sub(pattern, fr'{pre_white}\1{post_white}', sample)
    # Add random whitespace at beginning and end of lines.
    sample = ''.join(rand(3) * ' ' + f'{line}\n' + rand(3) * ' '
                     for line in sample.split('\n'))
    # Remove random line breaks.
    if not preserve_linebreaks:
        sample = ''.join('\n' * round(random()) + line
                         for line in sample.split('\n'))
    # Repopulate the preserved blocks.
    for i in range(len(blk_markers)):
        sample = repopulate(blk_matches_lists[i], blk_markers[i], sample)
    return sample
