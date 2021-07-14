

with open('F:/title', 'r', encoding='utf8') as rf:
    title_dict = {}
    for line in rf:
        line = line.strip()
        items = line.split('\t')
        if len(items) != 2: continue
        word, hot = items
        hot = int(hot)
        word = word.strip()
        if word in title_dict:
            dict_hot = title_dict[word]
            if hot > dict_hot:
                title_dict[word] = hot
        else:
            title_dict[word] = hot

    for key, val in title_dict.items():
        print(key + "\t" + str(val))