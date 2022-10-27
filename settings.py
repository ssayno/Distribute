#!/usr/bin/env python3
import os
STATIC = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), 'static'
    )
)
COOKIES = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), 'Data', 'Cookies'
    )
)
DELIMITER = "|"
TOKEN_SIZE = 30
