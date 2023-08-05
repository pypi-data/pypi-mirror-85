'''
Created on Oct 19, 2015
@author: hari
'''
from __future__ import print_function
from builtins import range
from pycoils.trees.splaytree import SplayTree
import unittest

class Splay_Tree_Test_Empty_Tree(unittest.TestCase):    
    def setUp(self):
        self._splaytree = SplayTree()
    
    def test_node_count_of_empty_tree(self):
        self.assertEqual(self._splaytree.node_count, 0, 'Empty tree node count must be 0')
        
    def test_find_key_empty_tree(self):
        self.assertEqual(self._splaytree.find(20), None, 'Empty tree find operation must return None')
    
    def test_delete_element_empty_tree(self):
        self._splaytree.remove(20)
    
    def tearDown(self):
        self._splaytree = None

class Splay_Tree_Test_Tree_With_1_Element(unittest.TestCase):
    
    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 10, obj = 10)
    
    def test_node_count_of_tree_with_1_node(self):
        self.assertEqual(self._splaytree.node_count, 1, 'Tree node count must be 1')
        
    def test_find_key_of_tree_with_1_node(self):
        self.assertEqual(self._splaytree.find(10), 10, 'Find operation failed on tree with 1 node')
    
    def test_delete_element_of_tree_with_1_node(self):
        self._splaytree.remove(10)
        self.assertEqual(self._splaytree.node_count, 0, 'Empty tree node count must be 0')
        self.assertEqual(self._splaytree.find(20), None, 'Empty tree find operation must return None')
            
    def tearDown(self):
        self._splaytree = None

class Splay_Tree_Test_Tree_Count_Find_Element_With_10_Elements(unittest.TestCase):

    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 5, obj = 5)
        self._splaytree.insert(key = 8, obj = 8)
        self._splaytree.insert(key = 7, obj = 7)
        self._splaytree.insert(key = 9, obj = 9)
        self._splaytree.insert(key = 10, obj = 10)
        self._splaytree.insert(key = 2, obj = 2)
        self._splaytree.insert(key = 1, obj = 1)
        self._splaytree.insert(key = 3, obj = 3)
        self._splaytree.insert(key = 4, obj = 4)
        self._splaytree.insert(key = 6, obj = 6)
        
        self._splay_tree_node_count = 10
    
    def test_node_count_of_tree_with_10_node(self):
        self.assertEqual(self._splaytree.node_count, self._splay_tree_node_count, 'Tree node count must be 10')
        
    def test_find_element_of_tree_with_10_node(self):
        for i in range(1, 11): # 1 to 10
            tree_element = self._splaytree.find(i)
            self.assertNotEqual(tree_element, None, 'BST findElement did not return existing element')
            self.assertEqual(tree_element, i, 'Find operation failed on tree with 1 node')
    
    def tearDown(self):
        self._splaytree = None

class Splay_Tree_Test_Tree_Delete_Element_With_10_Elements(unittest.TestCase):
    
    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 5, obj = 5)
        self._splaytree.insert(key = 8, obj = 8)
        self._splaytree.insert(key = 7, obj = 7)
        self._splaytree.insert(key = 9, obj = 9)
        self._splaytree.insert(key = 10, obj = 10)
        self._splaytree.insert(key = 2, obj = 2)
        self._splaytree.insert(key = 1, obj = 1)
        self._splaytree.insert(key = 3, obj = 3)
        self._splaytree.insert(key = 4, obj = 4)
        self._splaytree.insert(key = 6, obj = 6)
        
        self._splay_tree_node_count = 10
        
    def test_delete_element_of_tree_non_existing_element(self):
        self._splaytree.remove(11)
        self.assertEqual(self._splaytree.node_count, self._splay_tree_node_count, 'Tree node count must be 10')
    
    def test_delete_element_of_tree_with_10_node(self):
        elements_to_delete = [10, 1, 7, 3, 5, 8, 2, 6, 9]
        for element in elements_to_delete:
        
            self._splaytree.remove(element)
            self.assertEqual(self._splaytree.find(element), None, 'Element found in BST after deleting it!')
            self._splay_tree_node_count = self._splay_tree_node_count - 1
            self.assertEqual(self._splaytree.node_count, self._splay_tree_node_count, 'Tree node count must tally after deletion')
    
    def tearDown(self):
        self._splaytree = None

class Splay_Tree_Test_Tree_Delete_Element_With_10_Sorted_Elements(unittest.TestCase):
    
    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 1, obj = 1)
        self._splaytree.insert(key = 2, obj = 2)
        self._splaytree.insert(key = 3, obj = 3)
        self._splaytree.insert(key = 4, obj = 4)
        self._splaytree.insert(key = 5, obj = 5)
        self._splaytree.insert(key = 6, obj = 6)
        self._splaytree.insert(key = 7, obj = 7)
        self._splaytree.insert(key = 8, obj = 8)
        self._splaytree.insert(key = 9, obj = 9)
        self._splaytree.insert(key = 10, obj = 10)
        
        self._splay_tree_node_count = 10
        
    def test_delete_element_of_tree_non_existing_element(self):
        self._splaytree.remove(11)
        self.assertEqual(self._splaytree.node_count, self._splay_tree_node_count, 'Tree node count must be 10')
    
    def test_delete_element_of_tree_with_10_node(self):
        elements_to_delete = [10, 1, 7, 3, 5, 8, 2, 6, 9, 4]
        for element in elements_to_delete: 
            self._splaytree.remove(element)
            self.assertEqual(self._splaytree.find(element), None, 'Element found in BST after deleting it!')
            self._splay_tree_node_count = self._splay_tree_node_count - 1
            self.assertEqual(self._splaytree.node_count, self._splay_tree_node_count, 'Tree node count must tally after deletion')
    
    def tearDown(self):
        self._splaytree = None

class Splay_Tree_Test_Tree_Delete_Element_With_10_Reverse_Sorted_Elements(unittest.TestCase):
    
    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 10, obj = 10)
        self._splaytree.insert(key = 9, obj = 9)
        self._splaytree.insert(key = 8, obj = 8)
        self._splaytree.insert(key = 7, obj = 7)
        self._splaytree.insert(key = 6, obj = 6)
        self._splaytree.insert(key = 5, obj = 5)
        self._splaytree.insert(key = 4, obj = 4)
        self._splaytree.insert(key = 3, obj = 3)
        self._splaytree.insert(key = 2, obj = 2)
        self._splaytree.insert(key = 1, obj = 1)
        
        self._splay_tree_node_count = 10
        
    def test_delete_element_of_tree_non_existing_element(self):
        self._splaytree.remove(11)
        self.assertEqual(self._splaytree.node_count, self._splay_tree_node_count, 'Tree node count must be 10')
    
    def test_delete_element_of_tree_with_10_node(self):
        elements_to_delete = [10, 1, 7, 3, 5, 8, 2, 6, 9, 4]
        for element in elements_to_delete: 
            self._splaytree.remove(element)
            self.assertEqual(self._splaytree.find(element), None, 'Element found in BST after deleting it!')
            self._splay_tree_node_count = self._splay_tree_node_count - 1
            self.assertEqual(self._splaytree.node_count, self._splay_tree_node_count, 'Tree node count must tally after deletion')
            
    def tearDown(self):
        self._splaytree = None
        
class Splay_Tree_Test_Has_Key_with_Empty_Tree(unittest.TestCase):    
    def setUp(self):
        self._splaytree = SplayTree()
    
    def test_has_key_empty_tree(self):
        self.assertEqual(20 in self._splaytree, False, 'Empty tree has_key operation must return False')
    
    def tearDown(self):
        self._splaytree = None

class Splay_Tree_Test_Has_Key_with_Single_Node_Tree(unittest.TestCase):    
    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 10, obj = 'Object value')
    
    def test_has_key_empty_tree(self):
        self.assertEqual(10 in self._splaytree, True, 'Tree has_key operation must return True for existing key')
    
    def tearDown(self):
        self._splaytree = None

class Splay_Tree_Test_Has_Key_With_10_Elements(unittest.TestCase):
    
    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 5, obj = 5)
        self._splaytree.insert(key = 8, obj = 8)
        self._splaytree.insert(key = 7, obj = 7)
        self._splaytree.insert(key = 9, obj = 9)
        self._splaytree.insert(key = 10, obj = 10)
        self._splaytree.insert(key = 2, obj = 2)
        self._splaytree.insert(key = 1, obj = 1)
        self._splaytree.insert(key = 3, obj = 3)
        self._splaytree.insert(key = 4, obj = 4)
        self._splaytree.insert(key = 6, obj = 6)
        
        self._splay_tree_node_count = 10
    
    def test_has_key_with_10_node(self):
        for i in range(1, 11): # 1 to 10
            self.assertEqual(i in self._splaytree, True, 'has_key operation must return True for existing key.')
    
    def tearDown(self):
        self._splaytree = None
#
#Splay tree tests that do ops and check nodes with in-order traversal
#
class Splay_Tree_Test_Tree_Structure_After_Insert_With_Inorder_Traversal(unittest.TestCase):
    '''
    The purpose of this test is to make sure that the splay op does not ruin the tree. So after each insert we check the
    tree structure.
    '''
    def setUp(self):
        self._splaytree = SplayTree()
        
    def test_tree_structure_after_each_insert_with_inorder_traversal(self):
        expected_inorder_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        inorder_from_tree = []
        for i in range(1, 11): # 1 to 10
            self._splaytree.insert(i, i)
            for key, element in self._splaytree.traversal(want_in_order = True):
                inorder_from_tree.append(element)
            self.assertEqual(inorder_from_tree, expected_inorder_list[:len(inorder_from_tree)], 'Tree ruined during insert splays')
            inorder_from_tree = []
        
    def tearDown(self):
        self._splaytree = None

class Splay_Tree_Test_Tree_Structure_After_Delete_With_Inorder_Traversal(unittest.TestCase):
    '''
    The purpose of this test is to make sure that the splay op does not ruin the tree. So after each insert we check the
    tree structure.
    '''
    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 5, obj = 5)
        self._splaytree.insert(key = 8, obj = 8)
        self._splaytree.insert(key = 7, obj = 7)
        self._splaytree.insert(key = 9, obj = 9)
        self._splaytree.insert(key = 10, obj = 10)
        self._splaytree.insert(key = 2, obj = 2)
        self._splaytree.insert(key = 1, obj = 1)
        self._splaytree.insert(key = 3, obj = 3)
        self._splaytree.insert(key = 4, obj = 4)
        self._splaytree.insert(key = 6, obj = 6)

    def test_tree_structure_after_each_delete_with_inorder_traversal(self):
        expected_inorder_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        inorder_from_tree = []
        for i in range(1, 11): # 1 to 10
            self._splaytree.remove(i)
            for key, element in self._splaytree.traversal(want_in_order = True):
                inorder_from_tree.append(element)
            self.assertEqual(inorder_from_tree, expected_inorder_list[i:10], 'Tree ruined during insert splays')
            inorder_from_tree = []
        
    def tearDown(self):
        self._splaytree = None


class Splay_Tree_Test_Tree_Structure_After_Find_With_Inorder_Traversal(unittest.TestCase):
    '''
    The purpose of this test is to make sure that the splay op does not ruin the tree. So after each insert we check the
    tree structure.
    '''
    def setUp(self):
        self._splaytree = SplayTree()
        self._splaytree.insert(key = 5, obj = 5)
        self._splaytree.insert(key = 8, obj = 8)
        self._splaytree.insert(key = 7, obj = 7)
        self._splaytree.insert(key = 9, obj = 9)
        self._splaytree.insert(key = 10, obj = 10)
        self._splaytree.insert(key = 2, obj = 2)
        self._splaytree.insert(key = 1, obj = 1)
        self._splaytree.insert(key = 3, obj = 3)
        self._splaytree.insert(key = 4, obj = 4)
        self._splaytree.insert(key = 6, obj = 6)

    def test_tree_structure_after_each_find_with_inorder_traversal(self):
        expected_inorder_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        inorder_from_tree = []
        for i in range(1, 11): # 1 to 10
            self.assertEqual(self._splaytree.find(i), i, 'Element not found in Splay Tree!')
            for key, element in self._splaytree.traversal(want_in_order = True):
                inorder_from_tree.append(element)
            self.assertEqual(inorder_from_tree, expected_inorder_list, 'Tree ruined during insert splays')
            inorder_from_tree = []
        
    def tearDown(self):
        self._splaytree = None

#Allows running as python run.
if __name__ == '__main__':
    print('Splaytree tests')
    unittest.main()