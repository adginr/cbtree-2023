from app.service import ProcessTree
from nltk.tree import tree

query = """(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP
Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP
(JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ
trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS
restaurants) ) ) ) ) ) ) )"""


def test_class_initialization():
    process_tree = ProcessTree(query=query, limit=20)
    assert isinstance(process_tree.tree, tree.Tree)

    process_tree._get_nps(process_tree.tree)
