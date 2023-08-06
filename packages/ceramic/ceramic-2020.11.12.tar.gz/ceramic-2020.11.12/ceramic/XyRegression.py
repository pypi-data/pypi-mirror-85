from pensieve import Pensieve
from nightingale.regression import get_regression_model
from ravenclaw.wrangling import bring_to_front
from .Xy import Xy


class XyRegression:
	def __init__(self, xy, interactions=None, groups=None, eliminate=False, regression_type='linear', echo=1):
		"""
		:type xy: Xy
		:type interactions: list[tuple[str]] or NoneType
		"""
		self._pensieve = Pensieve(graph_direction='TB')
		self.pensieve['xy'] = xy
		self.pensieve['input_groups'] = groups
		def get_groups(xy, input_groups):
			if groups:
				return groups
			elif xy.has_id() and xy.has_duplicates():
				return xy.id_columns
			else:
				return None

		self.pensieve['groups'] = get_groups
		self.pensieve['interactions'] = interactions or []
		self.pensieve['elimination'] = eliminate
		self.pensieve['regression_type'] = regression_type

		def get_formula(xy, interactions):
			"""
			:type xy: Xy
			:type interactions: list[tuple[str]] or NoneType
			:rtype: str
			"""
			y = f'{xy.y_column} ~ '
			x = ' + '.join([xy.get_x_column_formula(column=column) for column in xy.x_columns])
			formula = y + x
			for interaction in interactions:
				formula += ' + ' + '*'.join(
					[xy.get_x_column_formula(column=column) for column in interaction if column in xy.x_columns]
				)
			return formula

		self.pensieve['formula'] = get_formula

		def _get_regression_model(formula, xy, regression_type, groups, elimination):
			return get_regression_model(
				formula=formula, data=xy.data, regression_type=regression_type,
				groups=groups, eliminate=elimination, echo=echo
			)
		self.pensieve['regression_model'] = _get_regression_model

		def get_summary(regression_model):
			summary_table = regression_model.summary_table.copy()
			summary_table['model_name'] = regression_model.name

			#summary_table = bring_to_front(data=summary_table, columns=['model_name'])

			if 't' in summary_table.columns:
				summary_table = summary_table.sort_values('t')
			elif 'z' in summary_table.columns:
				summary_table = summary_table.sort_values('z')


			main_columns = ['model_name']


			return bring_to_front(data=summary_table, columns=main_columns).reset_index(drop=True)

		self.pensieve['summary'] = get_summary

	@property
	def pensieve(self):
		"""
		:rtype: Pensieve
		"""
		return self._pensieve

	@property
	def model_name(self):
		"""
		:rtype: str
		"""
		return self.pensieve['model_name']

	@property
	def summary_table(self):
		"""
		:rtype: pandas.DataFrame
		"""
		return self.pensieve['summary']

	@property
	def model(self):
		"""
		:rtype:
		"""
		return self.pensieve['regression_model']

	@property
	def formula(self):
		return self.pensieve['formula']

