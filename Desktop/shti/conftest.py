import pytest

def pytest_addoption(parser):
    parser.addoption("--file_path", action="store", default="", help="input file path")
    parser.addoption("--mp4box_file_path", action="store", default="", help="mp4box_file_path input file path")
    