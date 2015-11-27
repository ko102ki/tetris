#import cx_Freeze
#
#executables = [cx_Freeze.Executable('tetris_ver1_0.py')]
#
#cx_Freeze.setup(
#    name = 'tetris',
#    options = {'build_exe': {'packages': ['pygame'],
#                            'include_files':['data/i.bmp']}},
#    executables = executables
#    )

from cx_Freeze import setup, Executable

setup(
    name = "tetris" ,
    version = "0.1" ,
    description = "tetris" ,
    executables = [Executable("tetris_ver1_0.py")]  ,
)