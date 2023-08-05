import json

from bavard_nlu.model import NLUModel


def train(*, agent_data_file: str, auto: bool = False, **nlu_model_args):
    """
    Parameters
    ----------
    agent_data_file : str
        Path to the agent data file to train on.
    auto : bool, optional
        Whether to have hyperparameters be automatically determined.
    **nlu_model_args : optional
        Any control parameters or hyperparameters to pass to NLUModel
        constructor. If `auto==True`, some of these values may be
        overridden.
    """
    with open(agent_data_file) as f:
        nlu_data = json.load(f)["nluData"]

    model = NLUModel(**nlu_model_args)
    model.train(nlu_data, auto=auto)
