import sys
from random import randint
from time import monotonic
import matplotlib.pyplot as plt
import numpy as np
import gmpy2
from gmpy2 import mpz
import os
import math
import time

# Add the mmfv4 directory to Python path
mmfv4_path = r"C:\Users\darag\Documents\MMFV4"
sys.path.append(mmfv4_path)

import mmfv4

sys.set_int_max_str_digits(10000000)

def matrice(x,y,max):
    m=[]
    for i in range(x):
        l=[]
        for k in range(y):
            print("M",i+1,":",k+1,end="",sep="")
            l.append(int(input("=")))
        m.append(l)
    return m,x,y,max


def random_matrice(x,y,max):
    m=[]
    for i in range(x):
        l=[]
        for k in range(y):
            l.append(randint(0,max))
        m.append(l)
    print_matrice(m)
    return m

def read_matrice(string_matrice):
    #je sais pas trop comment faire mais y'a surement moyen
    return 0

#renommer en calcul de matrices avec moyenne max minimum et autres pas forcement necessaire pour l'instant
def max_matrice(m):
    max=0
    for i in range(len(m)):
        for k in range(len(m[i])):
            if m[i][k]>max:
                max=m[i][k]
    return max

def min_matrice(m,max):
    min=max
    for i in range(len(m)):
        for y in range(len(m[0])):
            if m[i][y]<min:
                min=m[i][y]
    return min

def print_matrice(m):
    max=max_matrice(m)
    for i in range(len(m)):
        print("[",end=" ")
        for k in range(len(m[i])):
            if m[i][k]<10**((len(str(max)))-1):
                nb_zero=(len(str(max)))-len(str(m[i][k]))
                for l in range(nb_zero):
                    print(" ",end="")
            print(m[i][k],end=" ")
        print("]")
    print("Max=",max,"(",len(str(max)),")","Min=",min_matrice(m,max),"Lignes=",len(m),"Colonnes=",len(m[0]))


#Addition fonctionne normalement
def addition_matrice(m1,m2):
    if len(m1)!=len(m2):
        print("-----Erreur de taille-----")
    elif len(m1[0])!=len(m2[0]):
        print("-----Erreur de taille-----")
    else:
        m3=[]
        for i in range(len(m1)):
            l=[]
            for k in range(len(m2[0])):
                l.append(m1[i][k]+m2[i][k])
            m3.append(l)
        #print("Resultat:")
        #print_matrice(m3)
        return m3


#fonctionne sur le plan du calcul ordre des tailles pas verifie mais surement correct
def multiplication_matrice(m1,m2):
    if len(m1[0])!=len(m2):
        print("-----Erreur de taille-----")
    else:
        m3=[]
        for i in range(len(m1)): #th le nombre de lignes qu'il y aura len(m1[0])
            l=[]                       #je vais tenter d'inverser...
            for k in range(len(m2[0])): #th le nombre de colonnes qu-il y aura   len(m2)
                j=0
                for p in range(len(m1[0])):
                    j+=(m1[i][p])*(m2[p][k])
                l.append(j)
            m3.append(l)
        #print("Resultat:")
        #print_matrice(m3)
        return m3

#multiplication_matrice(random_matrice(5,5,100),random_matrice(5,5,100))

def carre_matrice(m):
    if len(m)!=len(m[0]):
        print("-----Erreur de taille-----")
    else:
        m=multiplication_matrice(m,m)
        return m

#carre_matrice([[1,1],[1,0]])

def puissance_matrice(m,n):
    mf=m
    if len(m)!=len(m[0]):
        print("-----Erreur de taille-----")
    else:
        for i in range(n-1):
            mf=multiplication_matrice(mf,m)
        return mf

#puissance_matrice([[1,1],[1,0]],5)

def matrice_fibo():
    return [[mpz(1), mpz(1)], [mpz(1), mpz(0)]]


#problemes de dimension sur les boucles des matrices matric(lignes,colonnes)
#multiplication_matrice(random_matrice(2,2,10),random_matrice(5,3,100))

#puissance_matrice([[1,1],[1,0]],64)

def quick_fibo(n):
    n_2=puissance_deux(n)
    lm=[]
    a=0
    for i in range(len(n_2)):
        m=matrice_fibo()
        for k in range(n_2[i]):
            m=carre_matrice(m)
        lm.append(m)
    a=lm[0]
    for i in range(1,len(lm)):
        a=multiplication_matrice(a,lm[i])
    return a


def puissance_deux(n):
    l=[]
    power = 0
    while n > 0:
        if n % 2 == 1:
            l.append(power)
        n //= 2
        power += 1
    return list(reversed(l))
def quick(n):
    m=matrice_fibo()
    for i in range(n):
        m=carre_matrice(m)
    return m
def fib_retard(n):
    a=0
    b=1
    c=0
    for i in range(n):
        c=a+b
        a=b
        b=c
    return a

def ME(n):
    n_2=puissance_deux(n)
    lm=[]
    a=0
    lt=[]
    m=matrice_fibo()
    a=n_2[0]
    n_2.pop(0)
    for k in range(a):
        m=carre_matrice(m)
        if k+1 in n_2:
            if m not in lt:
                lt.append(m)
    if 0 in n_2:
        lt.append(matrice_fibo())
    for i in range(len(n_2)):
        m=multiplication_matrice(m,lt[i])
    return m

def factorielle(n):
    m=1
    for i in range(1,n+1):
        m*=i
    return m
def combinaison(n,k):
    k = min(k, n - k)
    return int(round(factorielle(n))/(factorielle(n-k)*factorielle(k)))
def combination(n, k):
    """Calculate binomial coefficient C(n,k) = n! / (k! * (n-k)!)"""
    if k > n or k < 0:
        return 0
    if k == 0 or k == n:
        return 1
    
    # Use the more efficient formula to avoid large factorials
    k = min(k, n - k)  # Take advantage of symmetry
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result
def methode_gaetan(n):
    u=0
    for i in range((n-1)//2+1):
        u+=combination(n-i-1,i)
    return u

def test(n):
    d=monotonic()
    fib_retard(n)
    a=monotonic()
    new_ME(n)
    b=monotonic()
    ME(n)
    print("NEw:",b-a,"s","Matrice:",monotonic()-b,"s","OG",a-d,"s")


def verif(n):
    s=True
    for i in range(2,n):
        if ME(n)[0][1]!=new_ME(n)[0][1]:
            print(ME(i)[0][1],MEV2(i)[0][1])
            s=False
    print(s)
        
def MMF(m,n):
    mf=[[1,1],[1,1]]
    mf[0][0]=m[0][0]*n[0][0]+m[0][1]*n[1][0]
    mf[0][1]=m[0][0]*n[0][1]+m[0][1]*n[1][1]
    mf[1][0]=mf[0][1]
    mf[1][1]=mf[0][0]-mf[0][1]
    return mf

def C(m):
    return MMF(m,m)

def new_ME(n):
    n_2=puissance_deux(n)
    lm=[]
    a=0
    lt=[]
    m=matrice_fibo()
    a=n_2[0]
    n_2.pop(0)
    for k in range(a):
        m=C(m)
        if k+1 in n_2:
            if m not in lt:
                lt.append(m)
    if 0 in n_2:
        lt.append(matrice_fibo())
    for i in range(len(n_2)):
        m=MMF(m,lt[i])
    return m

def main(n):
    p=10
    x=np.arange(1,n+1,p)
    b=[]
    c=[]
    l=[]
    for i in range(1,n+1,p):
        e=monotonic()
        MEV4(i)
        f=monotonic()
        MEV3(i)
        g=monotonic()
        #fib_retard(i)
        #h=monotonic()
        b.append(f-e)
        c.append(g-f)
        #l.append(h-g)
    plt.figure(figsize=(10, 6))
    plt.plot(x, b, label='MEV4', marker='s', markersize=2)
    plt.plot(x, c, label='MEV3', marker='^', markersize=2)
    #plt.plot(x, l, label='Linear', marker='o', markersize=2)
    plt.xlabel('Input Size (n)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Performance Comparison of Three Functions')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def t(n):
    a=time.monotonic_ns()
    MEV3(n)
    b=time.monotonic_ns()
    MEV4(n)
    c=time.monotonic_ns()
    print("Runtime  MEV4 =",(c-b)/10**6,"ms, MEV3:",(b-a)/10**6,"ms")
    d=MEV2(n)
    with open("Fibo.txt", "w") as file:
        file.write(str(d))

def MMFV2(m,n):
    mf=[[1,1],[1,1]]
    mf[1][1]=m[1][0]*n[0][1]+m[1][1]*n[1][1]
    mf[0][1]=m[0][0]*n[0][1]+m[0][1]*n[1][1]
    mf[1][0]=mf[0][1]
    mf[0][0]=mf[0][1]+mf[1][1]
    return mf

def MMFV3(m,n):
    a=m[1][0]*n[0][1]+m[1][1]*n[1][1]
    b=m[0][0]*n[0][1]+m[0][1]*n[1][1]
    return [[a+b,b],[b,a]]

def CMFV2(m):
    return MMFV2(m,m)

def MEV2(n):
    n_2=puissance_deux(n)
    lm=[]
    a=0
    lt=[]
    m=matrice_fibo()
    a=n_2[0]
    n_2.pop(0)
    for k in range(a):
        m=MMFV3(m,m)
        if k+1 in n_2:
            if m not in lt:
                lt.append(m)
    if 0 in n_2:
        lt.append(matrice_fibo())
    for i in range(len(n_2)):
        m=MMFV2(m,lt[i])
    return m[0][1]

def methode_binet(n):
    # vrai pour tout n<=70 (on utilisera surement 64)
    #plus utile
    return round(((1+math.sqrt(5))**n-(1-math.sqrt(5))**n)/(2**n*math.sqrt(5)))
def new_binet(n):
    sqrt5 = 2.23606797749979 
    phi = 1.618033988749895  
    psi = -0.618033988749895
    return int((phi**n - psi**n) / sqrt5 + 0.5)

def verif(n):
    for i in range(n):
        if fib_retard(i)!=MEV4(i):
            print("Erreur",i,fib_retard(i),MEV4(i))

def test(n):
    for i in range(1,n+1):
        a=monotonic()
        methode_binet(i)
        b=monotonic()
        new_binet(i)
        c=monotonic()
        MEV2(i)
        d=monotonic()
        print(b-a,c-b,d-c)

def dec_power(n):
    if n <= 0:
        return []
    
    coefficients = []
    while n:
        power = n & -n 
        coeff = (power - 1).bit_length()  
        coefficients.append(coeff)
        n ^= power      

    return sorted(coefficients, reverse=True)

def fibo_64():
    #TESTER SI PAS INTERESSANT DE COPY LES VALEURS (SUREMENT 1000ns de gains) update: pas interessant
    return [[mpz(new_binet(65)),mpz(new_binet(64))],[mpz(new_binet(64)),mpz(new_binet(63))]]

def MEV3(n=1048576):
    t=[]
    #aa=time.monotonic_ns()
    if n<=70:
        return new_binet(n)
    else:
        #bb=time.monotonic_ns()
        n_2=dec_power(n)
        #gg=time.monotonic_ns()
        lt=[]
        a=n_2[0]
        n_2.pop(0)
        #jj=time.monotonic_ns()
        m=fibo_64()
        #ll=time.monotonic_ns()
        b=0
        #cc=time.monotonic_ns()
        for k in range(6,a):
            m=MMFV3(m,m)
            t.append(time.monotonic_ns())
            if k+1 in n_2:
                lt.append(m)
                n_2.remove(k+1)
                b+=1
        #dd=time.monotonic_ns()
        for i in n_2:
            if i<=6:
                #peut etre plus long, a verifier
                c=mpz(new_binet(2**i+1))
                d=mpz(new_binet(2**i))
                m=MMFV3(m,([[c,d],[d,c-d]]))
        #ee=time.monotonic_ns()
        for i in range(b):
            m=MMFV3(m,lt[i])
        #ff=time.monotonic_ns()
        #print("if:",bb-aa,"init:",cc-bb,"(dont conversion en 2^:",gg-bb,"et matrice fibo:",ll-jj,")","carre:",dd-cc,"petits:",ee-dd,"memoire:",ff-ee)
        return m[0][1]

def find_lowest_MEV4(n):
    low_time=10000000
    for i in range(n):
        a=time.monotonic_ns()
        MEV4(2**20)
        b=time.monotonic_ns()
        if b-a<low_time:
            low_time=b-a
    print(low_time/10**6,"ms")
    return low_time

def find_lowest_MEV3(n):
    low_time=10000000
    for i in range(n):
        a=time.monotonic_ns()
        MEV3(2**20)
        b=time.monotonic_ns()
        if b-a<low_time:
            low_time=b-a
    print(low_time/10**6,"ms")
    return low_time

def fast_doubling_fib(n):
    """Ultra-optimized fast doubling Fibonacci"""
    if n <= 1:
        return n
    
    # Pre-compute bit positions to avoid repeated bit_length() calls
    bit_length = n.bit_length() - 2
    a, b = 1, 1  # F(k), F(k+1)
    
    # Manual loop unrolling approach
    while bit_length >= 0:
        # Cache multiplications
        a_sq = a * a
        b_sq = b * b
        ab = a * b
        
        # F(2k) = a * (2b - a), F(2k+1) = a² + b²
        c = a * (b + b) - a_sq  # Rearranged to reuse a_sq
        d = a_sq + b_sq
        
        # Bit test with manual shift
        if n & (1 << bit_length):
            a, b = d, c + d
        else:
            a, b = c, d
            
        bit_length -= 1
    
    return a

def CMFV3(m):
    a=m[1][0]*m[1][0]+m[1][1]*m[1][1]
    b=(m[0][0]+m[1][1])*m[0][1]
    return [[a+b,b],[b,a]]

def MEV4(n=1048576):
    #aa=time.monotonic_ns()
    if n<=70:
        return new_binet(n)
    else:
        #bb=time.monotonic_ns()
        n_2=dec_power(n)
        #gg=time.monotonic_ns()
        lt=[]
        a=n_2[0]
        n_2.pop(0)
        #jj=time.monotonic_ns()
        m=fibo_64()
        #ll=time.monotonic_ns()
        b=0
        #cc=time.monotonic_ns()
        for k in range(6,a):
            m=CMFV3(m)
            if k+1 in n_2:
                lt.append(m)
                n_2.remove(k+1)
                b+=1
        #dd=time.monotonic_ns()
        for i in n_2:
            if i<=6:
                #peut etre plus long, a verifier
                c=mpz(new_binet(2**i+1))
                d=mpz(new_binet(2**i))
                m=mmfv4.mmfv4_bigint(m,([[c,d],[d,c-d]]))
        #ee=time.monotonic_ns()
        for i in range(b):
            m=mmfv4.mmfv4_bigint(m,lt[i])
        #ff=time.monotonic_ns()
        #print("if:",bb-aa,"init:",cc-bb,"(dont conversion en 2^:",gg-bb,"et matrice fibo:",ll-jj,")","carre:",dd-cc,"petits:",ee-dd,"memoire:",ff-ee)
        return m[0][1]


verif(140)