"""doc
# deeptech.core.cli

> The command line interface for deeptech.

By using this package you will not need to write your own main for most networks. This helps reduce boilerplate code.
"""
import argparse
import os
import deeptech.core.logging as logging
from deeptech.core.config import import_config
from deeptech.core.checkpoint import init_model, load_weights
from deeptech.core.definitions import SPLIT_TRAIN, SPLIT_VAL


def _setup_logging(name, config):
    if name != "":
        name = "_" + name
    logging.set_logger(os.path.join(config.training_results_path, logging.get_timestamp() + name, "log.txt"))


def _train(config, load_checkpoint, load_model):
    """
    The main training loop.
    """
    _setup_logging(config.training_name, config)
    train_data = config.data_dataset(config=config, split=SPLIT_TRAIN).to_pytorch()
    val_data = config.data_dataset(config=config, split=SPLIT_VAL).to_pytorch()
    model = config.model_model(config=config)
    init_model(model, train_data)
    if load_model is not None:
        logging.info("Loading model: {}".format(load_model))
        load_weights(load_model, model)

    loss = config.training_loss(config=config, model=model)
    optim = config.training_optimizer(config=config, model=model, loss=loss)
    trainer = config.training_trainer(
        config=config,
        model=model,
        loss=loss,
        optim=optim,
        callbacks=config.training_callbacks,
        train_data=train_data,
        val_data=val_data
    )
    if load_checkpoint is not None:
        trainer.restore(load_checkpoint)
    trainer.fit(epochs=config.training_epochs)


__implementations__ = {"train": _train}


def set(name, function):
    """
    Set a new mode for the cli execution.

    The mode 'train' is preimplemented but can be overwritten, if a custom one is required.

    :param name: (str) The name of the mode made available to the command line.
    :param function: (str) The function to call when the mode is selected via a command line argument.
    """
    __implementations__[name] = function


def run_manual(mode, config, load_checkpoint=None, load_model=None):
    """
    Run the cli interface manually by giving a config and a state dict.

    This can be helpfull when working with notebooks, where you have no command line.

    :param mode: (str) The mode to start.
    :param config: (Config) The configuration instance that is used.
    :param load_checkpoint: (Optional[str]) If provided this checkpoint will be restored in the trainer/model.
    :param load_model: (Optional[str]) If provided this model will be loaded.
    """
    if mode in __implementations__ and __implementations__[mode] is not None:
        __implementations__[mode](config, load_checkpoint, load_model)
    else:
        raise RuntimeError(f"Unknown mode {mode}. There is no implementation for this mode set.")


def run(config_class=None):
    """
    Run the cli interface.

    Parses the command line arguments (also provides a --help parameter).

    :param config_class: (Optional[Class]) A pointer to a class definition of a config.
        If provided there is no config parameter for the command line.
        Else the config specified in the command line will be loaded and instantiated.
    """
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='The main entry point for the script.')
    parser.add_argument('--mode', type=str, required=True, help='What mode should be run, trian or test.')
    parser.add_argument('--input', type=str, required=True, help='Folder where the dataset can be found.')
    parser.add_argument('--output', type=str, required=True, help='Folder where to save the results.')
    if config_class is None:
        parser.add_argument('--config', type=str, required=True, help='Configuration to use.')
    parser.add_argument('--load_checkpoint', type=str, required=False, help='Path to the checkpoint (model, loss, optimizer, trainer state) to load.')
    parser.add_argument('--load_model', type=str, required=False, help='Path to the model weights to load.')
    parser.add_argument('--name', type=str, default="", required=False, help='Name to give the run.')
    parser.add_argument('--device', type=str, default=None, required=False, help='CUDA device id')
    args = parser.parse_args()

    # Log args for reproducibility
    logging.info(f"Arg: --mode {args.mode}")
    logging.info(f"Arg: --input {args.input}")
    logging.info(f"Arg: --output {args.output}")
    if config_class is None:
        logging.info(f"Arg: --config {args.config}")
    logging.info(f"Arg: --load_checkpoint {args.load_checkpoint}")
    logging.info(f"Arg: --load_model {args.load_model}")
    logging.info(f"Arg: --name {args.name}")
    logging.info(f"Arg: --device {args.device}")

    if args.device:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.device

    if config_class is None:
        config = import_config(args.config, args.name, args.input, args.output)
    else:
        config = config_class(args.name, args.input, args.output)
    run_manual(args.mode, config, args.load_checkpoint, args.load_model)


if __name__ == "__main__":
    run()
