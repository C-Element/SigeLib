# Copyright (C) 2015 Clemente Junior
#
# This file is part of SigeLib
#
# SigeLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import sys

from sigelib import Environment

sys.path.append('../BifrostDB/')
from bifrost.db.mss import MSs
from bifrost.db.oracle import OracleDB
from bifrost.db.pg import PgDB


def create_sige():
    """
    Return a PostgreSQL connection to Bifrost DataBase.
    """
    env = Environment(True)
    return PgDB(env.sige_host, env.sige_user, env.sige_pass, env.sige_db)


def create_mss_driver():
    """
    Return a SQL Server connection to TopPonto Drivers DataBase.
    """
    env = Environment(True)
    return MSs(env.mss_driver_host, env.mss_driver_user, env.mss_driver_pass,
               env.mss_driver_db)


def create_mss_gate():
    """
    Return a SQL Server connection to mr_acessi_cn DataBase.
    """
    env = Environment(True)
    return MSs(env.mss_gate_host, env.mss_gate_user, env.mss_gate_pass,
               env.mss_gate_db)


def create_mss_top():
    """
    Return a SQL Server connection to TopPonto employees DataBase.
    """
    env = Environment(True)
    return MSs(env.mss_top_host, env.mss_top_user, env.mss_top_pass,
               env.mss_gate_db)


def create_mss_inner():
    """
    Return a SQL Server connection to GerenciadoInnerRep Drivers DataBase.
    """
    env = Environment(True)
    return MSs(env.mss_inner_host, env.mss_inner_user, env.mss_inner_pass,
               env.mss_inner_db)


def create_oracle():
    """ Return a Oracle connection to WinThor DataBase. """
    env = Environment(True)
    return OracleDB(env.winthor_host, env.winthor_user, env.winthor_pass)


    # def create_sigepe():
    #    """ Return a PostgreSQL connection to SIGePe DataBase. """
    #
    #    return PgDB('10.10.1.251', 'sigepe', 'epegis', 'sigepe')
