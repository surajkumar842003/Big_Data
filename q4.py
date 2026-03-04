import random
import hashlib
import itertools
from collections import defaultdict

random.seed()

threshold = 0.5
runs = 5
t_values = [50,100,200]


def load_data(filename):

    user_movies = defaultdict(set)

    with open(filename,'r') as f:

        for line in f:

            user,movie,rating,time = line.strip().split()

            user = int(user)
            movie = int(movie)

            user_movies[user].add(movie)

    return user_movies


user_movies = load_data("C:/Users/heysu/OneDrive/Documents/2nd-Semester/ML Big Data/dist_search/ml-100k/u.data")

users = list(user_movies.keys())


def jaccard(A,B):

    return len(A & B) / len(A | B)

true_pairs = set()
true_sim = {}

for u,v in itertools.combinations(users,2):

    s = jaccard(user_movies[u], user_movies[v])

    true_sim[(u,v)] = s

    if s >= threshold:
        true_pairs.add((u,v))


print("Pairs with TRUE similarity ≥ 0.5:",len(true_pairs))


def stable_hash(x):

    return int(hashlib.md5(str(x).encode()).hexdigest(),16)


max_hash = 2**32 - 1


def generate_hash_funcs(t):

    funcs = []

    for _ in range(t):

        a = random.randint(1,max_hash)
        b = random.randint(0,max_hash)

        funcs.append((a,b))

    return funcs


def minhash_signature(movie_set,hash_funcs):

    sig = []

    for a,b in hash_funcs:

        min_val = float("inf")

        for m in movie_set:

            h = (a*stable_hash(m) + b) % max_hash

            if h < min_val:
                min_val = h

        sig.append(min_val)

    return sig


def est_jaccard(sig1,sig2):

    match = 0

    for i in range(len(sig1)):

        if sig1[i] == sig2[i]:
            match += 1

    return match/len(sig1)


for t in t_values:

    print("\nSignature size =",t)

    fp_total = 0
    fn_total = 0

    for run in range(runs):

        hash_funcs = generate_hash_funcs(t)

        signatures = {}

        for u in users:

            signatures[u] = minhash_signature(user_movies[u],hash_funcs)

        est_pairs = set()

        for u,v in itertools.combinations(users,2):

            s = est_jaccard(signatures[u],signatures[v])

            if s >= threshold:
                est_pairs.add((u,v))


        fp = len(est_pairs - true_pairs)
        fn = len(true_pairs - est_pairs)

        fp_total += fp
        fn_total += fn


    print("Average False Positives:",fp_total/runs)
    print("Average False Negatives:",fn_total/runs)