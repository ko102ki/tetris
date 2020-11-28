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

target = Executable(
    script='tetriz_ver1_1.py',
    icon='data/exe_icon.ico',
    base='Win32GUI'
)

setup(
    name = 'tetriz' ,
    version = '1.1' ,
    description = 'tetriz' ,
    #executables = [Executable('tetris_ver1_1.py')]  ,
    executables = [target]  ,
)
