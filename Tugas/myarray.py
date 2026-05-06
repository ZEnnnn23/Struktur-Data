class Array:
    def __init__(self, size):
        self._data = [None] * size
        self._size = size

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        assert 0 <= index < self._size
        return self._data[index]

    def __setitem__(self, index, value):
        assert 0 <= index < self._size
        self._data[index] = value
