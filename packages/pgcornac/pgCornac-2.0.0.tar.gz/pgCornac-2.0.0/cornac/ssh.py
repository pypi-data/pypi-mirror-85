import errno
import fcntl
import logging
import os
import shlex
import socket
import subprocess
from random import randint
from time import sleep
from urllib.parse import urlparse

import tenacity

from . import FILESDIR
from .errors import RemoteCommandError


logger = logging.getLogger(__name__)


def logged_cmd(cmd, *a, **kw):
    logger.debug("Running %s", ' '.join([shlex.quote(str(i)) for i in cmd]))
    # Unpack passwords now that command is logged.
    cmd = [a.password if isinstance(a, Password) else a for a in cmd]
    child = subprocess.Popen(
        cmd, *a, **kw,
        encoding='utf-8',
        stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
    )

    fullout = []
    fullerr = []
    for out, err in icommunicate(child):
        if out:
            fullout.append(out)
        if err:
            logger.debug("<<< %s", err.rstrip())
            fullerr.append(err)

    out = ''.join(fullout)
    err = ''.join(fullerr)

    if child.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=child.returncode,
            cmd=cmd,
            output=out,
            stderr=err,
        )

    return out


remote_retry = tenacity.retry(
    wait=tenacity.wait_chain(*[
        tenacity.wait_fixed(15)
    ] + [
        tenacity.wait_fixed(3)
    ] * 5 + [
        tenacity.wait_fixed(1)
    ] * 15),
    retry=(tenacity.retry_if_exception_type(RemoteCommandError) |
           tenacity.retry_if_exception_type(OSError)),
    stop=tenacity.stop_after_delay(300),
    reraise=True)


@remote_retry
def wait_machine(address, port=22):
    logger.debug("Trying %s:%s.", address, port)
    address = socket.gethostbyname(address)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))
    sock.close()


class Password(object):
    seed = randint(0, 1000)

    def __init__(self, password):
        self.password = password
        self.hash_ = hash(f"{self.seed}-{self.password}")

    def __repr__(self):
        return '<%s %x>' % (self.__class__.__name__, self.hash_)

    def __str__(self):
        return '********'


class RemoteShell(object):
    ssh_config = str(FILESDIR / 'ssh_config')
    ssh_options = ["-F", ssh_config]

    @classmethod
    def from_url(cls, url):
        data = urlparse(url)
        return cls(data.username, data.hostname, data.port or 22)

    def __init__(self, user, host, port=22):
        self.ssh = [
            "ssh", "-q",
            *self.ssh_options,
            "-l", user,
            "-p", str(port),
            host,
        ]
        self.scp_target_prefix = f"{user}@{host}:"

    def __call__(self, command, *, ssh_options=None):
        quoted_command = [
            Password(shlex.quote(i.password))
            if isinstance(i, Password) else
            shlex.quote(i)
            for i in command
        ]

        try:
            return logged_cmd(self.ssh + (ssh_options or []) + quoted_command)
        except subprocess.CalledProcessError as e:
            message = e.stderr or e.stdout
            if message:
                message = message.splitlines()[-1]
            else:
                message = "Unknown error."
            raise RemoteCommandError(
                message=message,
                exit_code=e.returncode,
                stderr=e.stderr) from None

    def copy(self, src, dst):
        try:
            return logged_cmd(
                ["scp"] + self.ssh_options +
                [src, self.scp_target_prefix + dst]
            )
        except subprocess.CalledProcessError as e:
            raise Exception(e.stderr)

    @remote_retry
    def wait(self):
        # Just ping with true to trigger SSH. This method allows Host rewrite
        # in ssh_config.
        self(["true"])


def icommunicate(child, stdin=None, min_poll_delay=0.1):
    # Iterative Popen.communicate. yields out, err tuples for each returned
    # lines of stdout or stderr;

    set_nonblocking(child.stdout)
    set_nonblocking(child.stderr)

    # For the sake of compatibility. But actually, we'll never be interactive
    # in cornac remote commands.
    if stdin:
        child.stdin.write(stdin)
    child.stdin.close()

    while child.returncode is None:
        out = readline_nb(child.stdout)
        err = readline_nb(child.stderr)

        if out or err:
            yield out, err
            # Fasten loop while we have data.
            continue

        if child.poll() is not None:
            break

        # Chill loop until we have data. This mimic a select timeout.
        sleep(min_poll_delay)


def set_nonblocking(fo):
    fl = fcntl.fcntl(fo, fcntl.F_GETFL)
    fcntl.fcntl(fo, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def readline_nb(fo):
    try:
        # Replace EOF by none
        return fo.readline() or None
    except IOError as e:
        if e.errno != errno.EAGAIN:
            raise
