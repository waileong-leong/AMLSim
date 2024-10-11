import pytest
import networkx as nx
from aml_simulator.transaction_graph_generator import TransactionGenerator, get_degrees
from aml_simulator.transaction_graph_generator import get_in_and_out_degrees
from aml_simulator.transaction_graph_generator import directed_configuration_model
from .fixtures.conf import CONFIG
from aml_simulator.amlsim.normal_model import NormalModel
import pandas as pd 
import re 
def test_get_degrees():
    result = get_degrees('tests/csv/degree.csv', 12)
    assert result == (
        [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # in
        [0, 0, 2, 1, 1, 0, 0, 0, 1, 1, 0, 0]   # out
    )

def test_get_in_and_out_degrees_no_padding():
    df = pd.DataFrame([[1,2,4],[2,4,2],[1,2,4]], columns=['count', 'in-degree', 'out-degree'])
    result = get_in_and_out_degrees(df, 4)
    assert result == (
        [2, 4, 4, 2],
        [4, 2, 2, 4]
    )

def test_get_in_and_out_degrees_padding():
    df = pd.DataFrame([[1,2,4],[2,4,2],[1,2,4]], columns=['count', 'in-degree', 'out-degree'])
    result = get_in_and_out_degrees(df, 8)
    assert result == (
        [2, 4, 4, 2, 2, 4, 4, 2],
        [4, 2, 2, 4, 4, 2, 2, 4]
    )

def test_get_in_and_out_degrees_bad_mod_throws():
    df = pd.DataFrame([[1,2,4],[2,4,2],[1,2,4]], columns=['count', 'in-degree', 'out-degree'])
    with pytest.raises(ValueError, match=re.escape('The number of total accounts (7) must be a multiple of the degree sequence length (4).')):
        get_in_and_out_degrees(df, 7)

def test_get_in_and_out_degrees_unequal_degrees_throws():
    df = pd.DataFrame([[1,2,4],[2,4,2],[1,2,3]], columns=['count', 'in-degree', 'out-degree'])
    with pytest.raises(ValueError, match=re.escape('The sum of in-degree (12) and out-degree (11) must be same.')):
        get_in_and_out_degrees(df, 8)

def test_directed_configuration_model():
    G = directed_configuration_model(
        [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # in
        [0, 0, 2, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        0
    )
    # no self-loops were removed.
    assert G.degree(0) == 2
    assert G.degree(1) == 2
    assert G.degree(2) == 2
    assert G.degree(3) == 1
    assert G.degree(4) == 1
    assert G.degree(5) == 0
    assert G.degree(6) == 0
    assert G.degree(7) == 0
    assert G.degree(8) == 1
    assert G.degree(9) == 1
    assert G.degree(10) == 1
    assert G.degree(11) == 1

def test_directed_configuration_model_no_self_loops():
    G = directed_configuration_model(
        [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # in
        [0, 0, 2, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        0
    )
    assert list(nx.selfloop_edges(G)) == []

def test_directed_configuration_model_self_loops():
    G = directed_configuration_model(
        [10, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # in
        [2, 10, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        0
    )
    assert G.degree(0) == 12
    assert G.degree(1) == 11
    assert G.degree(2) == 5
    assert G.degree(3) == 0
    assert G.degree(4) == 0
    assert G.degree(5) == 0
    assert G.degree(6) == 0
    assert G.degree(7) == 0
    assert G.degree(8) == 0
    assert G.degree(9) == 0
    assert G.degree(10) == 0
    assert G.degree(11) == 0
    assert list(nx.selfloop_edges(G)) == []

def test_mark_active_edges_marks_default_as_false():
    G = nx.DiGraph()
    G.add_nodes_from([1, 2, 3])
    G.add_edge(2, 3)

    txg = TransactionGenerator(CONFIG)
    txg.g = G
    txg.mark_active_edges()
    assert txg.g[2][3]['active'] == False

def test_mark_active_edges_marks_real_path_as_active():
    G = nx.DiGraph()
    G.add_nodes_from([1, 2, 3])
    G.add_edge(2, 3)
    G.add_edge(1, 2)

    txg = TransactionGenerator(CONFIG)
    txg.g = G
    txg.normal_models = [
        NormalModel(
            1, 'single', {2,3}, 2
        )
    ]
    txg.mark_active_edges()
    assert txg.g[2][3]['active'] == True
    assert txg.g[1][2]['active'] == False