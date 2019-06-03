class op:
    L = []
    R = []
    VN = []
    VT = []
    firstVT = {}
    lastVT = {}
    PRtable = []

    def __init__(self, production_rule):

        for l in open(production_rule):
            p = l.strip('\n').split('->')
            self.L.append(p[0])
            self.R.append(p[1])

        for i in range(len(self.L)):
            if self.L[i] not in self.VN:
                self.VN.append(self.L[i])

        print('VN set:', self.VN)

        for r in self.R:
            for p in range(len(r)):
                if (r[p] not in self.VN) and (r[p] not in self.VT):
                    self.VT.append(r[p])

        print('VT set:', self.VT)

        self.firstVT = self.calc_firstvt()
        self.lastVT = self.calc_lastvt()
        self.PRtable = self.generate_table()

    def calc_firstvt(self):
        # 对每个产生式的左边
        firstVT = {}
        for i in range(len(self.L)):
            # 若产生式右边的首字符为终结符(P->a...)
            if self.R[i][0] in self.VT:
                # 将该终结符加入L[i]的firstVT集
                if self.L[i] not in firstVT:
                    firstVT[self.L[i]] = [self.R[i][0]]
                else:
                    firstVT[self.L[i]].append(self.R[i][0])
            # 若产生式右边的首字符为非终结符(P->Qa...)
            elif self.R[i][0] in self.VN:
                # 若产生式右边第二个符号为终结符
                if len(self.R[i]) > 1 and (self.R[i][1] in self.VT):
                    # 将该终结符加入L[i]的firstVT集
                    if self.L[i] not in firstVT:
                        firstVT[self.L[i]] = [self.R[i][1]]
                    else:
                        firstVT[self.L[i]].append(self.R[i][1])
        # P->Q..
        stack = []
        # 对于每个非终结符_k的FirstVT
        for _k in firstVT:
            # 取出FirstVT(_k)中的终结符入栈
            for _v in firstVT.get(_k):
                stack.append([_k, _v])

        while len(stack) > 0:
            tmp = stack.pop()
            K = tmp[0]
            v = tmp[1]
            # 逐条扫描产生式
            for i in range(len(self.R)):
                l, r = self.L[i], self.R[i]
                # 若产生式右部第一个符号是非终结符K
                if (r[0] == K and K != l) and (v not in firstVT.get(l)):
                    firstVT[l].append(v)  # 把FirstVT(K)中的元素加入FirstVT(L)
                    stack.append([l, v])  # 发生变化，需要重新对FirstVT(L)扫描

        print('firstVT set:', firstVT)
        return firstVT

    def calc_lastvt(self):
        lastVT = {}

        for i in range(len(self.L)):
            # (P->...a)
            if self.R[i][-1] in self.VT:
                if self.L[i] not in lastVT:
                    lastVT[self.L[i]] = [self.R[i][-1]]
                else:
                    lastVT[self.L[i]].append(self.R[i][-1])
            # (P->...aQ)
            elif self.R[i][-1] in self.VN:
                if len(self.R[i]) > 1 and (self.R[i][-2] in self.VT):
                    if self.L[i] not in lastVT:
                        lastVT[self.L[i]] = [self.R[i][-2]]
                    else:
                        lastVT[self.L[i]].append(self.R[i][-2])

        # ...Q
        stack = []

        for _k in lastVT:
            for _v in lastVT.get(_k):
                stack.append([_k, _v])

        while len(stack) > 0:
            tmp = stack.pop()
            K = tmp[0]
            v = tmp[1]
            for i in range(len(self.L)):
                l, r = self.L[i], self.R[i]
                if (r[0] == K and K != l) and (v not in lastVT.get(l)):
                    lastVT[l].append(v)
                    stack.append([l, v])

        print('lastVT set:', lastVT)

        return lastVT

    def generate_table(self):
        PRtable = [([None] * (len(self.VT) + 1)) for i in range(len(self.VT) + 1)]

        # 扫描产生式
        for i in range(len(self.L)):
            l, r = self.L[i], self.R[i]
            for _i in range(len(r) - 1):
                # ...ab...
                if (r[_i] in self.VT) and (r[_i + 1] in self.VT):
                    PRtable[self.VT.index(r[_i])][self.VT.index(r[_i + 1])] = '='
                # ...aQb...
                if (_i < len(r) - 2) and (r[_i] in self.VT) and (r[_i + 2] in self.VT) and (r[_i + 1] in self.VN):
                    PRtable[self.VT.index(r[_i])][self.VT.index(r[_i + 2])] = '='
                # ...aP...
                if (r[_i] in self.VT) and (r[_i + 1] in self.VN):
                    for b in self.firstVT[r[_i + 1]]:
                        PRtable[self.VT.index(r[_i])][self.VT.index(b)] = '<'
                # ...Pb...
                if (r[_i] in self.VN) and (r[_i + 1] in self.VT):
                    for b in self.lastVT[r[_i]]:
                        PRtable[self.VT.index(b)][self.VT.index(r[_i + 1])] = '>'

        S = self.VN[0]
        for b in self.firstVT[S]:
            PRtable[-1][self.VT.index(b)] = '<'
        for a in self.lastVT[S]:
            PRtable[self.VT.index(a)][-1] = '>'
        PRtable[-1][-1] = '='
        print(self.VT)
        print('\nThe precedence relation table is :')
        for i in range(len(PRtable)):
            print(PRtable[i])

        return PRtable

    def analyze(self, s_in):
        stack = []
        k = 0
        stack.append('#')

        self.VT.append('#')
        for a in s_in:
            print('stack state:', stack)
            j = None
            if stack[k] in self.VT:
                j = k
            else:
                j = k - 1

            while self.PRtable[self.VT.index(stack[j])][self.VT.index(a)] == '>':
                while True:
                    Q = stack[j]
                    if stack[j - 1] in self.VT:
                        j = j - 1
                    else:
                        j = j - 2
                    if self.PRtable[self.VT.index(stack[j])][self.VT.index(Q)] == '<':
                        break
                # N = 'a'

                stack = stack[0:j + 1]

                k = j + 1
                stack.append('N')

            if self.PRtable[self.VT.index(stack[j])][self.VT.index(a)] == '<' or self.PRtable[self.VT.index(stack[j])][
                self.VT.index(a)] == '=':
                k = k + 1
                # stack[k] = a
                stack.append(a)
            else:
                print('error')
                break

            if a == '#':
                break

        print('stack state:', stack)
        if stack == ['#', 'N', '#']:
            print('receive!')
        else:
            print('cannot receive!')


if __name__ == '__main__':
    opter = op('ProductionRule')
    opter.analyze('(i+i)*i#')
