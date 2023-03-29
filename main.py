'''To solve the task, I will use breadth-first search (BFS) of the graph, where each vertex will contain information about the state of the game. The initial state 
of the game is given as input, and vertices are connected only if it is possible to transition from one state to another. We want to reach the mate state for the
 white pieces in the smallest number of moves. States will be represented as numbers in the range [0, 524288], where each number is encoded with four blocks. 
The first block represents the current move, the second block represents the position of the white king, the third represents the position of the white rook, 
and the fourth represents the position of the black king. The board will be numbered as follows:
 8|  7  |  15  |  23  |  31  |  39  |  47  |  55  |  63  |
 7|  6  |  14  |  22  |  30  |  38  |  46  |  54  |  62  |
 6|  5  |  13  |  21  |  29  |  37  |  45  |  53  |  61  |
 5|  4  |  12  |  20  |  28  |  36  |  44  |  52  |  60  |
 4|  3  |  11  |  19  |  27  |  35  |  43  |  51  |  59  |
 3|  2  |  10  |  18  |  26  |  34  |  42  |  50  |  58  |
 2|  1  |  9   |  17  |  25  |  33  |  41  |  49  |  57  |
 1|  0  |  8   |  16  |  24  |  32  |  40  |  48  |  56  |
     a     b       c      d      e     f       g     h'''
from cmath import inf
import time
start_time = time.time()


def beating(b1, b2, c):  # beating of black king
    if b2[0] == c[0] or b2[1] == c[1]:
        return True


def no_escape(b1, b2, c):
    # on ends
    if (c[0] == 'a' and c[1] == '8'):
        if (b1[1] == '6' and (b1[0] == 'a' or b1[0] == 'b')) and b2[1] == '8':
            return True
        if (b1[0] == 'c' and (b1[1] == '7' or b1[1] == '8')) and b2[0] == 'a':
            return True
        return False
    elif (c[0] == 'a' and c[1] == '1'):
        if (b1[1] == '3' and (b1[0] == 'a' or b1[0] == 'b')) and b2[1] == '1':
            return True
        if (b1[0] == 'c' and (b1[1] == '1' or b1[1] == '2')) and b2[0] == 'a':
            return True
        return False
    elif (c[0] == 'h' and c[1] == '1'):
        if (b1[1] == '3' and (b1[0] == 'g' or b1[0] == 'h')) and b2[1] == '1':
            return True
        if (b1[0] == 'f' and (b1[1] == '1' or b1[1] == '2')) and b2[0] == 'h':
            return True
        return False
    elif (c[0] == 'h' and c[1] == '8'):
        if (b1[1] == '6' and (b1[0] == 'g' or b1[0] == 'h')) and b2[1] == '8':
            return True
        if (b1[0] == 'f' and (b1[1] == '7' or b1[1] == '8')) and b2[0] == 'h':
            return True
        return False
    elif c[1] == '8':
        if ord(b1[0]) == ord(c[0]) and ord(b1[1]) == ord(c[1])-2 and ord(b2[1]) == ord(c[1]):
            return True
        return False
    # the last row (without ends)
    elif c[1] == '1':
        if ord(b1[0]) == ord(c[0]) and ord(b1[1]) == ord(c[1])+2 and ord(b2[1]) == ord(c[1]):
            return True
        return False
    # the first column (without ends)
    elif c[0] == 'a':
        if ord(b1[1]) == ord(c[1]) and ord(b1[0]) == ord(c[0])+2 and ord(b2[0]) == ord(c[0]):
            return True
        return False
    # the last colum (without ends)
    elif c[0] == 'h':
        if ord(b1[1]) == ord(c[1]) and ord(b1[0]) == ord(c[0])-2 and ord(b2[0]) == ord(c[0]):
            return True
        return False
    return False


def mat(b1, b2, c):
    if beating(b1, b2, c) and no_escape(b1, b2, c):
        return True
    return False


def pat(b1, b2, c):
    if no_escape(b1, b2, c) and not beating(b1, b2, c):
        return True
    return False


def conv(w):  # changes e.g. from a8 to a number 7
    return (ord(w[1])-49)+(ord(w[0])-97)*8


def fromntochess(num):  # changes e.g. from 0 to a1 
    return chr(int(97+int((num - (num % 8))/8)))+chr(int(num % 8+49))


def move(curr_move):
    if curr_move == 'black':
        return 1
    else:
        return 0


# changes the list e.g. [1,'a1','a2','a3'] to a number corresponding to such a state
def state(line):
    return line[0] * 262144 + conv(line[1]) * 4096 + conv(line[2]) * 64 + conv(line[3])


def oksrod(bit, pos, king, w):  # checks if the move pos is "legal"
    # pos - new king position
    if bit == 1:
        pos_black_king = fromntochess(pos)
        pos_rook = fromntochess(w)
        if pos_black_king[0] == pos_rook[0] or pos_black_king[1] == pos_rook[1]:
            return False
    if pos - 1 == king or pos + 1 == king or pos - 9 == king or pos - 8 == king or pos - 7 == king or pos + 7 == king or pos + 8 == king or pos + 9 == king or pos - 9 == w or pos - 7 == w or pos + 7 == w or pos + 9 == w:
        return False
    return True


def new_king_move(bit, pos, king, rook):  # returns a list of new king moves
    res = []
    if pos % 8 != 0 and pos % 8 != 7 and pos > 7 and pos < 56:
        adjustment = [-1, 1, 8, -8, 7, -7, -9, 9]
        for i in adjustment:
            posnew = pos+i
            if posnew - 1 != king and posnew + 1 != king and posnew-9 != king and posnew-8 != king and posnew-7 != king and posnew+7 != king and posnew+8 != king and posnew+9 != king and posnew-1 != rook and posnew+1 != rook and posnew-9 != rook and posnew-8 != rook and posnew-7 != rook and posnew+7 != rook and posnew+8 != rook and posnew+9 != rook:
                if bit == 1:
                    if posnew % 8 != rook % 8 and chr(int(97+int((posnew - (posnew % 8))/8))) != chr(int(97+int((rook - (rook % 8))/8))):
                        res.append(posnew)
                else:
                    res.append(posnew)
    elif pos == 7:
        if (king != 5 and king != 13 and rook != 13 and rook > 7 and rook % 8 != 6):
            res.append(6)
        if (king != 5 and king != 13 and king != 21 and king != 22 and king != 23 and (rook < 8 or rook > 15) and rook != 5 and rook != 21 and rook != 22 and rook != 23 and rook % 8 != 6):
            res.append(14)
        if (king != 22 and king != 23 and rook != 22 and rook != 23 and rook % 8 != 7 and (rook < 8 or rook > 15)):
            res.append(15)
    elif pos == 0:
        if (king != 2 and king != 10 and rook != 10 and rook > 7 and rook % 8 != 1):
            res.append(1)
        if (king != 2 and king != 10 and king != 16 and king != 17 and king != 18 and (rook < 8 or rook > 15) and rook != 2 and rook != 16 and rook != 17 and rook != 18 and rook % 8 != 1):
            res.append(9)
        if (king != 16 and king != 17 and rook != 16 and rook != 17 and rook % 8 != 0 and (rook < 8 or rook > 15)):
            res.append(8)
    elif pos == 63:
        if (king != 53 and king != 61 and rook != 53 and rook != 61 and rook < 56 and rook % 8 != 6):
            res.append(62)
        if (king != 45 and king != 46 and king != 47 and king != 53 and king != 61 and (rook < 48 or rook > 55) and rook != 45 and rook != 46 and rook != 47 and rook != 61 and rook % 8 != 6):
            res.append(54)
        if (king != 46 and king != 47 and rook != 46 and rook != 47 and rook % 8 != 7 and (rook < 48 or rook > 55)):
            res.append(55)
    elif pos == 56:
        if (king != 50 and king != 58 and rook != 50 and rook != 58 and rook > 56 and rook % 8 != 1):
            res.append(57)
        if (king != 40 and king != 41 and king != 42 and king != 50 and king != 58 and (rook < 48 or rook > 55) and rook != 40 and rook != 41 and rook != 42 and rook != 50 and rook != 58 and rook % 8 != 1):
            res.append(49)
        if (king != 40 and king != 41 and rook != 40 and rook != 41 and rook % 8 != 0 and (rook < 48 or rook > 55)):
            res.append(48)
    elif pos > 0 and pos < 8:
        adjustment = [-1, 1, 7, 8, 9]
        for i in adjustment:
            posnew = pos+i
            if oksrod(bit, posnew, king, rook):
                res.append(posnew)
    elif pos < 64 and pos > 55:
        adjustment = [-1, 1, -7, -8, -9]
        for i in adjustment:
            posnew = pos+i
            if oksrod(bit, posnew, king, rook):
                res.append(posnew)
    elif pos % 8 == 0:
        adjustment = [-8, 8, 1, -7, 9]
        for i in adjustment:
            posnew = pos+i
            if oksrod(bit, posnew, king, rook):
                res.append(posnew)
    else:  # pos % 8 == 7
        adjustment = [-8, 8, -1, 7, -9]
        for i in adjustment:
            posnew = pos+i
            if oksrod(bit, posnew, king, rook):
                res.append(posnew)
    if res.count(rook) != 0:
        res.remove(rook)
    if res.count(king) != 0:
        res.remove(king)
    return res


def newmovewiezy(pos, kingb, kingcz):  # returns a list of new rook moves
    # pos - rook position
    res = []
    i = pos-8
    while i >= 0:
        if i == kingb or i == kingcz:
            i = -1
        if i != -1 and kingcz-1 != i and kingcz+1 != i and kingcz-9 != i and kingcz-8 != i and kingcz-7 != i and kingcz+7 != i and kingcz+8 != i and kingcz+9 != i:
            res.append(i)
        i = i-8
    i = pos+8
    while i <= 63:
        if i == kingb or i == kingcz:
            i = 64
        if i != 64 and kingcz-1 != i and kingcz+1 != i and kingcz-9 != i and kingcz-8 != i and kingcz-7 != i and kingcz+7 != i and kingcz+8 != i and kingcz+9 != i:
            res.append(i)
        i = i+8
    i = pos-1
    while i >= (pos//8)*8:
        if i == kingb or i == kingcz:
            i = (pos//8)*8-1
        if i != (pos//8)*8-1 and kingcz-1 != i and kingcz+1 != i and kingcz-9 != i and kingcz-8 != i and kingcz-7 != i and kingcz+7 != i and kingcz+8 != i and kingcz+9 != i:
            res.append(i)
        i = i-1
    i = pos+1
    while i <= 7+(pos//8)*8:
        if i == kingb or i == kingcz:
            i = 7+(pos//8)*8+1
        if i != 7+(pos//8)*8+1 and kingcz-1 != i and kingcz+1 != i and kingcz-9 != i and kingcz-8 != i and kingcz-7 != i and kingcz+7 != i and kingcz+8 != i and kingcz+9 != i:
            res.append(i)
        i = i+1
    if res.count(kingcz) != 0:
        res.remove(kingcz)
    if res.count(kingb) != 0:
        res.remove(kingb)
    return res


def stateprint(num):
    a = num % 64
    b = num//64 % 64
    c = num//4096 % 64
    print(fromntochess(c), fromntochess(b), fromntochess(a))


def path(pop, a, b):  # print the shortest path in the state graph that led to the mat
    if pop[b] == a:
        print(stateprint(a))
    else:
        path(pop, a, pop[b])
        print(stateprint(b))


with open('zad1_input.txt') as plik:
    for line in plik:
        line = line.strip().split()
        prev, od, kolejka = [], [], []
        pocz, end, wend = 0, 0, 0
        minpath = inf
        line.insert(0, move(line[0]))
        line.remove(line[1])
        for i in range(0, 524288):
            od.append(-1)
            prev.append(-1)
        # BFS
        start_state = state(line)
        kolejka.append(start_state)
        od[start_state] = 0
        while end+1 != pocz:
            u = kolejka[pocz]
            pocz = pocz+1
            aktstate = u
            pos_black_ = aktstate % 64
            aktstate //= 64
            pos_rook = aktstate % 64
            aktstate //= 64
            pos_king = aktstate % 64
            aktstate //= 64
            move = aktstate % 64
            # generating all neighbors in the state graph
            if move == 1:  # move of a black king
                tab = new_king_move(move, pos_black_, pos_king, pos_rook)
                for e in tab:
                    newstate = state(
                        [0, fromntochess(pos_king), fromntochess(pos_rook), fromntochess(e)])
                    if od[newstate] == -1:
                        od[newstate] = od[u]+1
                        if mat(fromntochess(pos_king), fromntochess(pos_rook), fromntochess(e)):
                            odl = od[newstate]
                            if minpath > odl:
                                minpath = odl
                                wend = newstate
                                prev[wend] = u
                        else:
                            prev[newstate] = u
                            kolejka.append(newstate)
                            end = end+1
            else:  # white figures move
                tab = new_king_move(move, pos_king, pos_black_, pos_rook)
                for e in tab:
                    newstate = state(
                        [1, fromntochess(e), fromntochess(pos_rook), fromntochess(pos_black_)])
                    if od[newstate] == -1:
                        od[newstate] = od[u]+1
                        if mat(fromntochess(e), fromntochess(pos_rook), fromntochess(pos_black_)):
                            odl = od[newstate]
                            if minpath > odl:
                                minpath = odl
                                wend = newstate
                                prev[wend] = u
                        else:
                            prev[newstate] = u
                            kolejka.append(newstate)
                            end = end+1
                # rook move
                tab = newmovewiezy(pos_rook, pos_king, pos_black_)
                for e in tab:
                    newstate = state(
                        [1, fromntochess(pos_king), fromntochess(e), fromntochess(pos_black_)])
                    if od[newstate] == -1:
                        od[newstate] = od[u]+1
                        if mat(fromntochess(pos_king), fromntochess(e), fromntochess(pos_black_)):
                            odl = od[newstate]
                            if minpath > odl:
                                minpath = odl
                                wend = newstate
                                prev[wend] = u
                        else:
                            prev[newstate] = u
                            kolejka.append(newstate)
                            end = end+1
        if minpath == inf:
            for i in range(0, 524288):
                if od[i] != -1:
                    pos_black_ = i % 64
                    pos_rook = (i//64) % 64
                    pos_king = (i//4096) % 64
                    if pat(fromntochess(pos_king), fromntochess(pos_rook), fromntochess(pos_black_)): 
                        minpath = 'INF'
        else:
            mode = 0
            # mode = int(input("0 - saving to a file, 1 - mode 'debugger'\n"))
            if mode == 1:
                if minpath != 'INF':
                    i = minpath
                    end = wend
                    res = []
                    while i >= 0:
                        a = end % 64
                        b = end//64 % 64
                        c = end//4096 % 64
                        # d=end//(4096*64)%64
                        res.append([fromntochess(c), fromntochess(b), fromntochess(a)])  # [d,...]
                        end = prev[end]
                        i = i-1
                    res.reverse()
                    help = 0
                    help2 = 1
                    while help2 != minpath+1:
                        for h in range(0, 3):
                            if res[help][h] != res[help2][h]:
                                print(res[help][h]+res[help2][h] + ' ', end='')
                        help += 1
                        help2 += 1
                    # for i in res:
                    #   if i[0]==1:
                    #       print('black',i[1],i[2],i[3])
                    #   else:
                    #       print('white',i[1],i[2],i[3])
                else:
                    print('INF')
            else:
                file = open("zad1_output.txt", "w")
                file.write(str(minpath))
                file.close()
# print("--- %s seconds ---" % (time.time() - start_time))
