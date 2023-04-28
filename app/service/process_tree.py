from typing import Iterable
from nltk import Tree
import pydantic
import itertools
import re

DELIMITERS = (",", "CC")

TREE_POSITION = tuple[int, ...]


class ParentNode(pydantic.BaseModel):
    """Iterface"""

    parent_pos: TREE_POSITION
    childs_pos_list: list[TREE_POSITION]


class ProcessTree:
    def __init__(self, query: str, limit: int) -> None:
        self.query = query
        self.tree = Tree.fromstring(query)
        self.limit = limit

    @staticmethod
    def _get_nps(tree: Tree) -> list[ParentNode]:
        """
        Return a list of parents position and its childs positions
        if parent is 'NP' and its child 'NP' and separated with either ',' or 'CC'=(and|or)
        """
        target_parent_with_its_child_positions: list[ParentNode] = []

        for pos in tree.treepositions():
            node = tree[pos]
            isEvenChilds__NP = all(
                map(lambda n: isinstance(n, Tree) and n.label() == "NP", node[::2])
            )
            isOddChilds__CC_Coma = all(
                map(
                    lambda n: isinstance(n, Tree) and n.label() in DELIMITERS,
                    node[1::2],
                )
            )
            if isEvenChilds__NP and isOddChilds__CC_Coma:
                # Get childs positions for its parent
                childs_pos_list = list(
                    (*pos, i) for i in range(len(node)) if i % 2 == 0
                )
                target_parent_with_its_child_positions.append(
                    ParentNode(parent_pos=pos, childs_pos_list=childs_pos_list)
                )
        return target_parent_with_its_child_positions

    @staticmethod
    def _format_str(tree: Tree):
        return re.sub("[\t\s]{2,}", " ", re.sub("[\r\n]", "", str(tree)))

    @staticmethod
    def _shuttle_tree_pos(
        tree: Tree,
        a_positions: Iterable[TREE_POSITION],
        b_positions: Iterable[TREE_POSITION],
    ):
        """Update an arbitrary tree with new positions"""

        updated_tree = tree.copy(deep=Tree)

        for a, b in zip(a_positions, b_positions):
            if a != b:
                updated_tree[a], updated_tree[b] = tree[b], tree[a]

        return updated_tree

    def get_unique(self) -> list[dict[str]]:
        """Return unique up to self.limit tree representations"""
        result: list[dict[str]] = []
        nps_nodes = self._get_nps(self.tree)

        # TODO Process multiple variation
        first_node = nps_nodes[0]

        first_node.childs_pos_list
        # Generate possible posititions
        permutations = list(itertools.permutations(first_node.childs_pos_list))

        # Get initial position
        initial_child_pos = permutations[0]

        # Get new possible possitions limited by self.limit + 1
        possible_child_pos_list = permutations[1 : self.limit + 1]

        for b_positions in possible_child_pos_list:
            updated_tree = self._shuttle_tree_pos(
                self.tree.copy(deep=True), initial_child_pos, b_positions
            )
            result.append({"text": self._format_str(updated_tree)})

        return result
