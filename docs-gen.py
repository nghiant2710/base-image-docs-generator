import json
import os

from string import Template
import shutil

class DocsGenerator(object):

	data = {}

	def __init__(self):
		self.device = json.loads(open('device.json').read())
		self.arch = set(item["arch"] for item in self.device)

	def import_data(self):
		self.clean_up()
		for device in self.device:
			docs_template = open('device.debian.tpl').read()
			docs_ref = open('device.debian.tpl.ref').read()
			if self.data.has_key(device["arch"]):
				self.data[device["arch"]] = self.data[device["arch"]] + '\n\n' + Template(docs_template).safe_substitute(device)
			else:
				self.data[device["arch"]] = '\n\n' + Template(docs_template).safe_substitute(device)
			if self.data.has_key("REF"):
				self.data["REF"] = self.data["REF"] + '\n\n' + Template(docs_ref).safe_substitute(device)
			else:
				self.data["REF"] = '\n\n' + Template(docs_ref).safe_substitute(device)

			if device["distro"]:
				for distro in device["distro"]:
					docs_template = open('device.{distro}.tpl'.format(distro=distro)).read()
					docs_ref = open('device.{distro}.tpl.ref'.format(distro=distro)).read()
					self.data[device["arch"]] = self.data[device["arch"]] + Template(docs_template).safe_substitute(device)
					self.data["REF"] = self.data["REF"] + '\n' + Template(docs_ref).safe_substitute(device)

	def clean_up(self):
		for arch in self.arch:
			if os.path.isfile(arch):
				os.remove(arch)
			if os.path.isfile(arch + '.ref'):
				os.remove(arch + '.ref')


def main():
	docs = DocsGenerator()
	docs.import_data()
	#docs.clean_up()
	docs_main = open('main.tpl').read()
	print(Template(docs_main).safe_substitute(docs.data))

if __name__ == '__main__':
	main()
