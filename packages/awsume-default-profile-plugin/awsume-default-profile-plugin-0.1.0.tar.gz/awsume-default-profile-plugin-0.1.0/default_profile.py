import argparse
import os
import sys

from awsume.awsumepy import hookimpl
from awsume.awsumepy.lib.logger import logger

ENV_KEY = "AWSUME_DEFAULT_PROFILE"
CONFIG_KEY = "default-profile"


@hookimpl
def post_add_arguments(
    config: dict, arguments: argparse.Namespace, parser: argparse.ArgumentParser
):
    logger.debug("Default Profile Plugin is active")
    if not arguments.profile_name and not arguments.role_arn:
        if os.environ.get(ENV_KEY):
            logger.debug("Setting default profile from environment variable")
            arguments.target_profile_name = os.environ[ENV_KEY]
        elif config.get(CONFIG_KEY):
            logger.debug("Setting default profile from config file")
            arguments.target_profile_name = config[CONFIG_KEY]
        else:
            logger.debug(
                'No default profile setting, falling back to target profile "default"'
            )
            arguments.target_profile_name = "default"
    else:
        logger.debug("Profile or role arn specified, skipping default profile settings")
