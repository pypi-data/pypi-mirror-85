"""
main entry point to the program
"""
import pylogconf.core
from pytconf import register_main, config_arg_parse_and_launch

from pyflexebs import LOG_LEVEL
from pyflexebs.endpoints.group_default import register_group_default


def register_all_groups():
    """
    registers all groups of operations with pytconf
    """
    register_group_default()


@register_main()
def main():
    """
    pyflexebs will enlarge/reduce your ebs volumes in real time
    """
    pylogconf.core.setup(level=LOG_LEVEL)
    register_all_groups()
    config_arg_parse_and_launch(app_name="pyflexebs")


if __name__ == '__main__':
    main()
