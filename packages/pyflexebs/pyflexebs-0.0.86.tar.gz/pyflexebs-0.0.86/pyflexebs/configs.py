"""
All configurations
"""


from pytconf import Config, ParamCreator


class ConfigAlgo(Config):
    """
    Parameters for interval monitors
    """
    interval = ParamCreator.create_int(
        default=60,
        help_string="interval to monitor",
    )
    watermark_max = ParamCreator.create_int_or_none(
        default=70,
        help_string="max watermark for disk utilization",
    )
    volume_max_size = ParamCreator.create_int(
        default=2000,
        help_string="Maximum disk size beyond which never extend",
    )
    # watermark_min = ParamCreator.create_int_or_none(
    #    default=None,
    #    help_string="min watermark for disk utilization",
    # )
    disregard = ParamCreator.create_list_str(
        default=["/"],
        help_string="what mount points to disregard",
    )
    file_systems = ParamCreator.create_list_str(
        default=["ext4", "xfs"],
        help_string="what file systems to check",
    )
    increase_percent = ParamCreator.create_int(
        default=50,
        help_string="By how much to increase (in percentiles)",
    )
    increase_max_gb = ParamCreator.create_int(
        default=100,
        help_string="never increase by more than (in GB)",
    )
    dryrun = ParamCreator.create_bool(
        default=False,
        help_string="Should we dry run the actual operations?",
    )


class ConfigProxy(Config):
    """
    Configure proxy settings for the daemon
    """
    no_proxy = ParamCreator.create_str_or_none(
        default="localhost,169.254.169.254",
        help_string="what addresses to exempt from proxy",
    )
    http_proxy = ParamCreator.create_str_or_none(
        default=None,
        help_string="http proxy",
    )
    https_proxy = ParamCreator.create_str_or_none(
        default=None,
        help_string="https proxy",
    )


class ConfigControl(Config):
    """
    Configure control of the daemon
    """
    daemonize = ParamCreator.create_bool(
        default=False,
        help_string="Should we daemonize?",
    )
    check_root = ParamCreator.create_bool(
        default=True,
        help_string="Should we check that we are running as root?",
    )
    check_tools = ParamCreator.create_bool(
        default=True,
        help_string="Should we check that we have the right tools?",
    )
    configure_proxy = ParamCreator.create_bool(
        default=True,
        help_string="Should we configure the proxy?",
    )
    configure_logging_syslog = ParamCreator.create_bool(
        default=True,
        help_string="Should I configure syslog logging?",
    )
    uninstall_does_kill = ParamCreator.create_bool(
        default=True,
        help_string="Should I kill the service when un-installing it?",
    )
    install_does_run = ParamCreator.create_bool(
        default=False,
        help_string="Should I run the service when installing it?",
    )
    loglevel = ParamCreator.create_str(
        default="INFO",
        help_string="A which log level will the daemon work? (not the command line tool)",
    )
