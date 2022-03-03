"""A hash map implementation with a fixed size."""

# TODO: Update this implementation so that you can insert None as a key


class FixedHashMap:
	class HashItem:
		__slots__ = ("key", "value", "is_tombstone")

		def __init__(self, key=None, value=None):
			self.key = key
			self.value = value
			self.is_tombstone = False

		def clear(self):
			self.key = None
			self.value = None
			self.is_tombstone = True

		def set(self, key, value):
			self.key = key
			self.value = value
			self.is_tombstone = False

		def __bool__(self):
			"""Evaluate to `False` if the key is not set."""
			return False if self.key is None else True

		def __repr__(self):
			return 'None' if self.key is None else f'{self.key}: {self.value}'

	__slots__ = ("capacity", "size", "data")

	def __init__(self, capacity=1000):
		self.capacity = capacity
		self.size = 0
		self.data = [self.HashItem() for _ in range(self.capacity)]

	def _find_slot(self, key):
		try:
			hash_idx = hash(key) % self.capacity
		except TypeError:
			raise ValueError("key must be hashable")
		count = 0
		while (
			(self.data[hash_idx] and (self.data[hash_idx].key != key))
			or self.data[hash_idx].is_tombstone
		):
			hash_idx = (hash_idx+1) % self.capacity
			count += 1
			if count >= self.size:
				raise KeyError(f"could not find key: {key}")
		return hash_idx

	def get_hash_item(self, key):
		key_idx = self._find_slot(key)
		if self.data[key_idx] is not None:
			return self.data[key_idx]
		else:
			raise KeyError(f"could not find key: {key}")

	def get(self, key):
		return self.get_hash_item(key).value

	def set(self, key, value):
		if self.size >= self.capacity:
			raise MemoryError("the hash map is full")
		hash_item = self.get_hash_item(key)
		if hash_item:
			hash_item.set(hash_item.key, value)
		else:
			hash_item.set(key, value)
			self.size += 1

	def delete(self, key):
		# use tombstone deletion
		# https://stackoverflow.com/a/60644631/3262054
		hash_item = self.get_hash_item(key)
		hash_item.clear()
		self.size -= 1

	def load(self):
		return float(self.size) / float(self.capacity)

	def keys(self):
		return [hash_item.key for hash_item in self.data if hash_item]

	def __setitem__(self, key, value):
		self.set(key, value)

	def __getitem__(self, key):
		return self.get(key)

	def __delitem__(self, key):
		return self.delete(key)

	def __repr__(self):
		data = [
			(str(k), str(self.get(k)))
			for k in self.keys()
			if k is not None
		]
		return '{}' if not data else '{'+', '.join('{}: {}'.format(repr(k), v) for k,v in data)+'}'


if __name__ == "__main__":
	def print_stats(h):
		print('fhm.load: {}'.format(fhm.load()))
		print('fhm: {}'.format(fhm))
		print('')

	test_size = 2
	fhm = FixedHashMap(test_size)
	print('Initialize Hash map of size {}\n'.format(test_size))
	for i in range(test_size+1):
		print('Try to add (\'{}\': {})'.format(str(i), i+1))
		try: fhm[str(i)] = i+1
		except Exception as e: print(e)
		print_stats(fhm)

	print("\n\n")

	for i in range(test_size+1):
		print('Try to delete key \'{}\''.format(str(i)))
		try: del fhm[str(i)]
		except Exception as e: print(e)
		print_stats(fhm)
