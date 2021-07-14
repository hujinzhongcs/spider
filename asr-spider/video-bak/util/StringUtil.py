import string
import re


def is_all_eng(input_string):
    for ch in input_string:
        if ch not in string.ascii_letters and ch not in ['\'']:
            return False
    return True


def is_tail_eng(input_string):
    if input_string == '':
        return False
    return input_string[-1] in string.ascii_letters or input_string[-1] in ['\'']


def is_head_eng(input_string):
    if input_string == '':
        return False
    return input_string[0] in string.ascii_letters or input_string[0] in ['\'']


def count_head_num(input_string):
    search_res = re.search(r'^\d+', input_string)
    if search_res:
        return search_res.end() - search_res.start()
    else:
        return 0


def count_tail_num(input_string):
    search_res = re.search(r'\d+$', input_string)
    if search_res:
        return search_res.end() - search_res.start()
    else:
        return 0


def find_num(input_string):
    search_res = re.search(r'\d+', input_string)
    if search_res:
        return search_res.start()
    else:
        return -1


def is_all_chn(input_string):
    for ch in input_string:
        ch_ord = ord(ch)
        if not ((0x4E00 <= ch_ord <= 0x9FFF) or
                (0x3400 <= ch_ord <= 0x4DBF) or
                (0x20000 <= ch_ord <= 0x2A6DF) or
                (0x2A700 <= ch_ord <= 0x2B73F) or
                (0x2B740 <= ch_ord <= 0x2B81F) or
                (0x2B820 <= ch_ord <= 0x2CEAF) or
                (0xF900 <= ch_ord <= 0xFAFF) or
                (0x2F800 <= ch_ord <= 0x2FA1F)
            ):
            return False
    return True


def find_same_sides(str1, str2, keychar = ''):
    head = find_same_head(str1, str2, keychar)
    # tail = find_same_tail(str1[len(head):], str2[len(head):], keychar)
    tail = find_same_tail(str1, str2, keychar)
    return head, tail


def find_same_head(str1, str2, keychar = ''):
    if keychar == '':
        i_head = 0
        while i_head < min(len(str1), len(str2)):
            if str1[i_head] != str2[i_head]:
                break
            i_head += 1
        if i_head > 0:
            head = str1[:i_head]
        else:
            head = ''
    else:
        i_head = 0
        last_i_head = 0
        str1 += keychar
        str2 += keychar
        while 0 <= i_head < min(len(str1), len(str2)):
            if str1[last_i_head:i_head] != str2[last_i_head:i_head]:
                break
            last_i_head = i_head
            i_head_1 = str1.find(keychar, last_i_head + 1)
            i_head_2 = str2.find(keychar, last_i_head + 1)
            if i_head_1 == i_head_2:
                i_head = i_head_1
            else:
                break
        if last_i_head > 0:
            head = str1[:last_i_head + 1]
        else:
            head = ''
    return head


def find_same_tail(str1, str2, keychar=''):
    str1_rvs = str1[::-1]
    str2_rvs = str2[::-1]

    tail_rvs = find_same_head(str1_rvs, str2_rvs, keychar)
    tail = tail_rvs[::-1]
    return tail


if __name__ == '__main__':
    print(find_same_sides('aaabbccdeff', 'aabbccdeff'))
    print(find_same_sides('aaa bbccde f', 'aab bccdef f', ' '))
    print(find_same_sides('asdf', 'asdf', ' '))
