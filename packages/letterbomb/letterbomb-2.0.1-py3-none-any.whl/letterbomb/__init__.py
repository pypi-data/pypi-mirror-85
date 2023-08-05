#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""
✉️💣 **LetterBomb**: A fork of the `classic Wii hacking tool
<https://wiibrew.org/wiki/LetterBomb>`_ from `fail0verflow
<https://github.com/fail0verflow/letterbomb>`_.

::

    ██╗     ███████╗████████╗████████╗███████╗██████╗ ██████╗  ██████╗ ███╗   ███╗██████╗
    ██║     ██╔════╝╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔══██╗
    ██║     █████╗     ██║      ██║   █████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║██████╔╝
    ██║     ██╔══╝     ██║      ██║   ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗
    ███████╗███████╗   ██║      ██║   ███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝
    ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝

----

For most usage, you should be using :func:`__main__`.
For additional usage, build and view the documentation located in the `docs` folder.

If you downloaded this package from `PyPi
<https://pypi.org/project/letterbomb>`_, the `docs` folder is not included.

Obtain the latest copy of LetterBomb and build it manually from here:
https://gitlab.com/whoatemybutter/letterbomb


**Note:** *This exploit only works for System Menu 4.3. 4.2 and below will not work.*

LetterBomb is licensed under the GPLv3+ license. You can grab a copy here:
https://www.gnu.org/licenses/gpl-3.0.txt.
"""
import hashlib
import hmac
import logging
import os
import pathlib
import sys
import struct
import zipfile
from datetime import datetime
from datetime import timedelta


__copyright__: str = "GPLv3+"
__project__: str = "LetterBomb"
__version__: str = "2.0.1"
__author__: str = "WhoAteMyButter"
__url__: str = "https://gitlab.com/whoatemybutter/letterbomb"
__download__: str = (
    "https://gitlab.com/whoatemybutter/letterbomb/"
    "-/archive/master/letterbomb-master.zip"
)
__license__: str = "GPLv3+"

TEMPLATES: dict = {
    "U": "./included/templates/U.bin",
    "E": "./included/templates/E.bin",
    "J": "./included/templates/J.bin",
    "K": "./included/templates/K.bin",
}

REGION_LIST: list = ["U", "E", "K", "J"]

LOGGING_DICT: dict = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

LOGGING_LEVEL: int = logging.DEBUG
LOGGING_FILE: [str, pathlib.Path] = ""

HERE: pathlib.PurePath = pathlib.Path(__file__).parent
BUNDLEBASE: pathlib.Path = pathlib.Path(HERE / "included/bundled/")


def mac_digest(mac: str) -> bytes:
    r"""
    Process `mac` through a SHA1 encoding with '\\x75\\x79\\x79' added.

    :param str mac: MAC address to digest
    :return: SHA-1 hash of MAC, plus \\x75\\x79\\x79, then digested
    :rtype: bytes
    """
    return hashlib.sha1(mac.encode("latin-1") + b"\x75\x79\x79").digest()


def serialize_mac(mac: str) -> str:
    """
    Return `mac` as a string, each field split by a ":".

    Padded with zeros to two-lengths.

    :param str mac: MAC address
    :return: ":" split string
    :rtype: str
    """
    return ":".join(mac[i : i + 2].zfill(2) for i in range(0, len(mac), 2))


def validate_mac(mac: str, oui_list: list) -> int:
    """
    Ensure `mac` is a valid Wii MAC address.

    Returns an integer:

    +-----------+------------+---------------+-------------+
    | 0         | 1          | 2             | 3           |
    +===========+============+===============+=============+
    | Valid MAC | Bad length | Not a Wii MAC | Dolphin MAC |
    +-----------+------------+---------------+-------------+

    :param list oui_list:
    :param str mac: MAC address to validate
    :return: 0 = valid, 1 = bad length, 2 = not a wii, 3 = dolphin MAC
    :rtype: int
    """
    if len(mac) != 12:
        return 1
    if not any(mac.upper().startswith(i.upper()) for i in oui_list):
        return 2
    if mac.upper() == "0017AB999999":
        return 3
    return 0


def pack_blob(digest: bytes, timestamp: int, blob: bytearray) -> bytearray:
    """
    Pack `blob` with corresponding timestamps and the MAC `digest`.

    :param bytes digest: MAC digest
    :param int timestamp: Unix epoch time
    :param bytearray blob: Blob content
    :return: Resulting blob content
    :rtype: bytearray
    """
    blob[0x08:0x10] = digest[:8]
    blob[0xB0:0xC4] = b"\x00" * 20
    blob[0x7C:0x80] = struct.pack(">I", timestamp)
    blob[0x80:0x8A] = b"%010d" % timestamp
    blob[0xB0:0xC4] = hmac.new(digest[8:], blob, hashlib.sha1).digest()
    return blob


def sd_path(digest: bytes, deltatime: datetime, timestamp: int) -> str:
    """
    Return the path of the LetterBomb, relative to the root of the SD card.

    :param bytes digest: MAC digest, see :func:`mac_digest`
    :param datetime deltatime: Time of letter receival
    :param int timestamp: Unix epoch time
    :return: String of resulting path, relative
    :rtype: str
    """
    return (
        "private/wii/title/HAEA/"
        f"{digest[:4].hex().upper()}/"
        f"{digest[4:8].hex().upper()}/"
        "%04d/%02d/%02d/%02d/%02d/HABA_#1/txt/%08X.000"
        % (
            deltatime.year,
            deltatime.month - 1,
            deltatime.day,
            deltatime.hour,
            deltatime.minute,
            timestamp,
        )
    )


def write_zip(
    mac: str,
    region: str,
    pack_bundle: bool,
    output_file: [str, pathlib.Path],
) -> int:
    """
    Write LetterBomb archive to `output_file`, return exit code.

    Depending upon the `region`, different LetterBomb templates will be used.
    If `pack_bundle` is True, the BootMii installer will be included with the archive.

    ----

    Exit codes:

    +-------------+--------------------+------------------------+---------------------+
    | 0           | 1                  | 2                      | 3                   |
    +=============+====================+========================+=====================+
    | Success, OK | MAC was bad length | MAC was not of a Wii's | MAC is from Dolphin |
    +-------------+--------------------+------------------------+---------------------+

    :param str mac: Full string of the Wii's MAC address
    :param str region: Region of Wii, must be single letter of U,J,K,E
    :param bool pack_bundle: Pack the BootMii installer with archive
    :param str,pathlib.Path output_file: File to write archive to
    :return: Return code, 0 = success, 1 = bad length mac, 2 = bad mac, 3 = dolphin mac
    :rtype: int
    """
    deltatime: datetime.date = datetime.utcnow() - timedelta(1)
    delta: datetime.date = deltatime - datetime(2000, 1, 1)
    timestamp: int = delta.days * 86400 + delta.seconds
    if not LOGGING_FILE:
        logging.basicConfig(filename=LOGGING_FILE, level=LOGGING_LEVEL)

    if region.upper() not in REGION_LIST:
        raise ValueError(f"region must be one of {', '.join(REGION_LIST)}")

    dig: bytes = mac_digest(mac)

    with open(pathlib.Path(HERE / TEMPLATES[region]), "rb") as bin_template, open(
        pathlib.Path(HERE / "included/oui_list.txt")
    ) as oui_file:
        blob: bytearray = pack_blob(dig, timestamp, bytearray(bin_template.read()))
        oui_list: list = oui_file.read().splitlines()

    if validate_mac(mac, oui_list) == 3:
        logging.info("If you're using Dolphin, try File→Open instead")
        logging.critical(
            'Dolphin MAC "%s" on: %s, ' "region: %s, bundle: %s",
            serialize_mac(mac.upper()),
            timestamp,
            region,
            pack_bundle,
        )
        return 3

    if validate_mac(mac, oui_list) == 2:
        logging.info("The exploit will only work if you enter your Wii's MAC address")
        logging.critical(
            'Invalid MAC "%s" on: %s, ' "region: %s, bundle: %s",
            serialize_mac(mac.upper()),
            timestamp,
            region,
            pack_bundle,
        )
        return 2

    if validate_mac(mac, oui_list) == 1:
        logging.info("You must input a 12-length MAC address")
        logging.critical(
            'Bad length MAC "%s" on: %s, ' "region: %s, bundle: %s",
            serialize_mac(mac.upper()),
            timestamp,
            region,
            pack_bundle,
        )
        return 1

    with zipfile.ZipFile(pathlib.Path(output_file).expanduser(), "w") as zip_out:
        zip_out.writestr(
            sd_path(dig, deltatime, timestamp), pack_blob(dig, timestamp, blob)
        )
        if pack_bundle:
            for name, dpath in [
                (name, pathlib.Path(BUNDLEBASE / name))
                for name in os.listdir(BUNDLEBASE)
                if not name.startswith(".")
            ]:
                zip_out.write(dpath, name)
    logging.info(
        '✉💣 LetterBombed file at: "%s" with MAC "%s" on: %s, region: %s, bundle: %s',
        output_file,
        serialize_mac(mac.upper()),
        timestamp,
        region,
        pack_bundle,
    )
    return 0


def write_stream(mac: str, region: str, pack_bundle: bool) -> int:
    """
    Write LetterBomb archive as a raw bytes stream.

    This ZIP will be streamed directly to `sys.stdout`. Be careful with handling it.

    Depending upon the `region`, different LetterBomb templates will be used.
    If `pack_bundle` is True, the BootMii installer will be included with the archive.

    ----

    Exit codes:

    +-------------+--------------------+------------------------+---------------------+
    | 0           | 1                  | 2                      | 3                   |
    +=============+====================+========================+=====================+
    | Success, OK | MAC was bad length | MAC was not of a Wii's | MAC is from Dolphin |
    +-------------+--------------------+------------------------+---------------------+

    :param str mac: Full string of the Wii's MAC address
    :param str region: Region of Wii, must be single letter of U,J,K,E
    :param bool pack_bundle: Pack the BootMii installer with archive
    :return: Return code, 0 = success, 1 = bad length mac, 2 = bad mac, 3 = dolphin mac
    :rtype: int
    """
    deltatime: datetime.date = datetime.utcnow() - timedelta(1)
    delta: datetime.date = deltatime - datetime(2000, 1, 1)
    timestamp: int = delta.days * 86400 + delta.seconds
    if not LOGGING_FILE:
        logging.basicConfig(filename=LOGGING_FILE, level=LOGGING_LEVEL)

    if region.upper() not in REGION_LIST:
        raise ValueError(f"region must be one of {', '.join(REGION_LIST)}")

    dig: bytes = mac_digest(mac)

    with open(pathlib.Path(HERE / TEMPLATES[region]), "rb") as bin_template, open(
        pathlib.Path(HERE / "included/oui_list.txt")
    ) as oui_file:
        blob: bytearray = pack_blob(dig, timestamp, bytearray(bin_template.read()))
        oui_list: list = oui_file.read().splitlines()

    if validate_mac(mac, oui_list) == 3:
        logging.info("If you're using Dolphin, try File→Open instead")
        logging.critical(
            'Dolphin MAC "%s" on: %s, ' "region: %s, bundle: %s",
            serialize_mac(mac.upper()),
            timestamp,
            region,
            pack_bundle,
        )
        return 3

    if validate_mac(mac, oui_list) == 2:
        logging.info("The exploit will only work if you enter your Wii's MAC address")
        logging.critical(
            'Invalid MAC "%s" on: %s, ' "region: %s, bundle: %s",
            serialize_mac(mac.upper()),
            timestamp,
            region,
            pack_bundle,
        )
        return 2

    if validate_mac(mac, oui_list) == 1:
        logging.info("You must input a 12-length MAC address")
        logging.critical(
            'Bad length MAC "%s" on: %s, ' "region: %s, bundle: %s",
            serialize_mac(mac.upper()),
            timestamp,
            region,
            pack_bundle,
        )
        return 1

    with zipfile.ZipFile(sys.stdout, "w") as zip_out:
        zip_out.writestr(
            sd_path(dig, deltatime, timestamp), pack_blob(dig, timestamp, blob)
        )
        if pack_bundle:
            for name, dpath in [
                (name, pathlib.Path(BUNDLEBASE / name))
                for name in os.listdir(BUNDLEBASE)
                if not name.startswith(".")
            ]:
                zip_out.write(dpath, name)
    logging.info(
        '✉💣 LetterBombed stream"%s" on: %s, region: %s, bundle: %s',
        serialize_mac(mac.upper()),
        timestamp,
        region,
        pack_bundle,
    )
    return 0
