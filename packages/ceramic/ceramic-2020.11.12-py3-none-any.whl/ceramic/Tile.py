from pandas import DataFrame


class Tile:
	def __init__(self, data, rows=None, columns=None):
		"""
		:type data: DataFrame or Tile
		:type rows: list[int] or NoneType
		:type columns: list[str] or NoneType
		"""

		self._original_data = data

		if rows is None:
			rows = list(range(len(data)))
		else:
			if max(rows) >= len(data):
				raise ValueError(f'row {max(rows)} does not exist!')
			if min(rows) < 0:
				raise ValueError(f'row {min(rows)} does not exist!')

		if columns is None:
			columns = list(data.columns)
		else:
			missing_columns = [x for x in columns if x not in data.columns]
			if len(missing_columns) > 0:
				raise KeyError(f'columns {missing_columns} are missing!')

		self._rows = rows
		self._columns = columns

	def __eq__(self, other):
		"""
		:type other: Tile
		:rtype: bool
		"""
		return self.rows == other.rows and self.columns == other.columns and self.original_data == other.original_data

	@property
	def original_data(self):
		"""
		:rtype: DataFrame
		"""
		return self._original_data

	@property
	def rows(self):
		"""
		:rtype: list[int]
		"""
		return self._rows

	@property
	def columns(self):
		"""
		:rtype: list[str]
		"""
		return self._columns

	@property
	def num_columns(self):
		"""
		:rtype: int
		"""
		return len(self.columns)

	@property
	def num_rows(self):
		"""
		:rtype: int
		"""
		return len(self.rows)

	@property
	def data(self):
		"""
		:rtype: DataFrame
		"""
		return self.original_data.iloc[self.rows][self.columns]
