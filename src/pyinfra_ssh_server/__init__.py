# SPDX-FileCopyrightText: 2024-present Zane Dufour <zane@znd4.me>
#
# SPDX-License-Identifier: MIT
import io
import pyinfra
from pyinfra import host, facts, operations
import pathlib
from pyinfra.api import deploy


@deploy("Set up mDNS")
def mdns(*, hostname: str):
    operations.apt.packages(
        name="Install mDNS",
        packages=["avahi-daemon", "avahi-utils"],
        update=True,
    )
    hostname = host.data.get("hostname")
    operations.server.shell([f"hostnamectl set-hostname {hostname}"])
    operations.systemd.service("avahi-daemon", restarted=True)


@deploy("Install and configure ssh server")
def sshd(*, public_key: str = "", password_auth: bool = False):
    sshd_install()
    sshd_password_auth(enabled=password_auth)
    sshd_known_hosts(public_key=public_key)


@deploy("turn off password authentication")
def sshd_password_auth(*, enabled: bool):
    if enabled:
        line = "PasswordAuthentication no"
        replace = "PasswordAuthentication yes"
    else:
        line = "PasswordAuthentication yes"
        replace = "PasswordAuthentication no"

    operations.files.line(
        name="turn off password authentication",
        path="/etc/ssh/sshd_config",
        line=line,
        replace=replace,
    )


@deploy("Install ssh server")
def sshd_install():
    operations.apt.packages(
        name="Install ssh server",
        packages=["openssh-server"],
        update=True,
    )
    operations.systemd.service("ssh", restarted=True)


@deploy("Add ssh key to known_hosts")
def sshd_known_hosts(*, public_key: str):
    if not public_key:
        return

    operations.files.put(
        name="Add ssh key to known_hosts",
        src=io.StringIO(public_key),
        dest=pathlib.Path(host.get_fact(facts.server.Home)) / ".ssh" / "known_hosts",
    )
