#!/usr/bin/python
import heapq
import copy
import sys
from random import randrange

inputFile = ""
solseq = False
pcost = False
nvisited = -1
heuristic_type = 0
rand = False
N = 0
M = 0

row = [1, 0, -1, 0]
col = [0, -1, 0, 1]
generatedPuzzles = []
solvedPuzzle = []
puzzle = []

def isSafe(i,j):
  global N
  return i >= 0 and i < N and j >= 0 and j < N

def search(puzzle):
  for i in range(len(puzzle)):
    for j in range(len(puzzle)):
      if puzzle[i][j] == 0:
        return (i,j)
            
def swap(puzzle, row1,col1,row2,col2):
  newPuzzle = copy.deepcopy(puzzle)
  v = newPuzzle[row1][col1]
  newPuzzle[row1][col1] = newPuzzle[row2][col2]
  newPuzzle[row2][col2] = v
  return newPuzzle
    
def printPuzzle(puzzle):
    for i in range (len(puzzle)):
        for j in range (len(puzzle)):
            print(str(puzzle[i][j]), end=" ")
        print(end="\n")
    print(end="\n")

def readFromFile():
  global N, puzzle
  f = open(inputFile,"r")
  for line in f.readlines():
    puzzle.append( [ int (x) for x in line.split(" ") ] )
  return puzzle

def readFromStdin():
  global puzzle, N
  puzzle = []
  N = int(input("Enter the number of square tiles in the puzzle (8 or 15): ")) 
  if(N == 8):
    N = 3
  elif(N == 15):
    N = 4
  else:
    print("This program can solve only 8 and 15 puzzles..")
    sys.exit(2)
  print("Please give the shuffled puzzle to solve. Separate the numbers with new line")
  puzzle = []
  for i in range(N):
    puzzle.append([])
    for j in range(N):
      puzzle[i].append(int(input()))
  printPuzzle(puzzle)
  if(input("You just entered this puzzle.Do you want to continue with this puzzle? Write no if you want to reenter the puzzle or press Enter: ") == "no"):
    readFromStdin()
  else:
    return puzzle

def main():
  global N, puzzle
  puzzle = []
  argvProcessing()
  solvedPuzzle = createSolvedPuzzle()
  if(rand == True):
    puzzle = shufflePuzzle()
  elif(inputFile != ""):
    puzzle = readFromFile()
    N = len(solvedPuzzle)
  else:
    puzzle = readFromStdin()
  if(heuristic_type != "1" and heuristic_type != "2"):
      print("You must give a heuristic type (Hamming = 1, Manhattan = 2)")
      sys.exit(2)
  elif(heuristic_type == "1"):
      cost = Hamming_dist_calc(puzzle)
  elif(heuristic_type == "2"):
      cost = Manhattan_dist_calc(puzzle)
  position = search(puzzle)
  heap = []
  heapq.heapify(heap)
  heapq.heappush(heap, (cost, puzzle, 0))
  que_solve(heap, position)

def alreadyGenerated(puzzle):
  for i in generatedPuzzles:
    if(puzzle == i):
      return True
  return False
  
def argvProcessing():
  global solseq,pcost,nvisited,heuristic_type,rand,N,M,inputFile
  length = len(sys.argv)
  for i in range(length):
    if sys.argv[i] == '-input':
      inputFile=(sys.argv[i+1])
    elif sys.argv[i] == '-solseq':
      solseq = True
    elif sys.argv[i] == '-pcost':
      pcost = True
    elif sys.argv[i] == '-nvisited':
      nvisited = 0
    elif sys.argv[i] == '-h':
      if(i == length - 1):
        print("You must give a heuristic type like: -h 1 or -h 2")
        sys.exit(2)
      else:
        heuristic_type = sys.argv[i+1]
    elif sys.argv[i] == '-rand':
      rand = True
      N = int(sys.argv[i+1])
      if(N == 8):
        N = 3
      elif(N == 15):
        N = 4
      else:
        print("The program can only solve 8- and 15-puzzles")
        sys.exit(2)
      M = int(sys.argv[i+2])
    
def Hamming_dist_calc(puzzle):
    count = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if(puzzle[i][j] != 0 and puzzle[i][j] != solvedPuzzle[i][j]):
                count+=1
    return count

def Manhattan_dist_calc(puzzle):
  manhattan_distance = 0
  temp_array=[]
  for i in range(len(puzzle)):
    for j in range(len(puzzle)):
      temp_array.append(puzzle[i][j])
  for i in range(len(temp_array)):
    if(i == len(temp_array) - 1):
      break
    if(temp_array[i] != i+1):
      manhattan_distance += abs((temp_array[i]//len(puzzle)) - ((i+1)//len(puzzle))) + abs((temp_array[i]%len(puzzle)) - ((i+1)%len(puzzle)))
  return manhattan_distance
      
    
def path_finder(position, puzzle, oldCost,lepes, heap):
  global nvisited, row, col
  for i in range(4):
    if (isSafe(position[0] + row[i],position[1] + col[i])):
      newPuzzle = swap(puzzle, position[0],position[1],position[0] + row[i], position[1] + col[i])
      if(heuristic_type == "1"):
        newCost = lepes + Hamming_dist_calc(newPuzzle)
        if(not alreadyGenerated(newPuzzle) and newCost <= oldCost +1):
          heapq.heappush(heap, (newCost, newPuzzle, lepes+1))
          if(nvisited > -1):
            nvisited+=1
          generatedPuzzles.append(newPuzzle)
      else:
        
        newCost = lepes + Manhattan_dist_calc(newPuzzle)
        if(not alreadyGenerated(newPuzzle) and newCost - lepes <= oldCost ):
          heapq.heappush(heap, (newCost, newPuzzle, lepes+1))
          if(nvisited > -1):
            nvisited+=1
          generatedPuzzles.append(newPuzzle)
      
      
def que_solve(heap, position):
  while(len(heap) != 0):
    currentHeapElement = heapq.heappop(heap)
    position = search(currentHeapElement[1])
    puzzle = currentHeapElement[1]
    if (currentHeapElement[2] > 31):
      break;
    if(puzzle == solvedPuzzle):
      print("Megoldas")
      if(pcost == True):
        print("Koltseg: " + str(currentHeapElement[0]))
      if(nvisited > -1):
        print("Meglatogatott csomopontok szama: " + str(nvisited))
      printPuzzle(currentHeapElement[1])
      break
    cost = currentHeapElement[0]
    if(solseq == True):
      printPuzzle(currentHeapElement[1])
    path_finder(position, puzzle, cost, currentHeapElement[2], heap)

def createSolvedPuzzle():
  global solvedPuzzle
  N = 3
  count = 1
  for i in range(N):
    solvedPuzzle.append([])
    for j in range(N):
      if(count == N*N):
        solvedPuzzle[i].append(0)
      else:
        solvedPuzzle[i].append(count)
      count+=1
  return solvedPuzzle

def shufflePuzzle():
  global solvedPuzzle, puzzle
  puzzle = copy.deepcopy(solvedPuzzle)
  position = (N-1, N-1)
  count = 0
  while(count < M):
    directionIndex = randrange(0, 3)
    if (isSafe(position[0]+row[directionIndex], position[1]+col[directionIndex])):
      puzzle = swap(puzzle, position[0],position[1],position[0] + row[directionIndex], position[1] + col[directionIndex])
      count+=1
      position = search(puzzle)
  if(puzzle == solvedPuzzle):
    shufflePuzzle(puzzle)
  else:
    return puzzle

main()