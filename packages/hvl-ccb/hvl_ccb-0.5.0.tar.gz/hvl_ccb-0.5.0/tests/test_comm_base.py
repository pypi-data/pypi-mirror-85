#  Copyright (c) 2019-2020 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Tests for the base class CommunicationProtocol.
"""

import pytest

from hvl_ccb.comm import NullCommunicationProtocol
from hvl_ccb.configuration import EmptyConfig


def test_instantiation():

    for arg in (EmptyConfig(), {}, None):
        with NullCommunicationProtocol(arg) as com:
            assert com is not None
            assert isinstance(com.config, EmptyConfig)

    with pytest.raises(TypeError):
        NullCommunicationProtocol({'extra_key': 0})
