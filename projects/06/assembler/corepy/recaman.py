import sys
from itertools import count, islice

def sequence():
	"""generate recaman's sequence"""
	seen = set()
	a = 0
	for n in count(1):
		yield a
		seen.add(a)
		c = a - n
		if c < 0 or c in seen:
			c = a + n
		a = c

def write_sequence_old(filename, num):
	"""Write Recaman's sequence to a text file."""
	f = open(filename, mode='wt', encoding='utf-8')
	f.writelines(f"{r}\n" 
		for r in islice(sequence(), num + 1))
	f.close()

# close is not required in the below because the with statement calls close for us.
def write_sequence(filename, num):
	with open(filename, mode='wt', encoding='utf-8') as f:
		f.writelines(f"{r}\n" 
			for r in islice(sequence(), num + 1))

if __name__ == '__main__':
	write_sequence(filename=sys.argv[1], num=int(sys.argv[2]))

