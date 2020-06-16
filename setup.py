from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='BlenderIKernel',
    version='1.1',
    packages=['BlenderIKernel', 'BlenderIKernel/tools'],
    description='Simple Blender IKernel for Jupyter',
    long_description=readme,
    author='DMC Development Team',
    author_email='dcadogan@live.com.ar',
    url='https://github.com/fovtran/BlenderIKernel',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
	data_files=[
	('lib/site-packages/BlenderIKernel/templates', ['BlenderIKernel/templates/file1.template'])
	],
)
