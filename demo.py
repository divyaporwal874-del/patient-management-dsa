"""Demo: runs the patient system on sample data and prints every step.
Run with:  python demo.py   (no typing needed)"""
from patient_system import PatientSystem, AVLTree, BST, Patient

ps = PatientSystem()

print("1. Registering patients")
for pid, name, age, pr in [(101, "Asha", 30, 2), (102, "Ravi", 45, 5), (103, "Meena", 8, 3), (104, "Zoya", 22, 3)]:
    ps.register(pid, name, age, pr)
    print("   registered:", pid, name, "priority", pr)

print("\n2. Search by ID")
print("   101 ->", ps.find(101).name)
print("   999 ->", ps.find(999))

print("\n3. Update details")
ps.update(101, name="Asha Sharma", age=31)
print("   101 ->", ps.find(101).name, ps.find(101).age)

print("\n4. Medical history and appointment")
ps.add_history(101, "Fever, 2 days")
ps.book_appointment(101, "25-11-2026", "Dr. Gupta")
print("   history:", ps.get_history(101))
print("   appointments:", ps.find(101).appointments)

print("\n5. Waiting queue (served by priority, then arrival)")
for pid in (101, 102, 103, 104):
    ps.add_to_queue(pid)
while True:
    p = ps.call_next()
    if p is None:
        break
    print("   called:", p.pid, p.name, "priority", p.priority)

print("\n6. Tree balance with IDs 1..200 inserted in order")
avl, bst = AVLTree(), BST()
for i in range(1, 201):
    avl.insert(Patient(i, "x", 20))
    bst.insert(i)
print("   plain BST height:", bst.height())
print("   AVL tree height :", avl.height())