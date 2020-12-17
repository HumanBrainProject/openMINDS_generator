import sys

sys.path.append("../..")

from openMINDS.openminds_helper import OpenMINDS_helper

def test_init():
    helper = OpenMINDS_helper()

def test_container():
    helper = OpenMINDS_helper()
    helper.get_container()
