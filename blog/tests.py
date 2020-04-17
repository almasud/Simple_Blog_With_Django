from django.test import TestCase

# Create your tests here.
def even_number(x):
	for i in range(1, x):
		if i % 2 == 0:
			yield i

even_num_list = list(even_number(10))
print(even_num_list)
