from bavard_nlu.model import NLUModel


def predict(
    *,
    model_path: str,
    batch_file: str = None,
    interactive: bool = False
):
    """
    Parameters
    ----------
    model_path : str
        Path to the saved model that will be loaded.
    batch_file : str, optional
        Pass this file path to predict on a file of text; one prediction per line.
    interactive : bool, optional
        If supplied, interact with the model, providing inputs for prediction via CLI.
    """
    model = NLUModel.from_dir(model_path)
    if batch_file:
        with open(batch_file) as f:
            utterances = [utterance.replace("\n", "") for utterance in f]
        print(model.predict(utterances))
    
    if interactive:
        quits = {"q", "quit", "exit"}
        utterance = ""
        while True:
            utterance = input("\nEnter your utterance ('q' to quit) >>> ")
            if utterance in quits:
                break
            print(model.predict([utterance]))
