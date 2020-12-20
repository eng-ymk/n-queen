from time import time
from random import randint as rand, shuffle

class State:
    def __init__(self, initial):
        self.board = initial
        self.cost = self.h()

    def h(self):
        sum = 0
        for i in range(0, len(self.board)):
            for j in range(i + 1, len(self.board)):
                check = self.isAttacking(i, self.board[i], j, self.board[j])
                if check:
                    sum += 1
        return sum

    def isAttacking(self, x1, y1, x2, y2):
        # same row
        if x1 == x2:
            return True
        # same column
        if y1 == y2:
            return True
        # same diagonal
        if abs(x1 - x2) == abs(y2 - y1):
            return True
        return False

    def copyBoard(self):
        temp = list()
        for i in self.board:
            temp.append(i)
        return temp

    def asString(self,separator = '|',black = '▓',white = ' ',queen = 'Q'):
        str = ""
        board = self.board

        for i in range(0, len(board)):
            for j in range(0,len(board)):
                if board[j]== i:
                    str += queen + separator
                elif (i+j) % 2 == 0:
                    str += white + separator
                else:
                    str += black + separator
            str += "\n"
        return str

    @staticmethod
    def random(d):
        board = []
        for i in range(0,d):
            board.append(rand(0, d-1))
        return State(board)

class HC:
    def __init__(self,initialState):
        self.state = initialState
        self.solutions = list()
        self.d= len(initialState.board)
        self.runningTime = 0
        self.steps=0
        self.isFound=False
    
    def solve(self):
        if self.state.cost == 0:
            self.solutions.append(self.state.board)
            self.steps=0
            self.runningTime=0
            return
        
        start = time()

        BestCost = self.d * self.d
        print("[        Board        ]","( Cost )")
        while not self.isFound:
            for i in range(0,self.d):
                for j in range(0,self.d-1):
                    tempBoard = self.state.copyBoard()
                    tempBoard[i]= (tempBoard[i] + j + 1)% self.d
                    tempState = State(tempBoard)
                    if(tempState.cost < BestCost):
                        BestCost = tempState.cost
                        self.solutions.clear()
                        self.solutions.append([i,tempBoard[i]])
                    elif tempState.cost == BestCost:
                        self.solutions.append([i,tempBoard[i]])
                    if (BestCost == 0):
                        self.isFound =True
            if len(self.solutions) == 0:
                break

            
            randomIndex = rand(0, len(self.solutions)-1)
            randomSolution = self.solutions[randomIndex]
            self.state.board[randomSolution[0]] = randomSolution[1]
            print(self.state.board,"(",BestCost,")")
            self.steps = self.steps + 1
            self.solutions = list()
            

        end = time()
        self.runningTime=end-start
        
    def result(self,path):
        print("Solved : ", self.isFound)
        print("Time : ", self.runningTime, "s")
        print("Steps : ", self.steps)
        print("Solution : ", self.state.board)
        print("Board: \n{}".format(self.state.asString()))
        
        outputsFile = open(path, "w")
        outputsFile.write("Solved : {}\n".format(self.isFound))
        outputsFile.write("Time : {} s\n".format(self.runningTime))
        outputsFile.write("Steps : {}\n".format(self.steps))
        outputsFile.write("Solution : {}\n".format(self.state.board))
        outputsFile.write("Board: \n{}".format(self.state.asString(' ','#','#')))
        outputsFile.close()

def readFile(path):
        with open(path) as f:
            content = f.readlines()
        content = [x.split() for x in content]
        temp=[0]*len(content)
        for i in range(0,len(content)):
            for j in range(0,len(content[i])):
                if(content[i][j] == 'Q'):
                    temp[j]=i
        return temp

board = readFile('Input.txt')
initialSate=State(board)
#initialSate=State.random(8)

agent = HC(initialSate)
agent.solve()
agent.result('Output.txt')
