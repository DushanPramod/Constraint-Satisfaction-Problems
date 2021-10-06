from csp import Constraint, CSP
from typing import Dict, List, Optional
import csv

class CompulsorySubjectConstraint(Constraint[str, str]):
    def __init__(self, subjects: List[str]) -> None:
        super().__init__(subjects)
        self.subjects: List[str] = subjects

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        for sub1, slot1 in assignment.items():
            if(sub1 in self.subjects):
                for sub2, slot2 in assignment.items():
                    temp1 = slot1.split()[0]
                    temp2 = slot2.split()[0]
                    if(sub1 != sub2 and temp1 == temp2):
                        return False
        return True

class RoomConstraint(Constraint[str,str]):
    def __init__(self) -> None:
        super().__init__([])

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        for sub1, slot1 in assignment.items():
            for sub2, slot2 in assignment.items():
                if(sub1!=sub2 and slot1==slot2):
                    return False
        return True


def ReadCSV():
    file = open('Input.csv')
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    file.close()

    rooms: List[str] = [i for i in rows[-1] if i != '']

    variables: List[str] = [i[0] for i in rows[:len(rows)-1]]
    domains: Dict[str, List[str]] = {i[0]:[x+ " " + y for x in i[2:] for y in rooms] for i in rows[:len(rows)-1]}
    compulsory_subject = [i[0] for i in rows[:len(rows)-1] if i[1]=="c"]

    return variables, domains,compulsory_subject

def WriteCSV(data):
    filename = 'Output.csv'
    with open(filename, 'w', newline="") as file:
        csvwriter = csv.writer(file)  # 2. create a csvwriter object
        csvwriter.writerows(data)  # 5. write the rest of the data


if __name__ == "__main__":
    variables, domains ,compulsory_subject = ReadCSV()

    csp: CSP[str, str] = CSP(variables, domains)
    csp.add_constraint(CompulsorySubjectConstraint(compulsory_subject))
    csp.add_constraint(RoomConstraint())

    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print(solution)
        WriteCSV([[sub, slot.split()[0], slot.split()[1]] for sub, slot in solution.items()])




