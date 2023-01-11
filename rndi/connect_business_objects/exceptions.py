#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import Optional


class MissingParameterError(Exception):
    def __init__(self, message: str, parameter: Optional[str] = None):
        self.message = message
        self.parameter = parameter

        super().__init__(self.message)


class MissingItemError(Exception):
    def __init__(self, message: str, item: Optional[str] = None):
        self.message = message
        self.item = item

        super().__init__(self.message)
