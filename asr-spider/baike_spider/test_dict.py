dict1 = {'1': 'a', '2': 'b', '3': 'c'}
dict2=dict1.copy()
print(id(dict1))
print(id(dict2))
def test_dict(dic):
    dic['1'] = 'd'
    print(dic)
    print(id(dic))

test_dict(dict1)
print(dict1)
print(dict2)
print(id(dict2))