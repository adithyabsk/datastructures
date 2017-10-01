#!/usr/bin/env python

class FixedHashMap(object):
	class HashItem(object):
		__slots__ = ("key", "value")
		def __init__(self, key=None, value=None):
			self.key = key
			self.value = value
		def clear(self):
			self.key = None
			self.value = None
		def __nonzero__(self):
			return False if self.key == None else True
		def __repr__(self):
			return 'None' if self.key == None else '{}: {}'.format(self.key, self.value)

	__slots__ = ("capacity", "size", "data")

	def __init__(self, capacity=1000):
		self.capacity = capacity
		self.size = 0
		self.data = [self.HashItem() for _ in range(self.capacity)]

	def _find_slot(self, key):
		i = hash(key) % self.capacity
		while self.data[i] and (self.data[i].key != key):
			i = (i+1) % self.capacity
		return i

	def set(self, key, value):
		if not isinstance(key, str):
			raise Exception("KeyError: Key must be string")
			return
		if self.size == self.capacity:
			raise Exception("MemoryError: The hash map is full")
			return
		i = self._find_slot(key)
		if self.data[i]:
			self.data[i].value = value
		else:
			self.data[i].key = key
			self.data[i].value = value
			self.size+=1

	def get(self, key):
		i = self._find_slot(key)
		if self.data[i]:
			return self.data[i].value
		else:
			raise Exception("KeyError: Could not find key: {}".format(key))
			return

	def delete(self, key):
		i = self._find_slot(key)
		if not self.data[i]:
			raise Exception("KeyError: Could not find key: {}".format(key))
			return
		j = i
		break_main = False

		# Prevent gaps between data points
		while True:
			self.data[i].clear()
			while True:
				j = (j+1) % self.capacity
				if not self.data[j]:
					break_main = True
					break

				k = hash(self.data[j].key) % self.capacity
				# Check if k is cyclically in between i and j
				if not ((i<k and k<=j) if (i <= j) else (i<k or k<=j)):
					break

			if break_main:
				break

			self.data[i] = self.data[j]
			i = j

		self.size-=1

	def load(self):
		return float(self.size) / float(self.capacity)

	def keys(self):
		return [i.key for i in self.data if i]

	def __setitem__(self, key, value):
		self.set(key, value)

	def __getitem__(self, key):
		return self.get(key)

	def __delitem__(self, key):
		return self.delete(key)

	def __repr__(self):
		data = [(k, str(self.get(k))) for k in self.keys()]
		return '{}' if not data else '{'+', '.join('{}: {}'.format(repr(k), v) for k,v in data)+'}'


if __name__ == "__main__":
	def print_stats(h):
		print 'fhm.load: {}'.format(fhm.load())
		print 'fhm: {}'.format(fhm)
		print ''

	test_size = 2
	fhm = FixedHashMap(test_size)
	print 'Initialize Hash map of size {}\n'.format(test_size)
	for i in range(test_size+1):
		print 'Try to add (\'{}\': {})'.format(str(i), i+1)
		try: fhm[str(i)] = i+1
		except Exception as e: print e
		print_stats(fhm)

	print "\n\n"

	for i in range(test_size+1):
		print 'Try to delete key \'{}\''.format(str(i))
		try: del fhm[str(i)]
		except Exception as e: print e
		print_stats(fhm)