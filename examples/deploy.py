from pyinfra_ssh_server import sshd, mdns
from pyinfra import host
import os
import subprocess as sp

hostname = host.host_data["hostname"]
mdns(hostname=hostname)
public_key = sp.check_output(
    [
        "op",
        "read",
        f"op://private/{hostname}.local/public key",
    ],
    text=True,
).strip()
sshd(public_key=public_key, password_auth=False)
