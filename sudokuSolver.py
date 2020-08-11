import stolendoku as s
from itertools import product

bounds = range(0,9)

def rowscan(board,row,num):
    for c in bounds:
        if board[row][c] == num:
            return True
    return False

def colscan(board,col,num):
    for r in bounds:
        if board[r][col] == num:
            return True
    return False

def boxrange(row,col):
    range1 = range(0,3)
    range2 = range(3,6)
    range3 = range(6,9)
    #set bounds of box
    if row in range1:
        rowrange = range1
    elif row in range2:
        rowrange = range2
    else:
        rowrange = range3
    
    if col in range1:
        colrange = range1
    elif col in range2:
        colrange = range2
    else:
        colrange = range3
    
    return rowrange,colrange

def boxscan(board,row,col,num):
    rowrange,colrange = boxrange(row,col) #sets bounds of current box  
    for r,c in product(rowrange,colrange):
        if board[r][c] == num:
            return True
    return False

def removeAt(notes,row,col,num):
    #row
    for c in bounds:
        if num in notes[row][c]:
            notes[row][c].remove(num)
    #col
    for r in bounds:
        if num in notes[r][col]:
            notes[r][col].remove(num)
    #box
    rowrange,colrange = boxrange(row,col)
    for r,c in product(rowrange,colrange):
        if num in notes[r][c]:
            notes[r][c].remove(num)

def solveS(board):
    notes = [
        [[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[]],
    ]
    for row,col,num in product(bounds,bounds,range(1,10)):
        if rowscan(board,row,num):#if count of num > 0, funct returns true
            continue
        if colscan(board,col,num):
            continue
        if boxscan(board,row,col,num):
            continue
        notes[row][col].append(num)#else append to list of possible choices

    while(True):
        loop = False
        #single solution check
        for r,c in product(bounds,bounds):
            if board[r][c] == 0 and len(notes[r][c]) == 1:
                currentnum = notes[r][c].pop()
                board[r][c] = currentnum
                removeAt(notes,r,c,currentnum)
                loop=True
        #single box checks
        fullset = set(list(range(0,10)))
        #row
        for r in bounds:
            #single empty square in row check
            rowcount = 0
            for c in bounds:
                if board[r][c] != 0:
                    rowcount += 1
            if rowcount == 8:
                thisset = set(board[r])
                currentnum = (fullset-thisset).pop()
                loop = True
                for c in bounds:
                    if board[r][c] == 0:
                        board[r][c] = currentnum
                        removeAt(notes,r,c,currentnum)#maybe change this so that it goes back to single solution check upon a box check
                        break
            #single possible location for value from notes check
            for n in range(1,10):
                ncount = 0
                lastr = -1
                lastc = -1
                for c in bounds:
                    if n in notes[r][c]:
                        ncount += 1
                        lastr = r
                        lastc = c
                if ncount == 1:
                    loop = True
                    board[lastr][lastc] = n
                    removeAt(notes,lastr,lastc,n)

        #col
        for c in bounds:
            #single square in col check
            colcount = 0
            for r in bounds:
                if board[r][c] != 0:
                    colcount += 1
            if colcount == 8:
                loop = True
                thiscol = [0,0,0,0,0,0,0,0,0]
                for r in bounds:
                    thiscol[r] = board[r][c]
                thisset = set(thiscol)
                currentnum = (fullset-thisset).pop()
                for r in bounds:
                    if board[r][c] == 0:
                        board[r][c] = currentnum
                        removeAt(notes,r,c,currentnum)
                        break
            #single possible location in col/notes check
            for n in range(1,10):
                ncount = 0
                lastr = -1
                lastc = -1
                for r in bounds:
                    if n in notes[r][c]:
                        ncount += 1
                        lastr = r
                        lastc = c
                if ncount == 1:
                    loop = True
                    board[lastr][lastc] = n
                    removeAt(notes,lastr,lastc,n)


        #square
        for sr,sc in product(range(0,3),range(0,3)):
            rowrange,colrange = boxrange(sr*3,sc*3)
            #single box check
            boxcount = 0
            for r,c in product(rowrange,colrange):
                if board[r][c] != 0:
                    boxcount += 1
            if boxcount == 8:
                loop = True
                thisbox = [0,0,0,0,0,0,0,0,0]
                i = 0
                for r,c in product(rowrange,colrange):
                    thisbox[i] = board[r][c]
                    i+=1
                thisset = set(thisbox)
                currentnum = (fullset-thisset).pop()
                for i in bounds:
                    if thisbox[i] == 0:
                        r,c = list(product(rowrange,colrange))[i]
                        board[r][c] = currentnum
                        removeAt(notes,r,c,currentnum)
                        break
            #single instance check
            for n in range(1,10):
                ncount = 0
                lastr = -1
                lastc = -1
                for r,c in product(rowrange,colrange):
                    if n in notes[r][c]:
                        ncount += 1
                        lastr = r
                        lastc = c
                if ncount == 1:
                    loop = True
                    board[lastr][lastc] = n
                    removeAt(notes,lastr,lastc,n)


                    
        if loop:
            continue
        else:
            break
        

    return board

def main():
    sudokustring = input("code?(Leave Blank for random board): ")
    if sudokustring:
        board = [[0 for c in bounds] for r in bounds]
        pbounds = list(product(bounds,bounds))
        for i in range(0,len(sudokustring)):
            r,c = pbounds[i]
            board[r][c] = int(sudokustring[i])

    else:
        board,correctBoard = s.makeSudoku()
        print("full puzzle: ")
        for r,c in product(bounds,bounds):
            print(f"{board[r][c]} ",end='')
        print()
        s.fancyPrint(correctBoard)

    s.fancyPrint(board)
    solved = solveS(board)
    s.fancyPrint(solved)
    
    if not sudokustring:
        if solved == correctBoard:
            print("correct")
        else:
            print("not quite there")
    
    

if __name__ == "__main__":
    main()
