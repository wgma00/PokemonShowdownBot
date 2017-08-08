
import pytest
from plugins.math.images import OnlineImage
import re


""" Tests the commands that are within the Command method
"""


def test_get_image_info_url():
    """this url will very likely not fail unless imgur servers are down."""
    url = 'http://i.imgur.com/b9STQvf.jpg'
    width, height = OnlineImage.get_image_info(url)
    assert width == 750 and height == 712

