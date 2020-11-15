import random
import copy
import math

class sudoku():

    def __init__(self,arr):
        # 枠の大きさ.固定しているが2*2などサイズを変えたい時用
        self.n = 9
        self.arr = arr

    def solve(self,x,y): # x,yは0を入れる
        if y > self.n-1:
            return True
        elif x > self.n-1:
            if self.solve(0,y+1):
                return True
            else:
                return False
        elif self.arr[y][x] != 0:
            if self.solve(x+1,y): # x > 8は上で弾いているのでこの形でスキップ
                return True
            else:
                return False
        else:
            l = [i for  i in range(1,10)]
            random.shuffle(l) # こうすることで全ての組合せを作ることができる
            for i in l:
            #for i in range(1,self.n+1):
                if self.check_v(x,i) and self.check_h(y,i) and self.check_s(x,y,i):
                    self.arr[y][x] = i
                    if self.solve(x+1,y):
                        return True
        self.arr[y][x] = 0 # 上のfor文で誤ったものを訂正
        return False

    def check_v(self,x,n): # 縦に同じ数字がないか調べる
        for i in range(self.n):
            if self.arr[i][x] == n:
                return False
        return True
    
    def check_h(self,y,n): # 横に同じ数字がないか調べる
        for i in range(self.n):
            if self.arr[y][i] == n:
                return False
        return True

    def check_s(self,x,y,n): # 正方形に同じ数字がないか調べる
        ms = int(math.sqrt(self.n))
        for i in range(ms):
            for j in range(ms):
                if self.arr[(y//ms)*ms+i][(x//ms)*ms+j] == n:
                    return False
        return True

    def print_arr(self): # 数独を埋め表示する
        self.solve(0,0)
        for i in range(self.n):
            print(self.arr[i])

# こちらは計算時間を考慮して3×3マスしか対応していない
class genarate(sudoku):
    
    def __init__(self,diff):
        self.gearr = [[0 for i in range(9)] for j in range(9)]
        self.diff = diff # 60以上は重いので60以下推奨
    
    # 上三行を埋める安易な関数
    def per(self):
        a = [] # 1つめのブロック
        b = [] # 2つめのブロック
        c = [] # 3つめのブロック
        num = [i for i in range(1,10)]
        random.shuffle(num)
        for i in range(9):
            self.gearr[0][i] = num[i]
            if i < 3:
                a.append(num[i])
            elif i < 6:
                b.append(num[i])
            else:
                c.append(num[i])
        random.shuffle(num)
        for i in range(3):
            for j in range(3,9):
                if num[i] in a and not(num[j] in a):
                    num[i],num[j] = num[j],num[i]
        for i in range(3,6):
            for j in range(9):
                if j <= 5 and j >= 3:
                    continue
                if num[i] in b and not(num[j] in b):
                    num[i],num[j] = num[j],num[i]
        for i in range(6,9):
            for j in range(6):
                if num[i] in c and not(num[j] in c):
                    num[i],num[j] = num[j],num[i]
        for i in range(9):
            self.gearr[1][i] = num[i]
            if i < 3:
                a.append(num[i])
            elif i < 6:
                b.append(num[i])
            else:
                c.append(num[i])
        random.shuffle(num)
        for i in range(9):
            if not(num[i] in a) and len(a) < 9:
                a.append(num[i])
            elif not(num[i] in b) and len(b) < 9:
                b.append(num[i])
            else:
                c.append(num[i])
        for i in range(3):
            self.gearr[2][i] = a[6+i]
        for i in range(3):
            self.gearr[2][3+i] = b[6+i]
        for i in range(3):
            self.gearr[2][6+i] = c[6+i]

    # 数字を消す関数
    def del_num(self):
        list_num = [i for i in range(81)]
        random.shuffle(list_num)
        for i in range(55): # ここの数字で難易度を調整
            tmp = copy.deepcopy(self.gearr) # 多次元リストの場合deepcopyで値受け渡し
            flag = True
            for j in range(1,10):
                if j == tmp[list_num[i]//9][list_num[i]%9]:
                    continue
                self.gearr[list_num[i]//9][list_num[i]%9] = 0
                super().__init__(self.gearr)
                if super().check_h(list_num[i]//9,j) and super().check_v(list_num[i]%9,j) and super().check_s(list_num[i]%9,list_num[i]//9,j):
                    self.gearr[list_num[i]//9][list_num[i]%9] = j
                    if super().solve(0,0): # Trueなら下の数字以外を挿入しても大丈夫なので0にしてしまうと一意性を保証できない
                        flag = False
                self.gearr = copy.deepcopy(tmp)
            if flag:
                self.gearr[list_num[i]//9][list_num[i]%9] = 0

    def print_gearr(self):
        self.per()
        super().__init__(self.gearr)
        super().solve(0,0)
        self.del_num()
        for i in range(9):
            print(self.gearr[i])

"""
# フィンランド人の環境科学者Arto Inkala博士が作成した世界一難しい数独で試す
array = [[0,0,5,3,0,0,0,0,0],
         [8,0,0,0,0,0,0,2,0],
         [0,7,0,0,1,0,5,0,0],
         [4,0,0,0,0,5,3,0,0],
         [0,1,0,0,7,0,0,0,6],
         [0,0,3,2,0,0,0,8,0],
         [0,6,0,5,0,0,0,0,9],
         [0,0,4,0,0,0,0,3,0],
         [0,0,0,0,0,9,7,0,0]]
import time
start = time.time()
k = sudoku(array)
k.print_arr()
end = time.time()
print(end-start)

# ここからは生成プログラムのテスト

import time
count = 0
count2 = 1
ma = 0
mi = 100
for i in range(32):
    start = time.time()
    t = genarate(55)
    t.print_gearr()
    end = time.time()
    count+=end-start
    count2*=(end-start)
    ma = max(ma,end-start)
    mi = min(mi,end-start)
    print("生成時間:",end-start,"s")
print()
import math
print("最大生成時間:",ma,"s")
print("最小生成時間:",mi,"s")
print("(算術)平均生成時間:",count/32,"s")
print("(幾何)平均生成時間:",math.sqrt(math.sqrt(math.sqrt(math.sqrt(math.sqrt(count2))))),"s")
"""
