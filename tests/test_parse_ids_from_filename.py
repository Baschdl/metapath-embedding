from unittest import TestCase
from metapath_embedding.find_neg_edges import parse_ids_from_filename


class TestParse_ids_from_filename(TestCase):
    def test_parse_ids_from_filename(self):
        self.assertEqual(parse_ids_from_filename("MetaPaths-5-0.8_0_17414227.txt"), (0, 17414227))
