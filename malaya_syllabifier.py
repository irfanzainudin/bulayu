import malaya

tokenizer = malaya.syllable.rules()

print(tokenizer.tokenize('aturan'))
print(tokenizer.tokenize('plastik'))
print(tokenizer.tokenize('swasta'))
print(tokenizer.tokenize('zoo'))
print(tokenizer.tokenize('angan-angan'))
print(tokenizer.tokenize('cuaca'))
print(tokenizer.tokenize('hidup'))
print(tokenizer.tokenize('insuran'))
print(tokenizer.tokenize('insurans'))
print(tokenizer.tokenize('ayam'))
print(tokenizer.tokenize('strategi'))
print(tokenizer.tokenize('hantu'))

string = 'sememang-memangnya kau sakai siot'
results = []
for w in string.split():
    results.extend(tokenizer.tokenize(w))
results

from senarai_kata import senarai_kata

parsed_sk = []
for j, k in enumerate(senarai_kata):
    parsed_sk.append(tokenizer.tokenize(k))

with open("malaya_parsed.py", "w") as mp:
    mp.write(str(parsed_sk))