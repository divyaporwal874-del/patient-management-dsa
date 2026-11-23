"""Intelligent Patient-Based Management System (DSA-II, BCSE0401)

Data structures used:
  AVLTree       - patient records, key = patient ID (self-balancing BST)
  BST           - plain BST, kept only to compare its height with the AVL tree
  PriorityQueue - max-heap, the most urgent patient is called first
"""
from dataclasses import dataclass, field
from itertools import count


@dataclass
class Patient:
    pid: int
    name: str
    age: int
    priority: int = 1  # 1 = routine ... 5 = emergency
    history: list = field(default_factory=list)
    appointments: list = field(default_factory=list)


# ---------------- AVL tree ----------------
class Node:
    def __init__(self, patient):
        self.patient = patient
        self.left = None
        self.right = None
        self.height = 1


def height(n):
    return n.height if n else 0


def update_height(n):
    n.height = 1 + max(height(n.left), height(n.right))


def balance(n):
    return height(n.left) - height(n.right) if n else 0


def rotate_right(y):
    x = y.left
    y.left = x.right
    x.right = y
    update_height(y)
    update_height(x)
    return x


def rotate_left(x):
    y = x.right
    x.right = y.left
    y.left = x
    update_height(x)
    update_height(y)
    return y


class AVLTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, patient):
        self.root = self._insert(self.root, patient)

    def _insert(self, node, p):
        if node is None:
            self.size += 1
            return Node(p)
        if p.pid < node.patient.pid:
            node.left = self._insert(node.left, p)
        elif p.pid > node.patient.pid:
            node.right = self._insert(node.right, p)
        else:
            raise ValueError("Patient ID already exists")
        update_height(node)
        b = balance(node)
        if b > 1 and p.pid < node.left.patient.pid:      # left-left
            return rotate_right(node)
        if b < -1 and p.pid > node.right.patient.pid:    # right-right
            return rotate_left(node)
        if b > 1:                                        # left-right
            node.left = rotate_left(node.left)
            return rotate_right(node)
        if b < -1:                                       # right-left
            node.right = rotate_right(node.right)
            return rotate_left(node)
        return node

    def search(self, pid):
        node = self.root
        while node:
            if pid == node.patient.pid:
                return node.patient
            node = node.left if pid < node.patient.pid else node.right
        return None

    def inorder(self):
        stack, node = [], self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.patient
            node = node.right

    def height(self):
        return height(self.root)


# ---------------- plain BST (for comparison only) ----------------
class BST:
    def __init__(self):
        self.root = None

    def insert(self, pid):
        new = Node(Patient(pid, "", 0))
        if self.root is None:
            self.root = new
            return
        cur = self.root
        while True:
            if pid < cur.patient.pid:
                if cur.left is None:
                    cur.left = new
                    return
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = new
                    return
                cur = cur.right

    def height(self):
        best, stack = 0, [(self.root, 1)] if self.root else []
        while stack:
            node, d = stack.pop()
            best = max(best, d)
            for child in (node.left, node.right):
                if child:
                    stack.append((child, d + 1))
        return best


# ---------------- priority queue (max-heap) ----------------
class PriorityQueue:
    """Higher priority first; same priority -> who arrived first."""

    def __init__(self):
        self.a = []
        self.arrival = count()

    def __len__(self):
        return len(self.a)

    def push(self, patient):
        self.a.append((patient.priority, -next(self.arrival), patient))
        i = len(self.a) - 1
        while i > 0 and self.a[(i - 1) // 2][:2] < self.a[i][:2]:
            parent = (i - 1) // 2
            self.a[parent], self.a[i] = self.a[i], self.a[parent]
            i = parent

    def pop(self):
        if not self.a:
            return None
        top = self.a[0][2]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            i = 0
            while True:
                big, l, r = i, 2 * i + 1, 2 * i + 2
                if l < len(self.a) and self.a[l][:2] > self.a[big][:2]:
                    big = l
                if r < len(self.a) and self.a[r][:2] > self.a[big][:2]:
                    big = r
                if big == i:
                    break
                self.a[i], self.a[big] = self.a[big], self.a[i]
                i = big
        return top


# ---------------- the system ----------------
class PatientSystem:
    def __init__(self):
        self.records = AVLTree()
        self.queue = PriorityQueue()
        self.waiting = set()

    def _get(self, pid):
        p = self.records.search(pid)
        if p is None:
            raise KeyError(f"No patient with ID {pid}")
        return p

    @staticmethod
    def _check(age, priority):
        if age < 0 or age > 120:
            raise ValueError("Age must be between 0 and 120")
        if priority not in (1, 2, 3, 4, 5):
            raise ValueError("Priority must be 1 to 5")

    def register(self, pid, name, age, priority=1):
        self._check(age, priority)
        self.records.insert(Patient(pid, name, age, priority))

    def find(self, pid):
        return self.records.search(pid)

    def update(self, pid, name=None, age=None, priority=None):
        p = self._get(pid)
        self._check(p.age if age is None else age, p.priority if priority is None else priority)
        if name is not None:
            p.name = name
        if age is not None:
            p.age = age
        if priority is not None:
            p.priority = priority  # applies the next time the patient joins the queue
        return p

    def add_history(self, pid, note):
        self._get(pid).history.append(note)

    def get_history(self, pid):
        return list(self._get(pid).history)

    def book_appointment(self, pid, date, doctor):
        self._get(pid).appointments.append((date, doctor))

    def add_to_queue(self, pid):
        p = self._get(pid)
        if pid in self.waiting:
            raise ValueError("Patient is already waiting")
        self.queue.push(p)
        self.waiting.add(pid)

    def call_next(self):
        p = self.queue.pop()
        if p:
            self.waiting.discard(p.pid)
        return p


# ---------------- simple menu ----------------
MENU = """
1. Register patient          6. Book appointment
2. Search patient by ID      7. Add patient to waiting queue
3. Update patient details    8. Call next patient
4. Add medical history note  9. List all patients
5. View medical history      0. Exit"""


def main():
    ps = PatientSystem()
    while True:
        print(MENU)
        c = input("Choose: ").strip()
        if c == "0":
            break
        try:
            if c == "1":
                ps.register(int(input("ID: ")), input("Name: "), int(input("Age: ")),
                            int(input("Priority (1 routine - 5 emergency): ")))
                print("Registered.")
            elif c == "2":
                print(ps.find(int(input("ID: "))) or "Not found.")
            elif c == "3":
                pid, f = int(input("ID: ")), input("Field (name/age/priority): ").strip()
                v = input("New value: ")
                ps.update(pid, **{f: v if f == "name" else int(v)})
                print("Updated.")
            elif c == "4":
                ps.add_history(int(input("ID: ")), input("Note: "))
                print("Saved.")
            elif c == "5":
                print(*ps.get_history(int(input("ID: "))) or ["No history."], sep="\n")
            elif c == "6":
                ps.book_appointment(int(input("ID: ")), input("Date: "), input("Doctor: "))
                print("Booked.")
            elif c == "7":
                ps.add_to_queue(int(input("ID: ")))
                print("Added to queue.")
            elif c == "8":
                print(ps.call_next() or "Queue is empty.")
            elif c == "9":
                for p in ps.records.inorder():
                    print(p.pid, p.name, p.age, "priority", p.priority)
            else:
                print("Invalid choice.")
        except (ValueError, KeyError, TypeError) as e:
            print("Error:", e)


if __name__ == "__main__":
    main()