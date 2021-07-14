def gen(n):
	for i in range(n):
		print(i)
		yield i**2

for i in gen(10):
	print("*",i)
