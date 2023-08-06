from sklearn.model_selection import train_test_split, KFold
from pandas import DataFrame
from pandas import concat


def _get_id_data(data, id_columns):
	if isinstance(id_columns, str):
		id_columns = [id_columns]

	new_data = data.copy()
	new_data['_row_'] = range(len(data))

	if id_columns is None:
		new_data['_id_'] = range(len(new_data))
		id_columns = ['_id_']
	ids = new_data[id_columns].drop_duplicates()
	return new_data, id_columns, ids


def get_training_test_split_by_group(data, id_columns, test_ratio, random_state=None):
	new_data, id_columns, ids = _get_id_data(data=data, id_columns=id_columns)
	if not isinstance(ids, DataFrame):
		raise TypeError(f'ids is not DataFrame. It is {type(ids)}')

	id_training, id_test = train_test_split(ids, test_size=test_ratio, random_state=random_state)
	training = id_training.merge(new_data, how='left', on=id_columns)
	test = id_test.merge(new_data, how='left', on=id_columns)
	training_indices = training['_row_']
	test_indices = test['_row_']
	return list(training_indices), list(test_indices)

"""
def get_kfold_by_group(data, id_columns, num_splits=5, random_state=None):
	new_data, id_columns, ids = _get_id_data(data=data, id_columns=id_columns)

	kfold = KFold(n_splits=num_splits, shuffle=True, random_state=random_state)
	folds = []
	for training_index, test_index in kfold.split(ids):
		training = list(ids.iloc[training_index].merge(right=new_data, on=id_columns, how='left')['_row_'])
		test = list(ids.iloc[test_index].merge(right=new_data, on=id_columns, how='left')['_row_'])
		if len(set(training)) < len(training):
			raise RuntimeError('duplicates found!')
		fold = {'training': training, 'test': test}
		folds.append(fold)

	return folds


def get_cross_validation_by_group(data, id_columns, num_splits=5, holdout_ratio=0.2, test_ratio=None, random_state=None):
	if holdout_ratio == 0:
		return {
			'validation': list(range(len(data))), 'holdout': [],
			'folds': get_kfold_by_group(data=data, id_columns=id_columns, num_splits=num_splits, random_state=random_state)
		}

	if num_splits < 2:
		training_index, test_index = get_training_test_split_by_group(
			data=data, id_columns=id_columns, random_state=random_state,
			test_ratio=test_ratio or holdout_ratio
		)
		return {
			'validation': training_index,
			'holdout': test_index,
			'folds': []
		}

	new_data, id_columns, ids = _get_id_data(data=data, id_columns=id_columns)
	validation_index, holdout_index = get_training_test_split_by_group(
		data=new_data, id_columns=id_columns, test_ratio=holdout_ratio
	)

	validation = new_data.iloc[validation_index][id_columns]
	validation_folds = get_kfold_by_group(data=validation, num_splits=num_splits, random_state=random_state, id_columns=id_columns)

	return {
		'validation': validation_index,
		'holdout': holdout_index,
		'folds': [
			{
				'training': list(
					validation.iloc[fold['training']].merge(right=new_data, how='left', on=id_columns)['_row_']
				),
				'test': list(
					validation.iloc[fold['test']].merge(right=new_data, how='left', on=id_columns)['_row_']
				)
			}
			for fold in validation_folds
		]
	}
"""

def get_cross_validation(data, id_columns, num_splits, holdout_ratio, test_ratio=None, random_state=None):
	if id_columns is None:
		new_data = data.copy()
		id_columns = ['cross_validation_id']
		new_data['cross_validation_id'] = range(new_data.shape[0])
	else:
		if isinstance(id_columns, str):
			id_columns = [id_columns]
		new_data = data[id_columns].copy()

	new_data['cross_validation_index'] = range(new_data.shape[0])

	id_data = new_data[id_columns].drop_duplicates()

	# shuffle
	id_data = id_data.sample(frac=1, random_state=random_state)

	# reset undex
	id_data = id_data.reset_index(drop=True)

	if holdout_ratio is None or holdout_ratio == 0:
		id_holdout = None
		id_validation = id_data
	else:
		num_holdout = max(1, int(round(holdout_ratio * id_data.shape[0])))
		num_validation = id_data.shape[0] - num_holdout

		id_holdout = id_data.iloc[:num_holdout, :].reset_index(drop=True)
		id_validation = id_data.iloc[num_holdout:, :].reset_index(drop=True)

	if id_holdout is None:
		holdout_data = None
		indices_holdout = []
	else:
		holdout_data = id_holdout.merge(right=new_data, on=id_columns, how='left')
		indices_holdout = sorted(list(holdout_data['cross_validation_index']))

	validation_data = id_validation.merge(right=new_data, on=id_columns, how='left')
	indices_validation = sorted(list(validation_data['cross_validation_index']))

	validation_data = validation_data.reset_index(drop=True)
	if num_splits < 2:
		if num_splits < 1:
			test_ratio = 0
			indices_test = []
			indices_training = indices_validation

		else:
			test_ratio = test_ratio or holdout_ratio

			num_test = max(1, int(round(test_ratio * id_validation.shape[0])))
			id_test = id_validation.iloc[:num_test, :]
			id_training = id_validation.iloc[num_test:, :]

			test_data = id_test.merge(right=validation_data, on=id_columns, how='left')
			training_data = id_training.merge(right=validation_data, on=id_columns, how='left')

			indices_test = sorted(list(test_data['cross_validation_index']))
			indices_training = sorted(list(training_data['cross_validation_index']))

		folds = [{'training': indices_training, 'test': indices_test}]

	else:
		id_validation['fold_index'] = [i % num_splits for i in range(id_validation.shape[0])]
		id_split_list = [
			id_split.drop(columns='fold_index')
			for _, id_split in id_validation.groupby('fold_index')
		]
		folds = []
		for i in range(num_splits):
			id_test = id_split_list[i]
			id_training = concat([id_split_list[j] for j in range(num_splits) if j != i])

			test_data = id_test.merge(right=validation_data, on=id_columns, how='left')
			training_data = id_training.merge(right=validation_data, on=id_columns, how='left')

			indices_test = sorted(list(test_data['cross_validation_index']))
			indices_training = sorted(list(training_data['cross_validation_index']))

			folds.append({'training': indices_training, 'test': indices_test})
	return {'validation': indices_validation, 'holdout': indices_holdout, 'folds': folds}
