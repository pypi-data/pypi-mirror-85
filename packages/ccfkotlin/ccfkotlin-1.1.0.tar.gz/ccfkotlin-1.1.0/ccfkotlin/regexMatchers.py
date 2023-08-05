from .l_token import *
import re


def hex_bin_number_matcher(position, text):
    min_length = 3
    cur_pos = position
    res_position = position

    if len(text) - position < min_length:
        return None

    pattern = re.compile(r"[-+]?0[xX].?")
    match_pos = pattern.search(text[position:position + min_length], position)
    if match_pos is not None and match_pos.start() == position:
        type = TokenType.HEX
    else:
        pattern = re.compile(r"[-+]?0[bB].?")
        match_pos = pattern.search(text[position:position + min_length], position)
        if match_pos is not None and match_pos.start() == position:
            type = TokenType.BIN
        else:
            return None

    hex_pattern = re.compile(r"[-+]?0[xX][0-9a-fA-F]+([eE]([-+]?[0-9]+)?)?")
    bin_pattern = re.compile(r"[-+]?0[bB][01]+([eE]([-+]?[0-9]+)?)?")
    while cur_pos < len(text):
        cur_pos += 1
        if hex_pattern.search(text[position:cur_pos], position) is not None:
            hex_match_pos, hex_stop = hex_pattern.match(text[position:cur_pos], position)
            if type == TokenType.HEX and hex_match_pos is not None and hex_match_pos.start() == position and hex_stop == cur_pos:
                res_position = cur_pos
        '''bin_match_pos, bin_stop = bin_pattern.search(text[position:cur_pos], position)
        
        if type == TokenType.BIN and bin_match_pos is not None and hex_match_pos.start() == position:
            res_position = cur_pos'''
    return Token(type, res_position, text[position:res_position]) if res_position != position else None

