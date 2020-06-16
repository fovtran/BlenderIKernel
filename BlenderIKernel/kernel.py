from ipykernel.kernelbase import Kernel
from IPython.display import HTML
from IPython import display
import urllib
import base64
#from tools import launch_blender
import tempfile

from .tools import pip_blender

def temp():
	tempscript = tempfile.mktemp()+"_blender_ipython_kernel.py"
	with open(tempscript,"w") as f:
		f.write("")

	try:
		print('starting: blender -b -P', tempscript)
		sys.exit(subprocess.call(['F:/BIN4/blender-2.82-windows64/blender.exe', '-b', '-P', tempscript]))
	finally:
		os.remove(tempscript)


def show_plot(url, width=700, height=500):
	s = '<iframe height="%s" id="igraph" scrolling="no" seamless="seamless" src="%s" width="%s"></iframe>' %\
	(height+50, "/".join(map(str,[url, width, height])), width+50)
	#return HTML(s)
	return s

class BlenderIKernel(Kernel):
	implementation = 'BlenderIKernel'
	implementation_version = '1.0'
	language = 'no-op'
	language_version = '0.1'
	language_info = {  'name': 'Any text', 'mimetype': 'text/html', 'file_extension': '.py', }
	banner = "BlenderIKernel - as useful as a parrot"

	def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
		image_file = open('f:/hyper_blender/untitled1.png', 'rb')
		c = urllib.parse.quote( base64.b64encode(image_file.read()) )
		data = {"image/png": c}

		if True:
			code = show_plot('https://plot.ly/~andreyDim/110')
			#data = {"text/html": code}
			stream_content = {'name': 'stdout', 'text': "<h2>header</h2>"}
			self.send_response(self.iopub_socket, 'stream', stream_content)

		if not silent:
			metadata =  { 'image/png' : { 'width': 600, 'height': 400 }  }
			display_data = {'source': 'kernel', 'data': data, 'metadata': metadata}
			self.send_response(self.iopub_socket, 'display_data', display_data)
			#display.Image(base64.b64decode(encoded_string))

		return {'status': 'ok', 'execution_count': self.execution_count, 'payload': [], 'user_expressions': {}, }
