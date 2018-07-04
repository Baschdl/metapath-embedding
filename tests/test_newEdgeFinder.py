from unittest import TestCase
from find_new_edges import NewEdgeFinder
import os


class TestNewEdgeFinder(TestCase):
    def test_find_equal(self):
        self.assertEqual([], NewEdgeFinder(os.path.join('data', 'all-edgelist-wikidata-Qid.csv'),
                                           os.path.join('data', 'all-edgelist-wikidata-Qid.csv')).find())

    def test_find_extra_edge_directed(self):
        self.assertEqual([('Q8229', 'Q37471758')], NewEdgeFinder(os.path.join('data', 'all-edgelist-wikidata-Qid.csv'),
                                                                 os.path.join('data',
                                                                              'all-edgelist-wikidata-Qid-new.csv')).find())

    def test_find_extra_edge_undirected(self):
        self.assertEqual([], NewEdgeFinder(os.path.join('data', 'all-edgelist-wikidata-Qid.csv'),
                                           os.path.join('data', 'all-edgelist-wikidata-Qid-new.csv'),
                                           directed=False).find())
