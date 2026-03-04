import random
import hashlib
import itertools
from collections import defaultdict

threshold = 0.6
runs = 5

configs = [
    (50,5,10),
    (100,5,20),
    (200,5,40),
    (200,10,20)
]

def load_data(filename):

    user_movies = defaultdict(set)

    with open(filename) as f:

        for line in f:

            u,m,r,t = line.split()

            user_movies[int(u)].add(int(m))

    return user_movies


user_movies = load_data("C:/Users/heysu/OneDrive/Documents/2nd-Semester/ML Big Data/dist_search/ml-100k/u.data")
users = list(user_movies.keys())

def jaccard(A,B):

    return len(A & B) / len(A | B)


true_pairs = set()
true_sim = {}

for u,v in itertools.combinations(users,2):

    s = jaccard(user_movies[u],user_movies[v])

    true_sim[(u,v)] = s

    if s >= threshold:
        true_pairs.add((u,v))



def stable_hash(x):

    return int(hashlib.md5(str(x).encode()).hexdigest(),16)


max_hash = 2**32-1


def generate_hash_funcs(t):

    funcs=[]

    for _ in range(t):

        a=random.randint(1,max_hash)
        b=random.randint(0,max_hash)

        funcs.append((a,b))

    return funcs


def minhash_signature(movie_set,hash_funcs):

    sig=[]

    for a,b in hash_funcs:

        min_val=float("inf")

        for m in movie_set:

            h=(a*stable_hash(m)+b)%max_hash

            if h<min_val:
                min_val=h

        sig.append(min_val)

    return sig


def lsh_candidates(signatures,r,b):

    buckets=defaultdict(list)

    for user,sig in signatures.items():

        for band in range(b):

            start=band*r
            end=start+r

            band_tuple=tuple(sig[start:end])

            buckets[(band,band_tuple)].append(user)

    candidates=set()

    for bucket in buckets.values():

        if len(bucket)>1:

            for u,v in itertools.combinations(bucket,2):

                candidates.add(tuple(sorted((u,v))))

    return candidates

for t,r,b in configs:

    print("\nConfig: t =",t," r =",r," b =",b)

    fp_total=0
    fn_total=0

    for run in range(runs):

        hash_funcs=generate_hash_funcs(t)

        signatures={}

        for u in users:

            signatures[u]=minhash_signature(user_movies[u],hash_funcs)

        candidates=lsh_candidates(signatures,r,b)

        fp=len([p for p in candidates if true_sim.get(p,0)<threshold])

        fn=len([p for p in true_pairs if p not in candidates])

        fp_total+=fp
        fn_total+=fn


    print("Average False Positives:",fp_total/runs)
    print("Average False Negatives:",fn_total/runs)