# SPDX-FileCopyrightText: 2024-present Zane Dufour <zane@znd4.me>
#
# SPDX-License-Identifier: MIT
import io
import pyinfra
from pyinfra import host, facts, operations
import pathlib
from pyinfra.api import deploy, operation


@operation
def mdns(*, hostname: str):
    yield from operations.apt.packages(
        name="Install mDNS",
        packages=["avahi-daemon", "avahi-utils"],
        update=True,
    )
    hostname = host.data.get("hostname")
    yield from operations.server.shell([f"hostnamectl set-hostname {hostname}"])
    yield from operations.systemd.service("avahi-daemon", restarted=True)


@operation
def sshd(*, public_key: str = "", password_auth: bool = False):
    yield from sshd_install()
    yield from sshd_password_auth(enabled=password_auth)
    yield from sshd_known_hosts(public_key=public_key)


@operation
def sshd_password_auth(*, enabled: bool):
    if enabled:
        line = "PasswordAuthentication no"
        replace = "PasswordAuthentication yes"
    else:
        line = "PasswordAuthentication yes"
        replace = "PasswordAuthentication no"

    yield from operations.files.line(
        name="turn off password authentication",
        path="/etc/ssh/sshd_config",
        line=line,
        replace=replace,
    )


@operation
def sshd_install():
    yield from operations.apt.packages(
        name="Install ssh server",
        packages=["openssh-server"],
        update=True,
    )
    yield from operations.systemd.service("ssh", restarted=True)


@operation
def sshd_known_hosts(*, public_key: str):
    if not public_key:
        return

    yield from operations.files.put(
        name="Add ssh key to known_hosts",
        src=io.StringIO(public_key),
        dest=pathlib.Path(host.get_fact(facts.server.Home)) / ".ssh" / "known_hosts",
    )
