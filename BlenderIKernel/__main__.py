from ipykernel.kernelapp import IPKernelApp
from . import BlenderIKernel

IPKernelApp.launch_instance(kernel_class=BlenderIKernel)
