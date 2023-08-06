from .Mosaic import Mosaic
from pandas import DataFrame, Series
from ravenclaw import is_numeric
from nightingale.feature_importance import get_model_influence
import warnings


class Xy(Mosaic):
	def __init__(self, data, x_columns, y_column, id_columns=None, row_groups=None):
		"""
		:type data: DataFrame
		:type x_columns: list[str]
		:type y_column: str
		:type id_columns: list[str] or NoneType
		:type row_groups: dict[str, list[int]]
		"""
		if isinstance(x_columns, str):
			x_columns = [x_columns]

		if isinstance(y_column, list) and len(y_column) == 1:
			y_column = y_column[0]

		if isinstance(id_columns, str):
			id_columns = [id_columns]

		if id_columns is None:
			column_groups = {'X': x_columns, 'y': [y_column]}
		else:
			column_groups = {'id': id_columns, 'X': x_columns, 'y': [y_column]}
		super().__init__(data=data, column_groups=column_groups, row_groups=row_groups)

	def drop(self, column_groups=None, row_groups=None):
		"""
		:rtype: Xy
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
			x_columns=new_column_groups['X'].copy(),
			y_column=new_column_groups['y'][0],
			id_columns=new_column_groups.get('id', None),
			row_groups=new_row_groups
		)

	def copy(self):
		"""
		:rtype: Xy
		"""
		return self.drop(column_groups=None, row_groups=None)

	def get(self, rows, columns):
		"""
		:rtype: Mosaic
		"""
		rows = rows or list(self._row_groups.keys())
		row_groups = {x: self._row_groups[x] for x in rows}

		if columns is None:
			return Xy(
				data=self.original_data,
				row_groups=row_groups,
				x_columns=self._column_groups['X'].copy(),
				y_column=self._column_groups['y'][0],
				id_columns=self._column_groups.get('id', None)
			)
		else:
			columns = columns or list(self._column_groups.keys())
			column_groups = {y: self._column_groups[y] for y in columns}
			return Mosaic(data=self.original_data, row_groups=row_groups, column_groups=column_groups)

	@property
	def X(self):
		"""
		:rtype: DataFrame
		"""
		return self['X'].data

	@property
	def y(self):
		"""
		:rtype: Series
		"""
		return self['y'].data.iloc[:, 0]

	@property
	def id(self):
		"""
		:rtype: DataFrame
		"""
		return self['id'].data

	def has_id(self):
		"""
		:rtype: bool
		"""
		return 'id' in self._column_groups

	@property
	def unique_ids(self):
		"""
		:rtype: DataFrame
		"""
		return self['id'].data.drop_duplicates()

	@property
	def num_uniques(self):
		"""
		:rtype: int
		"""
		if self.has_id():
			return len(self.unique_ids)
		else:
			raise RuntimeError('Xy does not have id columns')

	def has_duplicates(self):
		"""
		:rtype: bool
		"""
		return self.num_uniques < len(self.data)

	@property
	def x_columns(self):
		"""
		:rtype: list[str]
		"""
		return self._column_groups['X']

	@property
	def y_column(self):
		"""
		:rtype: str
		"""
		return self._column_groups['y'][0]

	@property
	def id_columns(self):
		"""
		:rtype: list[str]
		"""
		return self._column_groups.get('id', [])

	def get_column_type(self, column):
		"""
		:type column: str
		:rtype: str
		"""
		if is_numeric(self.data[column]):
			return 'numeric'
		else:
			return 'categorical'

	def get_x_column_formula(self, column):
		"""
		:rtype x_column: str
		:rtype: str
		"""
		return f'C({column})' if self.get_column_type(column=column) == 'categorical' else column

	def get_influence(self, model, use_probability, x_columns=None, num_points=500, num_threads=1, echo=1):
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			return get_model_influence(
				model=model, data=self.X, x_columns=x_columns or self.x_columns,
				use_probability=use_probability,
				num_points=num_points,
				num_threads=num_threads, echo=echo
			)
