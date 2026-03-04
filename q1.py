import random
import itertools
import os
import hashlib

random.seed(42)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().lower()
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        return text   


D1 = read_file("minhash/D1.txt")
D2 = read_file("minhash/D2.txt")
D3 = read_file("minhash/D3.txt")
D4 = read_file("minhash/D4.txt")

docs = [D1, D2, D3, D4]
doc_names = ["D1","D2","D3","D4"]


def char_kgrams(text, k):

    grams = set()

    for i in range(len(text) - k + 1):
        gram = text[i:i+k]

        if len(gram) == k:
            grams.add(gram)

    return grams


def word_kgrams(text, k):

    words = text.split()
    grams = set()

    for i in range(len(words) - k + 1):
        grams.add(" ".join(words[i:i+k]))

    return grams



os.makedirs("kgrams_output", exist_ok=True)


def save_kgrams(filename, grams):

    with open("kgrams_output/" + filename, 'w', encoding='utf-8') as f:

        for g in sorted(grams):
            f.write(g + "\n")



char2_sets = []
char3_sets = []
word2_sets = []

for i, doc in enumerate(docs):

    name = doc_names[i]

    c2 = char_kgrams(doc,2)
    c3 = char_kgrams(doc,3)
    w2 = word_kgrams(doc,2)

    char2_sets.append(c2)
    char3_sets.append(c3)
    word2_sets.append(w2)

    save_kgrams(name+"_char2grams.txt", c2)
    save_kgrams(name+"_char3grams.txt", c3)
    save_kgrams(name+"_word2grams.txt", w2)

print("K-grams saved to folder: kgrams_output\n")



def jaccard(A, B):

    intersection = len(A & B)
    union = len(A | B)

    if union == 0:
        return 0

    return intersection / union


pairs = list(itertools.combinations(range(4),2))


print("================================")
print("Exact Jaccard Similarity Results")
print("================================\n")


print("CHARACTER 2-GRAMS\n")

for i,j in pairs:

    sim = jaccard(char2_sets[i], char2_sets[j])

    print(f"{doc_names[i]} vs {doc_names[j]} : {sim}")


print("\nCHARACTER 3-GRAMS\n")

for i,j in pairs:

    sim = jaccard(char3_sets[i], char3_sets[j])

    print(f"{doc_names[i]} vs {doc_names[j]} : {sim}")


print("\nWORD 2-GRAMS\n")

for i,j in pairs:

    sim = jaccard(word2_sets[i], word2_sets[j])

    print(f"{doc_names[i]} vs {doc_names[j]} : {sim}")



def stable_hash(x):

    return int(hashlib.md5(x.encode()).hexdigest(),16)



max_hash = 2**32 - 1


def generate_hash_functions(t):

    hash_funcs = []

    for _ in range(t):

        a = random.randint(1, max_hash)
        b = random.randint(0, max_hash)

        hash_funcs.append((a,b))

    return hash_funcs


def compute_minhash_signature(shingles, hash_funcs):

    shingles = list(shingles)

    signature = []

    for a,b in hash_funcs:

        min_hash = min(((a*stable_hash(s)+b) % max_hash) for s in shingles)

        signature.append(min_hash)

    return signature


def minhash_similarity(sig1, sig2):

    match = 0

    for i in range(len(sig1)):

        if sig1[i] == sig2[i]:
            match += 1

    return match / len(sig1)


print("\n================================")
print("MinHash Approximation (D1 vs D2)")
print("================================\n")

g1 = char_kgrams(D1,3)
g2 = char_kgrams(D2,3)

t_values = [20,60,150,300,600]

for t in t_values:

    hash_funcs = generate_hash_functions(t)

    sig1 = compute_minhash_signature(g1, hash_funcs)
    sig2 = compute_minhash_signature(g2, hash_funcs)

    sim = minhash_similarity(sig1, sig2)

    print(f"t = {t} -> Approx Jaccard Similarity = {sim}")