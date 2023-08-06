import logging
from argparse import Namespace
from configparser import ConfigParser
from os import environ
from os.path import join
from pathlib import Path
from typing import Optional, Union

from forwarding_bot.arguments import ArgsModel, ArgParser

CONFIG_NAME = ".forwarding-bot"
SECTION_NAME = CONFIG_NAME[1:]

logger = logging.getLogger(__name__)


class DataConfig:
    """Class that provides loading of all of the config sources by priority"""

    def __init__(self):
        self.bot_token: Optional[str] = None
        self.user_token: Optional[str] = None
        self.destination_id: Optional[int] = None
        self.source_id: Optional[int] = None

    def load(
            self,
            arguments_: Union[ArgsModel, Namespace],
            local_config_: ConfigParser,
            global_config_: ConfigParser,
            environment_
    ):
        logger.debug("Load started")
        self.load_cli(arguments_)
        logger.debug("Local config")
        self.load_ini(local_config_)
        self.load_environ(environment_)
        logger.debug("Global config")
        self.load_ini(global_config_)

    def load_cli(self, arguments: Union[ArgsModel, Namespace]):
        logger.debug("Loading CLI args")

        self.bot_token = arguments.bot_token
        self.user_token = arguments.user_token
        self.destination_id = arguments.destination_id
        self.source_id = arguments.source_id

    def load_ini(self, config_: ConfigParser):
        logger.debug("Loading ini config")

        if SECTION_NAME not in config_.sections():
            return
        config = config_[SECTION_NAME]

        if not self.bot_token and config.get("BOT_TOKEN"):
            self.bot_token = config["BOT_TOKEN"]

        if not self.user_token and config.get("USER_TOKEN"):
            self.user_token = config["USER_TOKEN"]

        if not self.destination_id and config.get("DESTINATION_ID"):
            self.destination_id = config.getint("DESTINATION_ID")

        if not self.source_id and config.get("SOURCE_ID"):
            self.source_id = config.getint("SOURCE_ID")

    def load_environ(self, environment):
        logger.debug("Loading environ")

        if self.bot_token is None:
            self.bot_token = environment.get("FORWARDING_BOT_BOT_TOKEN")

        if self.user_token is None:
            self.user_token = environment.get("FORWARDING_BOT_USER_TOKEN")

        if self.destination_id is None:
            self.destination_id = int(environment.get("FORWARDING_BOT_DESTINATION_ID", 0))

        if self.source_id is None:
            self.source_id = int(environment.get("FORWARDING_BOT_SOURCE_ID", 0))

    def __repr__(self):
        return f"<{self.__class__.__name__}" \
               f"({', '.join([f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')])})>"


# cli
arg_parser = ArgParser()
# local ini
local_config = ConfigParser()
local_config.read(CONFIG_NAME)
# global ini
global_config = ConfigParser()
global_config.read(join(str(Path.home()), CONFIG_NAME))

data_config = DataConfig()
data_config.load(arguments_=arg_parser.get_args(),
                 local_config_=local_config,
                 environment_=environ,
                 global_config_=global_config)

# logger.info(f"DataConfig is {data_config}")
