# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:45:55 2023

@author: t-jan
"""
import random
import matplotlib.pyplot as plt
#import math

def Harmonic_Number(n):
   # return 0.5772156649 + math.log(n) + 1/(2*n)
    Hn=0
    for i in range(1,n+1):
        Hn+=1/i
    return Hn

def Harmonic_Number_2(n):
    Hn2=0
    for i in range(1,n+1):
        Hn2+=1/i**2
    return Hn2

def random_number(rozklad,n): # <1,n>
    prawdopodobienstwa=[]
    przedzialy=[]
    if rozklad=='jednostajny' or rozklad=='j':
        for i in range(0,n):
            prawdopodobienstwa.append(1/n)
    elif rozklad=='harmoniczny' or rozklad=='h':
        Hn=Harmonic_Number(n)
        for i in range(1,n+1):
            prawdopodobienstwa.append(1/(i*Hn))
    elif rozklad=='dwuharmoniczny' or rozklad=='d' or rozklad=='dh':
        Hn2=Harmonic_Number_2(n)
        for i in range(1,n+1):
            prawdopodobienstwa.append(1/(i**Hn2))
    elif rozklad=='geometryczny' or rozklad=='g':
        for i in range(1,n):
            prawdopodobienstwa.append(1/2**i)
        prawdopodobienstwa.append(1/2**(n-1))
    else: return 'nieznany rozklad'
    przedzialy.append(0)
    przedzialy.append(prawdopodobienstwa[0])
    for i in range(2,len(prawdopodobienstwa)+1):
        przedzialy.append(przedzialy[i-1]+prawdopodobienstwa[i-1])
    przedzialy.append(1)
    X=random.random()
    for i in range(0,len(przedzialy)):
        if X>=przedzialy[i] and X<przedzialy[i+1]:
            return i+1

def zadanie(x,cache,rez,obsluga,mark,flags_use_cach,flags_use_res):
    if obsluga=='fifo':
        if x in cache:
            return 0
        else:
            cache.pop(0)
            cache.append(x)
            return 1
        
    elif obsluga=='fwf':
        if x in cache:
            return 0
        else:
            if 0 in cache:
                cache[cache.index(0)]=x
                return 1
            cache=[]
            for cache_poj in range(0,k):
                cache.append(0)
            return 1
                
    elif obsluga=='lru':
        if x not in cache: # usuwamy 1. element  i wstawiamy x na koncu
            cache.pop(0)
            cache.append(x)
            return 1
        else: # przesuwamy x na koniec
            cache.pop(cache.index(x))
            cache.append(x)
            return 0
        
    elif obsluga=='lfu':
        if x in cache:
            flags_use_cach[cache.index(x)]+=1
            return 0
        else:
            if 0 in cache: # unika zer w rez
                flags_use_cach[cache.index(0)]=1
                cache[cache.index(0)]=x
                return 1
            if x in rez:
                cache.append(x)
                flags_use_cach.append(flags_use_res[rez.index(x)]+1) # to opt rez.idx
                flags_use_res.pop(rez.index(x))
                rez.pop(rez.index(x))
                cachmintmpidx=flags_use_cach.index(min(flags_use_cach))
                rez.append(cache[cachmintmpidx])
                flags_use_res.append(flags_use_cach[cachmintmpidx])
                cache.pop(cachmintmpidx)
                flags_use_cach.pop(cachmintmpidx)
                return 1
            elif x not in rez:
                cache.append(x)
                flags_use_cach.append(1)
                cachmintmpidx=flags_use_cach.index(min(flags_use_cach))
                rez.append(cache[cachmintmpidx])
                flags_use_res.append(flags_use_cach[cachmintmpidx])
                cache.pop(cachmintmpidx)
                flags_use_cach.pop(cachmintmpidx)
                return 1
                
    elif obsluga=='rand':
        if x in cache:
            return 0
        else:
            if 0 in cache:
                cache[cache.index(0)]=x
                return 1
            else:
                cache.pop(random.randint(0,len(cache)-1))
                cache.append(x)
                return 1
        
    elif obsluga=='rma':
        if x in cache:
            mark[cache.index(x)]='o'
            return 0
        else:
            if 'n' not in mark: # if all marked then all dismark
                for i in range(0,len(mark)):
                    mark[i]='n'
            dismark_indices=[]
            for i in range(0,len(mark)):
                if mark[i]=='n':
                    dismark_indices.append(i)
            ind=random.randint(0,len(dismark_indices)-1)
            mark.pop(ind)
            cache.pop(ind)
            cache.append(x)
            mark.append('o')
            return 1
        
    else: return 'nieznana metoda obslugi cache\'a'

# inicjalizacja n i k
n = [20, 30, 40, 50, 60, 70, 80, 90, 100]


n=70
rozklad='g'
rep=700

kk=[]
k_new=int(n/10)
while k_new <= n/5:
    kk.append(k_new)
    k_new+=1
obslugi=['fifo','fwf','lru','lfu','rand','rma']
colors=['limegreen','crimson','yellow','hotpink','b','orangered']

for k in kk:
    for ob in obslugi:
        koszt=0
        for rr in range(0,rep):
            cache = []
            rez=[]
            mark=[]
            flags_use_cach=[]
            flags_use_res=[]
            for cache_poj in range(0,k):
                cache.append(0)
                flags_use_cach.append(0)
                mark.append(0)
            for xx in range(0,n):
                x=random_number(rozklad, n)
                koszt+=zadanie(x,cache,rez,ob,mark,flags_use_cach,flags_use_res)
        if k==kk[0]:
            plt.scatter(k,koszt/rep,color=colors[obslugi.index(ob)],label=ob)
        else:
            plt.scatter(k,koszt/rep,color=colors[obslugi.index(ob)])
            
plt.xlabel('k - pojemność cache\'a')
plt.ylabel('koszt n operacji')
plt.legend()
if rozklad=='j':
    plt.title('Rozkład jednostajny\n n='+str(n))
elif rozklad=='h':
    plt.title('Rozkład harmoniczny\n n='+str(n))
elif rozklad=='d':
    plt.title('Rozkład dwuharmoniczny\n n='+str(n))
elif rozklad=='g':
    plt.title('Rozkład geometryczny\n n='+str(n))
plt.show()

