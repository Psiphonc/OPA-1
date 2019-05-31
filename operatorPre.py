L = []
R = []
# warning : VN and VT can only be one char
for l in open('ProductionRule'):
    p = l.strip('\n').split('->')
    L.append(p[0])
    R.append(p[1])

VN = []
VT = []

for i in range(len(L)):
    if L[i] not in VN:
        VN.append(L[i])

print('VN set:', VN)

for r in R:
    for p in range(len(r)):
        if (r[p] not in VN) and (r[p] not in VT):
            VT.append(r[p])

print('VT set:', VT)

# ----calculate lastVT
firstVT = {}

for i in range(len(L)):
    if R[i][0] in VT:
        # print L[i],R[i]
        if L[i] not in firstVT:
            firstVT[L[i]] = [R[i][0]]
        else:
            firstVT[L[i]].append(R[i][0])
    elif R[i][0] in VN:
        if len(R[i]) > 1 and (R[i][1] in VT):
            # print L[i],R[i]
            if L[i] not in firstVT:
                firstVT[L[i]] = [R[i][1]]
            else:
                firstVT[L[i]].append(R[i][1])

# print firstVT

stack = []

for _k in firstVT:
    for _v in firstVT.get(_k):
        stack.append([_k, _v])

# print stack

while len(stack) > 0:
    tmp = stack.pop()
    K = tmp[0]
    v = tmp[1]
    for i in range(len(R)):
        l, r = L[i], R[i]
        if (r[0] == K and K != l) and (v not in firstVT.get(l)):
            firstVT[l].append(v)
            stack.append([l, v])

print('firstVT set:', firstVT)

# ----calculate lastVT
lastVT = {}

for i in range(len(L)):
    if R[i][-1] in VT:
        # print L[i],R[i]
        if L[i] not in lastVT:
            lastVT[L[i]] = [R[i][-1]]
        else:
            lastVT[L[i]].append(R[i][-1])
    elif R[i][-1] in VN:
        if len(R[i]) > 1 and (R[i][-2] in VT):
            # print L[i],R[i]
            if L[i] not in lastVT:
                lastVT[L[i]] = [R[i][-2]]
            else:
                lastVT[L[i]].append(R[i][-2])

# print lastVT

stack = []

for _k in lastVT:
    for _v in lastVT.get(_k):
        stack.append([_k, _v])

# print stack

while len(stack) > 0:
    tmp = stack.pop()
    K = tmp[0]
    v = tmp[1]
    for i in range(len(L)):
        l, r = L[i], R[i]
        if (r[0] == K and K != l) and (v not in lastVT.get(l)):
            lastVT[l].append(v)
            stack.append([l, v])

print('lastVT set:', lastVT)

# --- construct precedence relation table
PRtable = [([None] * (len(VT) + 1)) for i in range(len(VT) + 1)]

for i in range(len(L)):
    l, r = L[i], R[i]
    for _i in range(len(r) - 1):
        if (r[_i] in VT) and (r[_i + 1] in VT):
            PRtable[VT.index(r[_i])][VT.index(r[_i + 1])] = '='
        if (_i < len(r) - 2) and (r[_i] in VT) and (r[_i + 2] in VT) and (r[_i + 1] in VN):
            PRtable[VT.index(r[_i])][VT.index(r[_i + 2])] = '='
        if (r[_i] in VT) and (r[_i + 1] in VN):
            for b in firstVT[r[_i + 1]]:
                # print VT.index(r[_i]),r[_i],r[_i+1],b,VT.index(b)
                PRtable[VT.index(r[_i])][VT.index(b)] = '<'
        # print PRtable
        if (r[_i] in VN) and (r[_i + 1] in VT):
            for b in lastVT[r[_i]]:
                PRtable[VT.index(b)][VT.index(r[_i + 1])] = '>'

# first VN is source S
S = VN[0]
for b in firstVT[S]:
    PRtable[-1][VT.index(b)] = '<'
for a in lastVT[S]:
    PRtable[VT.index(a)][-1] = '>'
PRtable[-1][-1] = '='

print('\nThe precedence relation table is :')
for i in range(len(PRtable)):
    print(PRtable[i])

# -----control program
s_in = '(i+i)*i#'

stack = []
k = 0
stack.append('#')

VT.append('#')
for a in s_in:
    print('stack state:', stack)

    j = None
    # stack.append(a)
    if stack[k] in VT:
        j = k
    else:
        j = k - 1

    while PRtable[VT.index(stack[j])][VT.index(a)] == '>':
        while True:
            Q = stack[j]
            if stack[j - 1] in VT:
                j = j - 1
            else:
                j = j - 2
            if PRtable[VT.index(stack[j])][VT.index(Q)] == '<':
                break
        # N = 'a'

        stack = stack[0:j + 1]

        k = j + 1
        stack.append('N')

    if PRtable[VT.index(stack[j])][VT.index(a)] == '<' or PRtable[VT.index(stack[j])][VT.index(a)] == '=':
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
