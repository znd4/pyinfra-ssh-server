# SPDX-FileCopyrightText: 2024-present Zane Dufour <zane@znd4.me>
#
# SPDX-License-Identifier: MIT
import pyinfra
from pyinfra.api import deploy

@deploy("Set up mDNS")
def mdns():
    pass

@deploy("Install ssh server")
def sshd_install():
    pass

@deploy("turn off password authentication")
def sshd_password_auth():
    pass

@deploy("Add ssh key to known_hosts")
def sshd_known_hosts():
    pass
