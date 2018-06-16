from typing import Any, List, Dict, Union, Tuple, TextIO


def load(fh: TextIO) -> Union[Dict[str, Any], List[Any]]:
    return loads(fh.read())


def loads(json: str) -> Union[Dict[str, Any], List[Any]]:
    length = len(json)
    num = 0
    num = _move_to_next_node(json, num, length)
    if num < length:
        end = _find_matching_end(json, num, length)
        if json[num] == '{':
            return _read_dictionary(json, num, end)[0]
        elif json[num] == '[':
            return _read_list(json, num, end)[0]


def _move_to_next_node(json: str, begin: int, end: int) -> int:
    flag = False
    for i in range(begin, end):
        c = json[i]
        if c == '"' and i > 0 and json[i - 1] != '"':
            flag = not flag
        if not flag:
            if c == '{' or c == '[':
                return i
    return end


def _find_matching_end(json: str, begin: int, end: int) -> int:
    num = 0
    flag = False
    for i in range(begin, end):
        c = json[i]
        if i == 0 or json[i - 1] != '\\':
            if c == '"':
                flag = not flag
            elif c == '{' or c == '[':
                num += 1
            elif c == '}' or c == ']':
                num -= 1
                if num == 0:
                    return i
    return end


def _read_dictionary(
        json: str,
        begin: int,
        end: int
) -> Tuple[Dict[str, Any], int]:
    dictionary = {}
    num = 1
    flag = False
    text = '\r\n\t ?"\'\\,:{}[]'
    text2 = r''
    text3 = r''
    i = begin + 1
    while i < end:
        flag2 = False
        c = json[i]
        if i == 0 or json[i - 1] != '\\':
            if c == '"':
                flag = not flag
            if not flag:
                if num != 1 and c == ',':
                    text3 = _trim_property_value(text3)
                    if len(text2) > 0 and text2 not in dictionary and len(text3) > 0:
                        dictionary[text2] = _json_decode(text3)
                    num = 1
                    text2 = ''
                    text3 = ''
                    flag2 = True
                if num == 1 and c == ':':
                    num = 2
                    text3 = ''
                    flag2 = True
                if num == 2 and c == '{':
                    end2 = _find_matching_end(json, i, end)
                    dictionary[text2], i = _read_dictionary(json, i, end2)
                    text3 = ''
                    num = 0
                    flag2 = True
                if num == 2 and c == '[':
                    end3 = _find_matching_end(json, i, end)
                    dictionary[text2], i = _read_list(json, i, end3)
                    text3 = ''
                    num = 0
                    flag2 = True
        if not flag2:
            if num == 1 and c not in text:
                text2 += c
            if num == 2:
                text3 += c
        i += 1
    if len(text2) > 0 and text2 not in dictionary:
        text3 = _trim_property_value(text3)
        if len(text3) > 0:
            dictionary[text2] = _json_decode(text3)
    return dictionary, i


def _read_list(
        json: str,
        begin: int,
        end: int
) -> Tuple[List[Any], int]:
    _list = []
    flag = False
    text = ""
    i = begin + 1
    while i < end:
        flag2 = False
        c = json[i]
        if i == 0 or json[i - 1] != '\\':
            if c == '"':
                flag = not flag
            if not flag:
                if c == '{':
                    end2 = _find_matching_end(json, i, end)
                    dictionary, i = _read_dictionary(json, i, end2)
                    _list.append(dictionary)
                    text = ''
                    flag2 = True
                elif c == '[':
                    end3 = _find_matching_end(json, i, end)
                    dictionary, i = _read_list(json, i, end3)
                    _list.append(dictionary)
                    text = ''
                    flag2 = True
                elif c == ',':
                    text = _trim_property_value(text)
                    if len(text):
                        _list.append(_json_decode(text))
                    text = ''
                    flag2 = True
        if not flag2:
            text += c
        i += 1
    text = _trim_property_value(text)
    if len(text) > 0:
        _list.append(_json_decode(text))
    return _list, i


def _trim_property_value(value: str) -> str:
    value = value.strip()
    if not value:
        result = ''
    else:
        while len(value) > 1 and value[0] == '\r'\
                or value[0] == '\n' or value[0] == '\t' or value[0] == ' ':
            value = value[1:]
        while len(value) > 0 and value[-1] == '\r'\
                or value[-1] == '\n' or value[-1] == '\t' or value[-1] == ' ':
            value = value[:-1]
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            result = value[1:-1]
        else:
            result = value
    return result


def _json_decode(json_string: str) -> str:
    json_string = json_string.replace('\\/', '/')
    json_string = json_string.replace('\\n', '\n')
    json_string = json_string.replace('\\r', '\r')
    json_string = json_string.replace('\\t', '\t')
    json_string = json_string.replace('\\"', '"')
    json_string = json_string.replace('\\\\', '\\')
    return json_string
