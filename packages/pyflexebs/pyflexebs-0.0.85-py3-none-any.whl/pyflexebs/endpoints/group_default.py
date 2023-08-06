"""
The default group of operations that pyflexebs has
"""
import os
import subprocess
import sys
import time

import bitmath
import boto3
import ec2_metadata
import psutil as psutil
import pylogconf.core
from daemon import daemon
from hurry.filesize import size
from pylogconf.core import create_pylogconf_file
from pytconf import register_endpoint, register_function_group, write_config_file_json_user, \
    write_config_file_json_system, rm_config_file_json_system, rm_config_file_json_user

import pyflexebs
import pyflexebs.version
from pyflexebs.configs import ConfigAlgo, ConfigProxy, ConfigControl

from pyflexebs.utils import run_with_logger, get_logger, check_root, configure_proxy, check_tools, dump

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pyflexebs commands"

TAG_DONT_RESIZE = "dont_resize"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pyflexebs.version.VERSION_STR)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigAlgo, ConfigProxy, ConfigControl],
)
def daemon_run() -> None:
    """
    Run daemon and monitor disk utilization
    """
    if ConfigControl.daemonize:
        with daemon.DaemonContext():
            run()
    else:
        run()


def run():
    if ConfigControl.configure_logging_syslog:
        pylogconf.core.remove_all_root_handlers()
        pylogconf.core.setup_syslog(
            name=pyflexebs.LOGGER_NAME,
            level=ConfigControl.loglevel,
        )
    logger = get_logger()
    logger.info("starting")
    if ConfigControl.configure_proxy:
        configure_proxy()
    if ConfigControl.check_tools:
        check_tools()
    if ConfigControl.check_root:
        check_root()
    metadata = ec2_metadata.ec2_metadata
    instance_id = metadata.instance_id
    ec2_resource = boto3.resource('ec2', region_name=metadata.region)
    instance = ec2_resource.Instance(instance_id)
    tags = instance.tags
    ec2_client = boto3.client('ec2', region_name=metadata.region)
    volumes = instance.volumes.all()
    device_to_volume = dict()
    for volume in volumes:
        for a in volume.attachments:
            device = normalize_device(a["Device"])
            device_to_volume[device] = volume
    while True:
        logger.info("checking disk utilization")
        for p in psutil.disk_partitions():
            if p.mountpoint in ConfigAlgo.disregard:
                continue
            if p.fstype not in ConfigAlgo.file_systems:
                continue
            if TAG_DONT_RESIZE in tags:
                continue
            logger.info("checking {} {} {}".format(
                p.device,
                p.mountpoint,
                p.fstype,
            ))
            if ConfigAlgo.watermark_max is not None:
                if psutil.disk_usage(p.mountpoint).percent >= ConfigAlgo.watermark_max:
                    logger.info("max watermark detected at disk {} mountpoint {}".format(
                        p.device,
                        p.mountpoint,
                    ))
                    logger.info("percent is {}, total is {}, used is {}".format(
                        psutil.disk_usage(p.mountpoint).percent,
                        psutil.disk_usage(p.mountpoint).total,
                        psutil.disk_usage(p.mountpoint).used,
                    ))
                    enlarge_volume(p, device_to_volume, ec2_client)
        time.sleep(ConfigAlgo.interval)


def normalize_device(dev: str) -> str:
    """
    turns /dev/sdb to /dev/xvdb (if needed)
    """
    last_part = dev.split("/")[2]
    if last_part.startswith("sd"):
        drive = last_part[2:]
        return "/dev/xvd{}".format(drive)
    return dev


def enlarge_volume(p, device_to_volume, ec2):
    logger = get_logger()
    is_lvm = subprocess.check_output("lvs | grep {} | wc -l".format(p.mountpoint[1:]), shell=True).decode().rstrip()

    if is_lvm != "0":
        cmd = "pvs | grep `lvs | grep {}  | awk '{{print $2}}'` | awk '{{print $1}}' | tail -1".format(p.mountpoint[1:])
        device = subprocess.check_output(cmd, shell=True).decode().rstrip()
        device = normalize_device(device)
    else:
        device = p.device

    if device not in device_to_volume:
        logger.error("Cannot find device [{}]. Not resizing".format(device))
        return

    volume = device_to_volume[device]
    volume_id = volume.id
    # volume_size = volume.size
    volume_size = psutil.disk_usage(p.mountpoint).total
    logger.info("total is [{}]".format(size(volume_size)))
    if int(bitmath.Byte(volume_size).to_GB()) > ConfigAlgo.volume_max_size:
        logger.info("Skipping... the device: {} is: {} and the configuration for maximum volume size is: {}".format(
            device, int(bitmath.Byte(volume_size).to_GB()), ConfigAlgo.volume_max_size))
        return
    volume_size_float = float(volume_size)
    volume_size_float /= 100
    # volume_size_float *= (100+ConfigAlgo.increase_percent)
    # new_size = int(volume_size_float)
    volume_size_float *= ConfigAlgo.increase_percent
    volume_size_int = int(volume_size_float)

    if int(bitmath.Byte(volume_size_float).to_GB()) > ConfigAlgo.increase_max_gb:
        volume_size_int = ConfigAlgo.increase_max_gb

    new_size = volume_size + volume_size_int
    if volume.size < new_size:
        logger.info("trying to increase size to [{}]".format(size(new_size)))
        # noinspection PyBroadException
        try:
            result = ec2.modify_volume(
                DryRun=ConfigAlgo.dryrun,
                VolumeId=volume_id,
                Size=int(bitmath.Byte(new_size).to_GB()),
            )
            logger.debug("Success in increasing size [{}]".format(result))
            logger.info("Success in increasing size")
        except Exception as e:
            logger.info("Failure in increasing size [{}]".format(e))
    # resize the file system
    logger.info("doing [{}] extension".format(p.fstype))
    if is_lvm != "0":
        if not ConfigAlgo.dryrun:
            run_with_logger([
                "blockdev",
                "--rereadpt",
                device,
            ], logger=logger)
            run_with_logger([
                "pvresize",
                device,
            ], logger=logger)
            run_with_logger([
                "lvextend",
                "-l",
                "+95%FREE",
                p.device,
            ], logger=logger)

    if p.fstype == "ext4":
        if not ConfigAlgo.dryrun:
            run_with_logger([
                "resize2fs",
                p.device,
            ], logger=logger)
    if p.fstype == "xfs":
        if not ConfigAlgo.dryrun:
            run_with_logger([
                "xfs_growfs",
                "-d",
                p.mountpoint,
            ], logger=logger)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigAlgo, ConfigProxy],
)
def show_volumes() -> None:
    """
    Show volume information
    """
    logger = get_logger()
    configure_proxy()
    metadata = ec2_metadata.ec2_metadata
    # check that we have attached an IAM role to the machine
    # we need this for credentials
    if metadata.iam_info is None:
        logger.error("No IAM role attached to instance. Please fix instance configuration.")
        return
    logger.info("Found iam_info, good...")
    instance_id = metadata.instance_id
    session = boto3.session.Session(region_name=metadata.region)
    ec2 = session.resource('ec2')
    instance = ec2.Instance(instance_id)
    logger.info("instance is [{}]".format(instance_id))
    volumes = instance.volumes.all()
    for v in volumes:
        dump(v)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def create_pylogconf() -> None:
    """
    create a pylogconf configuration file
    """
    create_pylogconf_file()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigProxy],
)
def show_policies() -> None:
    """
    Show policies that are configured for your role
    """
    logger = get_logger()
    configure_proxy()
    metadata = ec2_metadata.ec2_metadata
    # check that we have attached an IAM role to the machine
    # we need this for credentials
    if metadata.iam_info is None:
        logger.error("No IAM role attached to instance. Please fix instance configuration.")
        return
    logger.info("Found iam_info, good...")
    logger.info("found [{}]".format(metadata.iam_info))
    instance_profile_arn = metadata.iam_info["InstanceProfileArn"]
    logger.info("instance_profile_arn [{}]".format(instance_profile_arn))
    name = instance_profile_arn.split("/")[1]
    logger.info("name [{}]".format(name))
    session = boto3.session.Session(region_name=metadata.region)
    iam = session.client('iam')
    policy_list = iam.list_attached_role_policies(RoleName=name)
    for policy in policy_list["AttachedPolicies"]:
        policy_name = policy["PolicyName"]
        policy_arn = policy["PolicyArn"]
        logger.info("policy_name: [{}]".format(policy_name))
        logger.info("policy_arn: [{}]".format(policy_arn))


SYSTEMD_FOLDER = "/lib/systemd/system"
SERVICE_NAME = "pyflexebs.service"
UNIT_FILE = "/lib/systemd/system/{}".format(SERVICE_NAME)

CONTENT = """[Unit]
Description=pyflexebs service
After=multi-user.target

[Service]
Type=simple
ExecStart={} daemon_run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigControl],
)
def service_install() -> None:
    """
    Install the service on the current machine
    """
    check_root()
    assert os.path.isdir(SYSTEMD_FOLDER), "systemd folder does not exist. What kind of linux is this?"
    assert not os.path.isfile(UNIT_FILE), "you already have the service installed"
    abs_path_to_program = sys.argv[0]
    if not os.path.isabs(abs_path_to_program):
        abs_path_to_program = os.path.join(os.getcwd(), abs_path_to_program)
    prev_mask = os.umask(0o000)
    with os.fdopen(os.open(UNIT_FILE, os.O_WRONLY | os.O_CREAT, 0o644), 'wt') as f:
        f.write(CONTENT.format(abs_path_to_program))
    os.umask(prev_mask)
    subprocess.check_call([
        "systemctl",
        "daemon-reload",
    ])
    subprocess.check_call([
        "systemctl",
        "enable",
        SERVICE_NAME,
    ])
    if ConfigControl.install_does_run:
        subprocess.check_call([
            "systemctl",
            "start",
            SERVICE_NAME,
        ])
    write_config_file_json_system()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigControl],
)
def service_uninstall() -> None:
    """
    Uninstall the service from the current machine
    """
    check_root()
    assert os.path.isdir(SYSTEMD_FOLDER), "systemd folder does not exist. What kind of linux is this?"
    assert os.path.isfile(UNIT_FILE), "you dont have the service installed"
    if ConfigControl.uninstall_does_kill:
        subprocess.check_call([
            "systemctl",
            "stop",
            SERVICE_NAME,
        ])
    subprocess.check_call([
        "systemctl",
        "disable",
        SERVICE_NAME,
    ])
    os.unlink(UNIT_FILE)
    subprocess.check_call([
        "systemctl",
        "daemon-reload",
    ])
    rm_config_file_json_system()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def service_start() -> None:
    """
    Start the service
    """
    check_root()
    subprocess.check_call([
        "systemctl",
        "start",
        SERVICE_NAME,
    ])


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def service_stop() -> None:
    """
    Stop the service
    """
    check_root()
    subprocess.check_call([
        "systemctl",
        "stop",
        SERVICE_NAME,
    ])


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[],
)
def write_config_json_user() -> None:
    """
    Write user configuration file
    """
    write_config_file_json_user()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[],
)
def write_config_json_system() -> None:
    """
    Write system configuration file
    """
    write_config_file_json_system()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[],
)
def rm_config_json_user() -> None:
    """
    Remove user configuration file
    """
    rm_config_file_json_user()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[],
)
def rm_config_json_system() -> None:
    """
    Remove system configuration file
    """
    rm_config_file_json_system()
