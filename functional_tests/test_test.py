
import unittest

# screen dumps config
from pathlib import Path, PurePath
from .base import FunctionalTest

# Path(__file__).resolve() - full path to base.py
# xxx/
#    screendumps
#    superlist/functional_tests/base.py
SCREEN_DUMP_LOCATION = Path(__file__).resolve().parent.parent.parent.joinpath('screendumps')

@unittest.skip
class TempTest(unittest.TestCase):
    '''test for temporary features'''

    def test_Path(self):
        #Path.resolve(PurePath.joinpath(BASE_DIR, '../database/db.sqlite3')),
        print(f'screendumps - {SCREEN_DUMP_LOCATION}')
        if not SCREEN_DUMP_LOCATION.exists():
            SCREEN_DUMP_LOCATION.mkdir()
            print(f'creating dir')
            if SCREEN_DUMP_LOCATION.is_dir():
                print('Created!!!')

@unittest.skip
class ScreenDumpTest(FunctionalTest):
    '''test dumpging screenshots'''
    def test_just_fail(self):
        '''just fail'''
        self.fail()

    def test_open_and_fail(self):
        '''open home page and fail'''
        self.browser.get(self.live_server_url)
        self.fail()

