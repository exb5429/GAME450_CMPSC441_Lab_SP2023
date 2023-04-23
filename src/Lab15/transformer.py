from sentence_transformers import SentenceTransformer, util

answer1 = "According to the International Shark Attack File, there were 11 confirmed deaths from shark attacks worldwide in 2021. However, it's important to note that the risk of a shark attack is still relatively low, with only a small number of fatal attacks occurring each year compared to the millions of people who swim in the ocean. It's also worth noting that many shark species are endangered, and conservation efforts are essential to protect these important and fascinating creatures."
answer2= "According to the International Shark Attack File, there were 10 confirmed deaths from unprovoked shark attacks worldwide in 2020. It's important to note that the risk of a shark attack is still relatively low, with only a small number of fatal attacks occurring each year compared to the millions of people who swim in the ocean. However, it's essential to take precautions when swimming in the ocean to minimize the risk of an encounter with a shark."

sentences1 = answer1.split(". ")
sentences2 = answer2.split(". ")


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

if __name__ == "__main__":
    for sentence1 in sentences1:
        for sentence2 in sentences2:
            embedding_1 = model.encode(sentence1, convert_to_tensor=True)
            embedding_2 = model.encode(sentence2, convert_to_tensor=True)
            print(util.pytorch_cos_sim(embedding_1, embedding_2))
    



