from sklearn.feature_extraction.text import TfidfVectorizer

doc1 = "I like apples. I like oranges too"
doc2 = "I love apples. I hate doctors"
doc3 = "An apple a day keeps the doctor away"
doc4 = "Never compare an apple to an orange"

documents = [doc1, doc2, doc3, doc4]

tfidf = TfidfVectorizer().fit_transform(documents)
sim = tfidf * tfidf.T

print(sim.A) # 4*4的矩阵 转成Array的形式