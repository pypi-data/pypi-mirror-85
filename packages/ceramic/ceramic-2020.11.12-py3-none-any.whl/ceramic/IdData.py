class IdData:
	def __init__(self, data, id_columns):
		self._data = data[id_columns].drop_duplicates()