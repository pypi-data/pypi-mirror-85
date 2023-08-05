from fire import Fire

from bavard_nlu.cli.evaluate import evaluate
from bavard_nlu.cli.predict import predict
from bavard_nlu.cli.train import train
from bavard_nlu.cli.tune import tune


if __name__ == '__main__':
    Fire({
        "evaluate": evaluate,
        "predict": predict,
        "train": train,
        "tune": tune
    })
