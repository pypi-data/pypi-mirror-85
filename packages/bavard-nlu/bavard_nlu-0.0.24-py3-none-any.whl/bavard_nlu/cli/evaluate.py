import json

from bavard_nlu.model import NLUModel


def evaluate(
    *,
    agent_data_file: str,
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

    model = NLUModel(**nlu_model_args)
    train_performance, val_performance = model.evaluate(
        nlu_data, auto=auto, test_ratio=test_ratio, nfolds=nfolds, repeat=repeat
    )
    print("train performance:", train_performance)
    print("test performance:", val_performance)
