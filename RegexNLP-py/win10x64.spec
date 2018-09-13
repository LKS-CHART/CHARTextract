# -*- mode: python -*-

block_cipher = None

import os
import scipy
import sys
sys.setrecursionlimit(5000)

a = Analysis(['__main_simple__.py'],
             pathex=['build_requirements\\ucrt\\DLLs\\x64', os.path.join(os.path.dirname(scipy.__file__), 'extra-dll'),
                os.getcwd()],
             binaries=[],
             datas=[(os.path.join(os.path.dirname(scipy.__file__), 'special', '_ufuncs_cxx.cp36-win_amd64.pyd'),'.'),],
             hiddenimports=['scipy._lib.messagestream', 'numpy', 'tkinter', 'scipy', 'matplotlib', 'fixtk',
                'scipy.signal', 'scipy.signal.bsplines', 'scipy.special', 'scipy.special._ufuncs_cxx',
                'scipy.linalg.cython_blas',
                'scipy.linalg.cython_lapack',
                'scipy.integrate',
                'scipy.integrate.quadrature',
                'scipy.integrate.odepack',
                'scipy.integrate._odepack',
                'scipy.integrate.quadpack',
                'scipy.integrate._quadpack',
                'scipy.integrate._ode',
                'scipy.integrate.vode',
                'scipy.integrate._dop', 'scipy._lib', 'scipy._build_utils','scipy.__config__',
                'scipy.integrate.lsoda', 'scipy.cluster', 'scipy.constants','scipy.fftpack','scipy.interpolate',
                'scipy.io','scipy.linalg','scipy.misc','scipy.ndimage','scipy.odr','scipy.optimize',
                'scipy.setup','scipy.sparse','scipy.spatial','scipy.special','scipy.stats','scipy.version',
                'sklearn.utils.sparsetools._graph_validation', 'sklearn.utils.sparsetools._graph_tools',],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='RegexNLP',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='RegexNLP-py')
