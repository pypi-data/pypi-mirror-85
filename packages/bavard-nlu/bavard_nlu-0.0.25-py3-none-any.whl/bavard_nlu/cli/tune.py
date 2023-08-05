import json

from bavard_nlu.tuner import NLUModelTuner, HyperNLUModelFactory


def tune(
    *,
    agent_data_file: str,
    max_trials: int,
    strategy: str = "random",
    auto: bool = False,
    test_ratio: float = None,
    nfolds: int = None,
    repeat: int = 0,
    **nlu_model_args
):
    """
    Parameters
    ----------
    agent_data_file : str
        Path to the agent data file to evaluate on.
    max_trials : int
        The maximum number of trials to run the hyperparameter optimization for.
    strategy : str, optional.
        The hyperparameter tuning strategy to use. One of `{"random", "bayesian"}`.
    auto : bool, optional
        Whether to have hyperparameters be automatically determined.
    test_ratio : float, optional
        The percentage of the dataset to use as a test set, if evaluating
        via a train/test split.
    nfolds : int, optional
        The number of folds to do, if evaluating via k-fold cross validation.
    repeat : int, optional
        If > 0, the evaluation will be performed `repeat` times and results will be
        averaged. This is useful when you want to average out the variance caused by
        random weight initialization, etc.
    **nlu_model_args : optional
        Any control parameters or hyperparameters to pass to NLUModel
        constructor. If `auto==True`, some of these values may be
        overridden.
    """
    with open(agent_data_file) as f:
        nlu_data = json.load(f)["nluData"]

    hypermodel = HyperNLUModelFactory(nlu_data=nlu_data, max_seq_len=200, **nlu_model_args)
    tuner = NLUModelTuner(hypermodel, strategy, max_trials=max_trials)
    tuner.search(auto=auto, test_ratio=test_ratio, nfolds=nfolds, repeat=repeat)

    print("Tuning Results:")
    tuner.results_summary()

    best_hps, = tuner.get_best_hyperparameters()
    print("Best hyperparameters found:")
    print(best_hps.values)
