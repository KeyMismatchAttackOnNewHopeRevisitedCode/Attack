import math
from random import randrange
from NodeTree import *

# used to check if Hypothesis 1 holds when we
# are in the leftmost leaf of the tree T2
extra = [0,0,0,-1,768]

# secret key represented as a vector
S = [0] * 1024

# total number of queries in the experiments used to compute the average number
queries = 0

# indication if we encountered issue with Hypothesis 1 during the attack
Hypo = True

# Key mismatch oracle
# Oracle implemented already for our choice of ciphertext m_E = (C,u) and message u_E
# Input uniquely defined by j_0, j_1, j_2, j_3, a, k
# j_0, j_1, j_2, j_3 determine the polynomial c
# a, k determine the polynomial U
# k is moreover the index of the targeted quadruplet
# u_E = (1,0,...,0) fixed for all queries
def Oracle(j0,j1,j2,j3,a,k):
    global S
    shifted_S = [0] * 1024  # shifted_S corresponds to the product x^(-k) * S
    for ii in range(1024-k):
        shifted_S[ii] = S[ii+k]
    for ii in range(k):
        shifted_S[1024-k+ii] = -S[ii]
    # decapsulation of the first bit:
    temp = 0
    temp += abs((a * shifted_S[0] - Decompress(j0 + 4)) % 12289 - 6144)
    temp += abs((a * shifted_S[256] - Decompress(j1 + 4)) % 12289 - 6144)
    temp += abs((a * shifted_S[512] - Decompress(j2 + 4)) % 12289 - 6144)
    temp += abs((a * shifted_S[768] - Decompress(j3 + 4)) % 12289 - 6144)
    if temp >= 12289:
        output = '+'
    else:
        output = '-'
    # decapsulation of the remaining bits:
    for index in range(1, 256):
        temp = 0
        temp += abs((a * shifted_S[0+index]) % 12289 - 6144)
        temp += abs((a * shifted_S[256+index]) % 12289 - 6144)
        temp += abs((a * shifted_S[512+index]) % 12289 - 6144)
        temp += abs((a * shifted_S[768+index]) % 12289 - 6144)
        if temp < 12289:
            return '+'
    return output

# generation of the secret key according to the centered binomial distribution
# secret key represented by a vector stored in a global variable
def KeyGeneration():
    global S
    for ii in range(1024):
        coeff = 0
        for jj in range(8):
            b_0 = randrange(2)
            b_1 = randrange(2)
            coeff += (b_0 - b_1)
        S[ii] = coeff

# the whole framework
def Attack(numberOfAttacks):
    global S
    global queries
    global Hypo
    success = 0
    T2=reconstruct(readjson("T2.txt"))
    T1=reconstruct(readjson("T1.txt"))
    for ii in range(numberOfAttacks):
        KeyGeneration()
        secret = RecoverSecretKey(T1, T2)
        if S == secret:
            success += 1

    averageQ = queries / numberOfAttacks
    averageSuccess = 100 * (success / numberOfAttacks)
    print("Number of experiments: " + str(numberOfAttacks))
    print("Average number of queries: " + str(averageQ))
    print("Average success probability: " + str(averageSuccess))

# recovers the secret key
# input are the roots of tress T1 and T2
def RecoverSecretKey(T1, T2):
    global Hypo
    Hypo = True
    secret = [0] * 1024
    for k in range(256):
        if Hypo == True:
            s0, s1, s2, s3 = T2_RecoverQuadruplet(k, T2)
            if Hypo == True:
                secret[k] = s0
                secret[k + 256] = s1
                secret[k + 512] = s2
                secret[k + 768] = s3
            else:
                s0, s1, s2, s3 = T1_RecoverQuadruplet(k, T1)
                secret[k] = s0
                secret[k + 256] = s1
                secret[k + 512] = s2
                secret[k + 768] = s3
        else:
            s0, s1, s2, s3 = T1_RecoverQuadruplet(k, T1)
            secret[k] = s0
            secret[k + 256] = s1
            secret[k + 512] = s2
            secret[k + 768] = s3
    return secret

# recovering one quadruplet of secret coefficients according to the tree T1
# Hypothesis 1 always holds for this tree
# input is the index k of the targeted quadruplet and the root of tree T1
# returns the recovered quadruplet of secret coefficients which is always correct
def T1_RecoverQuadruplet(k, root):
    global queries
    while root.left != None:
        t = Oracle(root.j0, root.j1, root.j2, root.j3, root.coeff, k)
        queries += 1
        if t == '+':
            root = root.left
        else:
            root = root.right
    return root.j0, root.j1, root.j2, root.j3

# recovering one quadruplet of secret coefficients according to the tree T2
# Hypothesis 1 holds only with 95% for this tree
# input is the index k of the targeted quadruplet and the root of tree T1
# output is quadruplet of secret coefficients and indication if there was a problem with Hypothesis 1
# if there was no problem with Hypo 1, then the returned quadruplet is correct
# if there is a problem with Hypo 1, then the returned quadruplet is not correct
def T2_RecoverQuadruplet(k, root):
    global queries
    global extra
    global Hypo
    leftmost = True
    while root.left != None:
        t = Oracle(root.j0, root.j1, root.j2, root.j3, root.coeff, k)
        queries += 1
        if t == '+':
            root = root.left
        else:
            leftmost = False
            root = root.right
    if leftmost == True:
        t = Oracle(extra[0], extra[1], extra[2], extra[3], extra[4], k)
        if t == '+':
            Hypo = False
    return root.j0, root.j1, root.j2, root.j3

# Decompress function which is used within the key mismatch oracle
# it maps an element from Z_8 to Z_12289
def Decompress(v):
    return math.floor(((12289 * v) / 8) + 0.5)




##################################################################################################################################


Attack(5)
