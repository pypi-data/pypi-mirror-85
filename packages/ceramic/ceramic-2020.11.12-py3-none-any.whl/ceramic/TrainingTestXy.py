from .Xy import Xy
from .TransformedModel import TransformedModel


class TrainingTestXy(Xy):
	def __init__(
			self, data, x_columns, y_column, training_rows=None, test_rows=None, id_columns=None,
			training_name='training', test_name='test'
	):
		super().__init__(
			data=data, x_columns=x_columns, y_column=y_column, id_columns=id_columns,
			row_groups={training_name: training_rows, test_name: test_rows}
		)

	@property
	def training(self):
		"""
		:rtype: Xy
		"""
		return self['training']

	@property
	def test(self):
		"""
		:rtype: Xy
		"""
		return self['test']


class TransformedTrainingTestXy(TrainingTestXy):
	def __init__(
			self, data, x_columns, y_column, training_rows=None, test_rows=None, id_columns=None,
			training_name='training', test_name='test', transformer=None
	):
		self._transformer = transformer
		if isinstance(x_columns, str):
			x_columns = [x_columns]

		if isinstance(y_column, list) and len(y_column) == 1:
			y_column = y_column[0]

		if isinstance(id_columns, str):
			id_columns = [id_columns]

		if transformer is None:
			self._original_x_columns = None
			transformed_data = data
			transformed_x_columns = x_columns
			self._original_training_test = None

		else:
			self._original_x_columns = x_columns.copy()
			self._original_training_test = TrainingTestXy(
				data=data, x_columns=x_columns, y_column=y_column, training_rows=training_rows, test_rows=test_rows,
				id_columns=id_columns, training_name=training_name, test_name=test_name

			)
			self._transformer.fit(self._original_training_test[training_name].X)
			transformed_data = self._transformer.transform(data[x_columns])
			transformed_x_columns = list(transformed_data.columns)

			if id_columns is not None:
				for id_column in id_columns:
					transformed_data[id_column] = data[id_column].values
			transformed_data[y_column] = data[y_column].values

		super().__init__(
			data=transformed_data, x_columns=transformed_x_columns, y_column=y_column,
			training_rows=training_rows, test_rows=test_rows, id_columns=id_columns,
			training_name=training_name, test_name=test_name
		)

	@property
	def transformer(self):
		return self._transformer

	def get_influence(self, model, use_probability, x_columns=None, num_points=500, num_threads=1, echo=1):
		x_columns = x_columns or self._original_x_columns

		if self.transformer is not None:
			transformed_model = TransformedModel(model=model, transformer=self.transformer)
		else:
			transformed_model = model

		return super().get_influence(
			model=transformed_model, x_columns=x_columns,
			use_probability=use_probability,
			num_points=num_points, num_threads=num_threads, echo=echo
		)
