from random import randint, sample
import sqlite3
import csv

class Competitor():
    def __init__(self, name):
        self.name = name
        self.scores = []
        self.total = 0.0
    
    def totalScore(self):
        self.total = round((sum(self.scores)/len(self.scores)), 2)
    
    def __str__(self):
        s = ",".join([str(x) for x in self.scores])
        return f"{i.name:>10}: {i.total:>5} ({s})\n"

class Tournament():
    def __init__(self, name):
        self.name = name
        self.competitors = []

    def set_comps(self, comp_list):
        self.competitors = comp_list

def new_tournament(t_name_unsafe, comp_list):
    with sqlite3.connect('thunderdome.db') as conn:
        c = conn.cursor()
        t_name = ''.join(i for i in t_name_unsafe if i.isalnum())
        c.execute("""CREATE TABLE IF NOT EXISTS """+t_name+""" (Name,
                Total, Scores)""")
        for i in comp_list.split(", "):
            x = (i, 0.0, 'none')
            c.execute("INSERT INTO "+t_name+" VALUES (?,?,?)", x)
        conn.commit()
    tourn = Tournament(t_name)
    tourn.set_comps([Competitor(i) for i in comp_list.split(", ")])
    return tourn

# Loads a list of competitors from a csv file.
def load_competitors():
    l = []
    with open("names", "r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            c = Competitor(row[0])
            if len(row) > 1:
                c.scores = [int(x) for x in row[1:]]
                c.totalScore()
            l.append(c)
    return l

# Writes a list of competitors and their scores to a csv file.
def saveComps(compList):
    with open("names", "w+", newline='') as f:
        writer = csv.writer(f)
        for i in compList:
            writer.writerow([i.name]+i.scores)

# Recursively constructs a list of brackets. Each bracket is itself a list of
# 4 competitors. 
def new_bracket(compList):
    if len(compList) <= 4:
        return [compList]
    else:
        z = [compList[0:4]]
        z += new_bracket(compList[4:])
        return z 

# Sorts the list of competitors in place based on the "total" attribute
# of each Competitor object. '''
def sortComps(compList):
    compList.sort(key=lambda x: x.total, reverse=True)

# Randomly assigns a win position to the competitors
# Simply for testing, not intended for actual use '''
def randBracketWin(compList):
    c = sample(compList, len(compList))
    score_bracket(c)

# Given a particular bracket, displays it to the user and asks them to 
# input the names of the competitors in the order of winning place. Uses
# nested list comprehension to sort the bracket according to the user's
# input. 
def run_bracket(bracket):
    print(f"\nThe next bracket is:\n{', '.join([x.name for x in bracket])}.")
    print(f"Please enter the results in order of place, separated by commas and spaces:")
    places = input(">> ").split(", ")
    # Need to add error checking, make sure given names are in this bracket
    results = [comp for name in places for comp in bracket if comp.name == name]
    return results

def score_bracket(results):
    # Need to adjust this. Currently gives low points to winner of smaller
    # brackets, making it impossible after a few rounds to get out of the
    # bottom
    # bracket. Adjust as follows: Take a set number, divide by the factorial of
    # the number of competitors; ie if number = 10 and competitors = 4, 10 / !4.
    # Award number of points equal to reverse placement; ie 1st place gets 4
    # parts. 
    score = len(results)
    for i in results:
        i.scores.append(score)
        score-=1

# ---------------------------------------------------
# Main
# ---------------------------------------------------
if __name__=="__main__":    
    comps = load_competitors()
    print(", ".join([i.name for i in comps]))

    print("\nBrackets:\n-----------")
    brackets = new_bracket(comps)
    counter = 1
    for i in brackets:
        print(counter, end=": ")
        print(", ".join([x.name for x in i]))
        counter+=1
    
    for i in brackets:
        randBracketWin(i)
        #score_bracket(run_bracket(i))
    for i in comps:
        i.totalScore()
    sortComps(comps)
    saveComps(comps)
    
    st = "\nScores\n----------\n"
    for i in comps:
        st = st + str(i)
    print(st+"\n")
