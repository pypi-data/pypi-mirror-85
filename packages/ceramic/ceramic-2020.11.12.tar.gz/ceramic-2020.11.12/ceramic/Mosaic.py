from .Tile import Tile
from pandas import DataFrame, concat


class Mosaic:
	_STATE_ATTRIBUTES_ = ['_row_groups', '_column_groups', '_original_data']

	def __init__(self, data, row_groups=None, column_groups=None):
		"""
		:type data: DataFrame
		:type row_groups: dict[str, list[int]]
		:type column_groups: dict[str, list[str]]
		"""
		if row_groups is None:
			self._row_groups = {'all_rows': list(range(len(data)))}
		else:
			self._row_groups = {
				key: [rows] if isinstance(rows, (str, int)) else rows
				for key, rows in row_groups.items()
			}

		if column_groups is None:
			self._column_groups = {'all_columns': list(data.columns)}
		else:
			self._column_groups = {
				key: [columns] if isinstance(columns, (str, int)) else columns
				for key, columns in column_groups.items()
			}

		self._original_data = data
		self._tiles = None
		self._create_tiles()

	def _create_tiles(self):
		self._tiles = {
			row_group_name: {
				column_group_name: Tile(data=self.original_data, columns=columns, rows=rows)
				for column_group_name, columns in self._column_groups.items()
			}
			for row_group_name, rows in self._row_groups.items()
		}

	def copy(self):
		"""
		:rtype: Mosaic
		"""
		return self.drop(row_groups=None, column_groups=None)

	def drop(self, row_groups=None, column_groups=None):
		"""
		:type row_groups: str or list[str] or NoneType
		:type column_groups: str or list[str] or NoneType
		:rtype: Mosaic
		"""
		new_row_groups = self._row_groups.copy()
		new_column_groups = self._column_groups.copy()

		if row_groups is not None:
			if isinstance(row_groups, str):
				row_groups = [row_groups]
			for row_group in row_groups:
				del new_row_groups[row_group]
		if column_groups is not None:
			if isinstance(column_groups, str):
				column_groups = [column_groups]
			for column_group in column_groups:
				del new_column_groups[column_group]

		return self.__class__(
			data=self.original_data,
			row_groups=new_row_groups,
			column_groups=new_column_groups
		)

	def get(self, rows, columns):
		"""
		:rtype: Mosaic
		"""
		rows = rows or list(self._row_groups.keys())
		columns = columns or list(self._column_groups.keys())

		row_groups = {x: self._row_groups[x] for x in rows}
		column_groups = {y: self._column_groups[y] for y in columns}
		return self.__class__(data=self.original_data, row_groups=row_groups, column_groups=column_groups)

	def __getstate__(self):
		return {
			name: getattr(self, name)
			for name in self._STATE_ATTRIBUTES_
		}

	def __setstate__(self, state):
		for name, value in state.items():
			setattr(self, name, value)
		self._create_tiles()

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
		return sum([list(values) for values in self._row_groups.values()], [])

	@property
	def columns(self):
		"""
		:rtype: list[str]
		"""
		return sum([list(values) for values in self._column_groups.values()], [])

	@property
	def data(self):
		"""
		:rtype: DataFrame
		"""
		return self.original_data.iloc[self.rows][self.columns]

	def represent_row(self, row_group_name, max_columns=None, max_rows=None):
		return concat(
			[
				tile.data.iloc[0:min(tile.num_rows, max_rows or tile.num_rows),0:min(tile.num_columns, max_columns or tile.num_columns)]
				for tile in self._tiles[row_group_name].values()
			],
			axis=1, keys=self._tiles[row_group_name].keys()
		)

	def represent_data(self, max_columns=None, max_rows=None):
		"""
		:type max_columns: NoneType or int
		:type max_rows: NoneType or int
		:rtype: DataFrame
		"""

		return concat(
			[
				self.represent_row(row_group_name=row_group_name, max_columns=max_columns, max_rows=max_rows)
				for row_group_name in self._tiles.keys()
			],
			axis=0, keys=self._tiles.keys()
		)

	def display(self, p=None, max_columns=None, max_rows=None):
		representation = self.represent_data(max_columns=max_columns, max_rows=max_rows)

		try:
			from IPython.core.display import display
			if isinstance(representation, dict):
				for key, value in representation.items():
					display(key, value)
			else:
				display(representation)
		except ImportError:
			if p is not None:
				p.pretty(representation)
			else:
				print(representation)

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text('Mosaic')
		else:
			self.display(p=p)

	def __getitem__(self, item):
		if isinstance(item, str) and item in self._row_groups:
			return self.get(rows=[item], columns=None)
		elif isinstance(item, str) and item in self._column_groups:
			return self.get(rows=None, columns=[item])
		elif isinstance(item, (tuple, list)) and len(item) == 2:
			if all([x in self._row_groups for x in item]):
				return self.get(rows=item, columns=None)
			elif all([y in self._column_groups for y in item]):
				return self.get(columns=item, rows=None)
			elif item[0] in self._row_groups and item[1] in self._column_groups:
				return self.get(rows=[item[0]], columns=[item[1]])
			elif item[0] in self._column_groups and item[1] in self._row_groups:
				return self.get(columns=[item[0]], rows=[item[1]])
			else:
				raise KeyError(f'{item}')
		elif isinstance(item, (tuple, list)):
			if all([x in self._row_groups for x in item]):
				return self.get(rows=item, columns=None)
			elif all([y in self._column_groups for y in item]):
				return self.get(columns=item, rows=None)
			else:
				raise KeyError(f'{item}')
		else:
			raise KeyError(f'{item}')
