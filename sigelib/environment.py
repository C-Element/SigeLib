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


class Environment(object):
    """
    Sige Environment class
    """

    def __init__(self, load_from_default=False):
        self.production = False
        self.sige_host = ''
        self.sige_user = ''
        self.sige_pass = ''
        self.sige_db = ''
        self.mss_driver_host = ''
        self.mss_driver_user = ''
        self.mss_driver_pass = ''
        self.mss_driver_db = ''
        self.mss_gate_host = ''
        self.mss_gate_user = ''
        self.mss_gate_pass = ''
        self.mss_gate_db = ''
        self.mss_top_host = ''
        self.mss_top_user = ''
        self.mss_top_pass = ''
        self.mss_top_db = ''
        self.mss_inner_host = ''
        self.mss_inner_user = ''
        self.mss_inner_pass = ''
        self.mss_inner_db = ''
        self.winthor_host = ''
        self.winthor_user = ''
        self.winthor_pass = ''
        if load_from_default:
            self.load()

    def load(self, path='/var/.sige/.environment'):
        """
        Load environment variables from file.
        """
        with open(path, 'r') as file:
            for line in file.read().split('\n'):
                data = line.split('=')
                if data[0] == 'PRODUCTION':
                    self.production = bool(int(data[1]))
                elif data[0] == 'SIGE_HOST':
                    self.sige_host = data[1]
                elif data[0] == 'SIGE_USER':
                    self.sige_user = data[1]
                elif data[0] == 'SIGE_PASS':
                    self.sige_pass = data[1]
                elif data[0] == 'SIGE_DB':
                    self.sige_db = data[1]
                elif data[0] == 'MSS_DRIVER_HOST':
                    self.mss_driver_host = data[1]
                elif data[0] == 'MSS_DRIVER_USER':
                    self.mss_driver_user = data[1]
                elif data[0] == 'MSS_DRIVER_PASS':
                    self.mss_driver_pass = data[1]
                elif data[0] == 'MSS_DRIVER_DB':
                    self.mss_driver_db = data[1]
                elif data[0] == 'MSS_GATE_HOST':
                    self.mss_gate_host = data[1]
                elif data[0] == 'MSS_GATE_USER':
                    self.mss_gate_user = data[1]
                elif data[0] == 'MSS_GATE_PASS':
                    self.mss_gate_pass = data[1]
                elif data[0] == 'MSS_GATE_DB':
                    self.mss_gate_db = data[1]
                elif data[0] == 'MSS_TOP_HOST':
                    self.mss_top_host = data[1]
                elif data[0] == 'MSS_TOP_USER':
                    self.mss_top_user = data[1]
                elif data[0] == 'MSS_TOP_PASS':
                    self.mss_top_pass = data[1]
                elif data[0] == 'MSS_TOP_DB':
                    self.mss_top_db = data[1]
                elif data[0] == 'MSS_INNER_HOST':
                    self.mss_inner_host = data[1]
                elif data[0] == 'MSS_INNER_USER':
                    self.mss_inner_user = data[1]
                elif data[0] == 'MSS_INNER_PASS':
                    self.mss_inner_pass = data[1]
                elif data[0] == 'MSS_INNER_DB':
                    self.mss_inner_db = data[1]
                elif data[0] == 'WINTHOR_HOST':
                    self.winthor_host = data[1]
                elif data[0] == 'WINTHOR_USER':
                    self.winthor_user = data[1]
                elif data[0] == 'WINTHOR_PASS':
                    self.winthor_pass = data[1]

    def save(self, path='/var/.sige/.environment'):
        """
        Save environment variables to file.
        """
        with open(path, 'w') as file:
            lines = 'PRODUCTION={}\n'.format(1 if self.production else 0)
            lines += 'SIGE_HOST={}\n'.format(self.sige_host)
            lines += 'SIGE_USER={}\n'.format(self.sige_user)
            lines += 'SIGE_PASS={}\n'.format(self.sige_pass)
            lines += 'SIGE_DB={}\n'.format(self.sige_db)
            lines += 'MSS_DRIVER_HOST={}\n'.format(self.mss_driver_host)
            lines += 'MSS_DRIVER_USER={}\n'.format(self.mss_driver_user)
            lines += 'MSS_DRIVER_PASS={}\n'.format(self.mss_driver_pass)
            lines += 'MSS_DRIVER_DB={}\n'.format(self.mss_driver_db)
            lines += 'MSS_GATE_HOST={}\n'.format(self.mss_gate_host)
            lines += 'MSS_GATE_USER={}\n'.format(self.mss_gate_user)
            lines += 'MSS_GATE_PASS={}\n'.format(self.mss_gate_pass)
            lines += 'MSS_GATE_DB={}\n'.format(self.mss_gate_db)
            lines += 'MSS_TOP_HOST={}\n'.format(self.mss_top_host)
            lines += 'MSS_TOP_USER={}\n'.format(self.mss_top_user)
            lines += 'MSS_TOP_PASS={}\n'.format(self.mss_top_pass)
            lines += 'MSS_TOP_DB={}\n'.format(self.mss_top_db)
            lines += 'MSS_INNER_HOST={}\n'.format(self.mss_inner_host)
            lines += 'MSS_INNER_USER={}\n'.format(self.mss_inner_user)
            lines += 'MSS_INNER_PASS={}\n'.format(self.mss_inner_pass)
            lines += 'MSS_INNER_DB={}\n'.format(self.mss_inner_db)
            lines += 'WINTHOR_HOST={}\n'.format(self.winthor_host)
            lines += 'WINTHOR_USER={}\n'.format(self.winthor_user)
            lines += 'WINTHOR_PASS={}\n'.format(self.winthor_pass)
            file.write(lines)
