from random import choice

CHARS='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'

def random_string(length=10, prefix=''):
	random_length = length - len(prefix)
	if random_length <= 0:
		return prefix
	return (prefix + ''.join([choice(CHARS) for i in range(random_length)]))[0:length]

