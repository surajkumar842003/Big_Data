import random
import hashlib
import time

random.seed(42)

m = 20000   

def read_file(filename):

    with open(filename,'r',encoding='utf-8') as f:

        text = f.read().lower()
        text = text.replace("\n"," ")
        text = text.replace("\t"," ")

    return text


D1 = read_file("minhash/D1.txt")
D2 = read_file("minhash/D2.txt")



def char_kgrams(text,k):

    grams = set()

    for i in range(len(text)-k+1):

        grams.add(text[i:i+k])

    return grams


g1 = char_kgrams(D1,3)
g2 = char_kgrams(D2,3)



def jaccard(A,B):

    return len(A & B) / len(A | B)


true_j = jaccard(g1,g2)

print("True Jaccard similarity:",true_j)
print()


def stable_hash(x):

    return int(hashlib.md5(x.encode()).hexdigest(),16)


def generate_hash_functions(t):

    hash_funcs = []

    for _ in range(t):

        a = random.randint(1,m-1)
        b = random.randint(0,m-1)

        hash_funcs.append((a,b))

    return hash_funcs


def minhash_signature(shingles,hash_funcs):

    shingles = list(shingles)

    signature = []

    for a,b in hash_funcs:

        min_val = float("inf")

        for s in shingles:

            h = (a * stable_hash(s) + b) % m

            if h < min_val:
                min_val = h

        signature.append(min_val)

    return signature

def estimate(sig1,sig2):

    match = 0

    for i in range(len(sig1)):

        if sig1[i] == sig2[i]:

            match += 1

    return match / len(sig1)


t_values = [20,60,150,300,600]

print("MinHash Approximation Results\n")

for t in t_values:

    start = time.time()

    hash_funcs = generate_hash_functions(t)

    sig1 = minhash_signature(g1,hash_funcs)
    sig2 = minhash_signature(g2,hash_funcs)

    approx = estimate(sig1,sig2)

    end = time.time()

    print("t =",t)
    print("Approx Jaccard =",approx)
    print("Error =",abs(approx-true_j))
    print("Time =",end-start)
    print()