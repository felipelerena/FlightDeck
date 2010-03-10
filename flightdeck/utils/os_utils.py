# from http://jimmyg.org/blog/2009/working-with-python-subprocess.html#checking-a-program-is-on-the-path
import os
def whereis(program):
	for path in os.environ.get('PATH', '').split(':'):
		if os.path.exists(os.path.join(path, program)) and \
		   not os.path.isdir(os.path.join(path, program)):
			return os.path.join(path, program)
	return None

