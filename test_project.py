"""Run with:  python -m unittest -v test_project.py
Test names 1-7 match the rows of Table 1 in the report."""
import unittest
from patient_system import PatientSystem, AVLTree, BST, Patient
import algorithms as alg


class TestProject(unittest.TestCase):
    def setUp(self):
        self.ps = PatientSystem()
        self.ps.register(101, "Asha", 30, 2)
        self.ps.register(102, "Ravi", 45, 5)
        self.ps.register(103, "Meena", 8, 3)

    def test_1_record_entry(self):
        self.assertEqual(self.ps.records.size, 3)
        self.ps.register(104, "Kabir", 60, 1)
        self.assertEqual(self.ps.records.size, 4)
        with self.assertRaises(ValueError):
            self.ps.register(104, "Duplicate", 20, 1)       # same ID not allowed
        with self.assertRaises(ValueError):
            self.ps.register(105, "Bad age", 200, 1)        # invalid age

    def test_2_search_patient(self):
        self.assertEqual(self.ps.find(102).name, "Ravi")
        self.assertIsNone(self.ps.find(999))

    def test_3_update_details(self):
        self.ps.update(101, name="Asha Sharma", age=31)
        p = self.ps.find(101)
        self.assertEqual((p.name, p.age), ("Asha Sharma", 31))

    def test_4_medical_history(self):
        self.ps.add_history(101, "Fever, 2 days")
        self.ps.add_history(102, "Chest pain")
        self.assertEqual(self.ps.get_history(101), ["Fever, 2 days"])
        self.assertEqual(self.ps.get_history(103), [])

    def test_5_priority_handling(self):
        for pid in (101, 102, 103):
            self.ps.add_to_queue(pid)
        self.ps.register(104, "Zoya", 22, 3)
        self.ps.add_to_queue(104)
        order = [self.ps.call_next().pid for _ in range(4)]
        self.assertEqual(order, [102, 103, 104, 101])       # 5, 3 (first), 3 (later), 2
        self.assertIsNone(self.ps.call_next())

    def test_6_tree_balance(self):
        avl, bst = AVLTree(), BST()
        for pid in range(1, 201):                           # IDs in increasing order
            avl.insert(Patient(pid, "x", 20))
            bst.insert(pid)
        self.assertEqual(bst.height(), 200)                 # plain BST becomes a chain
        self.assertLessEqual(avl.height(), 9)               # AVL stays balanced
        self.assertTrue(all(avl.search(pid) for pid in range(1, 201)))
        ids = [p.pid for p in avl.inorder()]
        self.assertEqual(ids, sorted(ids))

    def test_7_algorithm_practice(self):
        self.assertEqual(alg.matrix_chain([10, 30, 5, 60]), 4500)
        self.assertEqual(alg.matrix_chain([30, 35, 15, 5, 10, 20, 25]), 15125)
        self.assertEqual(alg.knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7), (9, [1, 2]))
        self.assertEqual(alg.n_queens(4)[0], 2)
        self.assertEqual(alg.n_queens(8)[0], 92)
        g1 = [[0, 1, 0, 1, 0], [1, 0, 1, 1, 1], [0, 1, 0, 0, 1], [1, 1, 0, 0, 1], [0, 1, 1, 1, 0]]
        g2 = [[0, 1, 0, 1, 0], [1, 0, 1, 1, 1], [0, 1, 0, 0, 1], [1, 1, 0, 0, 0], [0, 1, 1, 0, 0]]
        self.assertIsNotNone(alg.hamiltonian_cycle(g1))
        self.assertIsNone(alg.hamiltonian_cycle(g2))
        c = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
        self.assertEqual(alg.tsp_branch_and_bound(c), 80)
        self.assertEqual(alg.tsp_branch_and_bound(c), alg.tsp_brute_force(c))


if __name__ == "__main__":
    unittest.main()