class TransformedModel:
	def __init__(self, model, transformer):
		self._model = model
		self._transformer = transformer

	def transform(self, data):
		try:
			transformed = self._transformer.predict(data)
		except AttributeError:
			try:
				transformed = self._transformer.pred(data)
			except AttributeError:
				transformed = self._transformer.transform(data)
		return transformed

	def fit(self, data):
		self._transformer.fit(data)
		self._model.fit(self.transform(data=data))

	def predict(self, data):
		transformed = self.transform(data=data)
		try:
			prediction = self._model.predict(transformed)
		except AttributeError:
			prediction = self._model.pred(transformed)
		return prediction
