#!/usr/bin/env python

# Copyright 2016 Earth Sciences Department, BSC-CNS

# This file is part of R2D2.

# R2D2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# R2D2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with R2D2. If not, see <http://www.gnu.org/licenses/>.

import unittest
from r2d2.argument_parser import ArgumentParser
from r2d2.http.dataset import DatasetHTTP


class TestAERONETv3(unittest.TestCase):
    pyear = None
    pmon = None
    pday = None

    def setUp(self):
        self.argument_parser = ArgumentParser()

    def test_download(self):
        args = self.argument_parser.parse_args({
            '--config','./conf/aeronet-v3/config.cfg',
            '--param_year', str(self.pyear),
            '--param_month', str(self.pmon),
            '--param_day', str(self.pday)})
        self._assert_download_succeeded(args)

    def _assert_download_succeeded(self, args):
        self.assertTrue(DatasetHTTP(args).main())#, '{0} argument has not been initialized correctly'.format(argument))


if __name__ == "__main__":
    import sys
    from datetime import datetime
    dt = datetime.strptime(sys.argv[1], "%Y%m%d")
    TestAERONETv3.pyear = dt.year
    TestAERONETv3.pmon = dt.month
    TestAERONETv3.pday = dt.day
    unittest.main(argv=[sys.argv[1]])
