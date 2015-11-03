__author__ = 'Stephen Kan'

import unittest
import mock
from superphy.uploader.miner_ijson import MinerDataUploader

MinerDataUploader('samples/test_set.json', 'ecoli')