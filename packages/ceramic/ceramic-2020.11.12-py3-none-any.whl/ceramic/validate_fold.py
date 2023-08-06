import warnings
from copy import deepcopy


def validate_fold(model_fold, shared_memory, evaluation_function):
	"""
	:type model_fold: dict
	:type shared_memory: dict
	:type evaluation_function: callable
	:rtype: DataFrame
	"""
	score_board = shared_memory['score_board']
	main_metric = shared_memory['main_metric']
	best_model_criteria = shared_memory['best_model_criteria']
	model_name = model_fold['model_name']

	if len(score_board) == 0:
		shared_memory['progress_bar'].show(amount=shared_memory['progress_amount'], text=f'validating {model_name}')

	else:
		new_board = {name: sum(performances)/len(performances) for name, performances in score_board.items()}
		if best_model_criteria == 'highest':
			new_board = [(k, v) for k, v in sorted(new_board.items(), key=lambda item: -item[1])]
		else:
			new_board = [(k, v) for k, v in sorted(new_board.items(), key=lambda item: item[1])]

		if len(new_board) >= 2:
			best_model_name = new_board[0][0]
			best_score = new_board[0][1]
			second_model_name = new_board[1][0]

			score_text = f'1st: {best_model_name} [{main_metric}:{round(best_score, 2)}], 2nd: {second_model_name} - validating {model_name}'
		elif len(new_board) == 1:
			best_model_name = new_board[0][0]
			best_score = new_board[0][1]
			score_text = f'1st: {best_model_name} [{main_metric}:{round(best_score, 2)}] - validating {model_name}'

		shared_memory['progress_bar'].show(amount=shared_memory['progress_amount'], text=score_text)

	with warnings.catch_warnings():
		warnings.simplefilter('ignore')

		this_model = deepcopy(model_fold['model'])
		fold = model_fold['fold']
		fold_num = model_fold['fold_num']

		try:
			this_model.fit(X=fold.training.X, y=fold.training.y)
		except Exception as e:
			print(f'error validation fold with model:"{model_name}"')
			print(list(fold.training.y)[0:10])
			print(fold.training.y.dtype)
			print('\n'*10)
			print(fold.data.head())

			raise e
		training_evaluation = evaluation_function(this_model.predict(fold.training.X), fold.training.y)
		test_evaluation = evaluation_function(this_model.predict(fold.test.X), fold.test.y)

		if main_metric is not None and main_metric in test_evaluation:
			performance = test_evaluation[main_metric]
			if model_name in score_board:
				score_board[model_name].append(performance)
			else:
				score_board[model_name] = [performance]

	shared_memory['progress_amount'] += 1
	return {
		'model': this_model,
		'model_name': model_name,
		'fold_num': fold_num,
		'training_evaluation': training_evaluation,
		'test_evaluation': test_evaluation
	}