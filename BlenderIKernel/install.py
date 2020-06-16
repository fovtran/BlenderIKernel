import argparse
import json
import os, sys

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory

from os.path import abspath, dirname, join as pathjoin

#sys.executable = pathjoin(dirname(abspath(sys.argv[0])), 'blender_ipython_wrapper.py')
sys.executable = 'f:/binr/blender2.78.4win64-bpy-module-py35/bpypython.exe'

kernel_json = {
    "argv": [sys.executable, "-m", "BlenderIKernel", "-f", "{connection_file}"],
    "display_name": "Blender IKernel",
    "language": "python",
}

def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        # TODO: Copy any resources
		# rm -rf BlenderIKernel\__pycache__ build c:\Python38-x86_64\lib\site-packages\BlenderIKernel* C:\Users\diego2\AppData\Roaming\jupyter\kernels\echo

        print('Installing Jupyter kernel spec')
        KernelSpecManager().install_kernel_spec(td, '.BlenderIKernel', user=user, prefix=prefix, replace=True)

def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False # assume not an admin on non-Unix platforms

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--user', action='store_true', help="Install to the per-user kernels registry. Default if not root.")
    ap.add_argument('--sys-prefix', action='store_true', help="Install to sys.prefix (e.g. a virtualenv or conda env)")
    ap.add_argument('--prefix', help="Install to the given prefix. " "Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/")
    args = ap.parse_args(argv)

    if args.sys_prefix:
        args.prefix = sys.prefix
    if not args.prefix and not _is_root():
        args.user = True

    install_my_kernel_spec(user=args.user, prefix=args.prefix)

if __name__ == '__main__':
    main()
