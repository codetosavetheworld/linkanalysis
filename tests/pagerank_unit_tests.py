from __future__ import print_function
import unittest
from network import Network
import numpy as np
import numpy.testing

# setup function
def setup():
    # Start from an empty graph
    n = Network()
    n.graph_instance.delete_all()
    #just for test
    n.add_node("www.example.com", "2015-05-02", "daily")
    n.add_node("www.example2.com", "2017-07-02", "hourly")
    n.add_node("www.example3.com", "2017-07-01", "hourly")

    n1 = n.get_node("www.example.com")
    n2 = n.get_node("www.example2.com")
    n3 = n.get_node("www.example3.com")

    n.add_edge(n1,n2,"<h1>")
    n.add_edge(n3,n2,"<h1>")
    n.add_edge(n1,n2,"<h3>")

    return n, n1, n2, n3

def test_simple_pagerank_check():
    n, n1, n2, n3  = setup()
    np.testing.assert_almost_equal(
        n._pagerank(),
        [ 0.2127657, 0.5744686,   0.2127657],
    )
    print("passed test_simple_pagerank_check")

def test_adding_pagerank_to_nodes():
    n, n1, n2, n3  = setup()
    assert n1.get("page_rank") is None
    n.update_pagerank()
    assert n1.get("page_rank") is not None
    print("passed test_adding_pagerank_to_nodes")

def test_get_specific_pagerank():
    n, n1, n2, n3  = setup()
    # pagerank for a specific link
    n.update_pagerank()
    assert abs(n2.get("page_rank") - 0.5744686) < 0.0001
    print("passed test_get_specific_pagerank (checked value)")

def test_add_node_update_pagerank():
    n, n1, n2, n3  = setup()
    n.update_pagerank()
    assert abs(n2.get("page_rank") - 0.5744686) < 0.0001
    # Now add some nodes
    n4 = n.add_node("www.example3.com", "2017-08-01", "hourly")
    n.add_edge(n1,n4,"<h1>")
    n.add_edge(n3,n4,"<h1>")
    n.update_pagerank()
    assert abs(n2.get("page_rank") - 0.41605838) < 0.0001
    print("passed test_add_node_update_pagerank - pagerank changed")

def test_get_dictionary():
    n, n1, n2, n3  = setup()
    links = ["www.example.com", "www.example2.com"]
    dct = n.get_pagerank_dict(links=links)
    assert isinstance(dct, dict)
    assert len(dct) == 2
    assert sorted(list(dct.keys())) == sorted(links)
    print("passed test_get_dictionary, dictionary returned")

if __name__ == '__main__':
    test_simple_pagerank_check()
    test_adding_pagerank_to_nodes()
    test_get_specific_pagerank()
    test_add_node_update_pagerank()
    test_get_dictionary()
    print("All tests passed")
