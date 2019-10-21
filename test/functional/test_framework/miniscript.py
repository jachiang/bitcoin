#!/usr/bin/env python3
# Copyright (c) 2015-2019 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Functionality to build and parse miniscripts.
"""

from .script import CScript
from enum import Enum

class Type:
    literals = {
            "B": 1 << 0,    # Base type
            "V": 1 << 1,    # Verify type
            "K": 1 << 2,    # Key type
            "W": 1 << 3,    # Wrapped type
            "z": 1 << 4,    # Zero-arg property
            "o": 1 << 5,    # One-arg property
            "n": 1 << 6,    # Nonzero arg property
            "d": 1 << 7,    # Dissatisfiable property
            "u": 1 << 8,    # Unit property
            "e": 1 << 9,    # Expression property
            "f": 1 << 10,   # Forced property
            "s": 1 << 11,   # Safe property
            "m": 1 << 12,   # Nonmalleable property
            "x": 1 << 13,   # Expensive verify
            }

    def __init__(self, bitflags = 0):
        self.flags = bitflags

    def from_string(self, property_str):
        bitflags = 0
        for char in property_str:
            bitflags |= self.literals[char]
        assert self.is_valid(bitflags=bitflags)
        self.flags = bitflags

    def to_string(self):
        assert self.is_valid()
        property_str = ""
        for i in range(len(self.literals)):
            bitflag = 1 << i
            # Check if bitflag is active.
            if bitflag & self.flags != 0:
                # Search for flag literal corresponding to bitflag.
                for lit, flag in self.literals.items():
                    if flag == bitflag:
                        property_str += lit
        return property_str

    def is_valid(self, bitflags = None):

        # Evaluate flags of this Type instance.
        if bitflags is None:
            bitflags = self.flags

        num_types = \
            bool(self.flags & self.literals["K"]) + \
            bool(self.flags & self.literals["V"]) + \
            bool(self.flags & self.literals["B"]) + \
            bool(self.flags & self.literals["W"])

        if num_types == 0:
            return False
        else:
            assert num_types is 1
            # Check for conflicts in Type & properties.
            return \
                (not self.flags & self.literals["z"] or not self.flags & self.literals["o"]) and \
                (not self.flags & self.literals["n"] or not self.flags & self.literals["z"]) and \
                (not self.flags & self.literals["V"] or not self.flags & self.literals["d"]) and \
                (not self.flags & self.literals["K"] or self.flags & self.literals["u"]) and \
                (not self.flags & self.literals["V"] or not self.flags & self.literals["u"]) and \
                (not self.flags & self.literals["e"] or not self.flags & self.literals["f"]) and \
                (not self.flags & self.literals["e"] or self.flags & self.literals["d"]) and \
                (not self.flags & self.literals["V"] or not self.flags & self.literals["e"]) and \
                (not self.flags & self.literals["d"] or not self.flags & self.literals["f"]) and \
                (not self.flags & self.literals["V"] or self.flags & self.literals["f"]) and \
                (not self.flags & self.literals["K"] or self.flags & self.literals["s"]) and \
                (not self.flags & self.literals["z"] or self.flags & self.literals["m"])

class NodeTypes(Enum):
    JUST_0 = 0
    JUST_1 = 1
    PK = 2
    PK_H = 3

class WitnessType(Enum):
    # Type of witness elements.
    signature = 0
    preimage = 1
    threshold = 2

class Node:
    NodeTypes
    def __init__(self):
        self.script = CScript()
        # What about OR
        self.sat = None

        # What about OR
        self.nsat = None
        self.type = None
        self.properties = None

        # Stacksize
        # Witness size
        # Requires signature
        # TopLevel valid

    def to_type(self):
        pass

    def is_valid(self):
        # Derive properties.
        pass

    def construct_pk(self, ecpubkey):
        assert ecpubkey.is_valid
        self.script_elements = [ecpubkey.get_bytes()]
        # Top level needs to expand this...no. That is OR.
        # [(threshold, 2, 4, [sat], [sat], [sat], [sat])]
        self.sat_xy = [(WitnessType.signature, ecpubkey)]
        self.sat_z = []
        self.nsat = [0]
        self.properties = Type()
        self.properties.from_string("Konudems")
        self.xyz = [None, None, None]

    @staticmethod
    def _lift_threshold(satisfying_expr):
        pass
        # Lift threshold subexpressions to top-level threshold expression.
        # Parse tree, and build top-level treshold.



    # def pk(key):
    #     assert((key[0] in [0x02, 0x03]) or (key[0] not in [0x04, 0x06, 0x07]))
    #     assert(len(key) == 33)
    #     script = lambda x: [key]
    #     nsat = lambda x: [0]
    #     sat_xy = lambda x: [('sig', key)]
    #     sat_z = lambda x: [False]
    #     typ = lambda x: 'K' # Only one possible.
    #     corr = lambda x: {'z': False,'o': True, 'n': True, 'd': True, 'u': True}
    #     mal = lambda x: {'e': True,'f': False, 'm': True, 's': True}
    #     children = [None, None, None] # Terminal.
    #     return node_type(script=script, nsat=nsat, sat_xy=sat_xy, sat_z=sat_z,  typ=typ, corr=corr, mal=mal,children=children)
