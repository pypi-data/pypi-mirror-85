from gherkin2oas import gherkin2oas
import os
from pathlib import Path

def test_simple_scenarios():
	test_folders_path = locate_the_test_folders_path()
	for test_folder in os.listdir(test_folders_path):
		print(gherkin2oas(
			resources_folder="{}/{}".format(test_folders_path, test_folder),
			oas_title = "test",
			oas_description = "test",
			oas_security = "test",
			oas_version = "1",
			oas_host = "localhost",
			oas_basepath = "/api",
			oas_schemes=["http", "https"],
			oas_produces=["application/json"]
			))

def locate_the_test_folders_path():
	for path in [os.getcwd(), Path(os.getcwd()).parent]:
		for dirpath, dirnames, filenames in os.walk(path):
			for dirname in dirnames:
				if dirname == "gentests":
					return os.path.join("{}/{}".format(dirpath, dirname))