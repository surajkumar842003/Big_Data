
bands = 20
rows = 8

def lsh_probability(s, bands, rows):
    return 1 - (1 - s**rows)**bands


jaccard_values = {
    ("D1","D2"):0.977979274611399,
    ("D1","D3"):0.5803571428571429,
    ("D1","D4"):0.3050847457627119,
    ("D2","D3"):0.5680473372781065,
    ("D2","D4"):0.30590339892665475,
    ("D3","D4"):0.31212381771281167
}

print("LSH Probability Results\n")

for pair,s in jaccard_values.items():

    p = lsh_probability(s,bands,rows)

    print(pair,"Similarity =",s,"Probability =",p)