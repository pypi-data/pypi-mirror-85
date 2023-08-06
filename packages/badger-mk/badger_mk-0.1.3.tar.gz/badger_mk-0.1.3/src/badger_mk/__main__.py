#!/usr/bin/env python3
"""Badger

Create graphic files from templates via data substitution.
"""
from __future__ import annotations

import sys

import badger_mk


def main(args=None) -> int:
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    badger_mk.Badger().run()


if __name__ == "__main__":
    sys.exit(main())
