import re, math
from collections import Counter
from api_calls import get_synonyms
import spacy
from string import punctuation

nlp = spacy.load("en_core_web_sm")
def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
    doc = nlp(text.lower()) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return result

def get_keywords(text):
    output = set(get_hotwords(text))
    no_of_keywords=int(math.sqrt(len(text)))*2
    most_common_list = Counter(output).most_common(no_of_keywords)
    keywords=[]
    for item in most_common_list:
        keywords.append(item[0])
    return keywords

def get_synonyms_for_keywords(keywords):
    synonyms={}
    for word in keywords:
        synonyms[word]=get_synonyms(word)
    return synonyms

def length_score(s1, s2):
    l1, l2 =len(s1), len(s2)
    if l1/l2 >=0.75:
        return 1
    if l1/l2 >=0.5:
        return 0.75
    if l1/l2 >=0.35:
        return 0.5
    if l1/l2 >=0.1:
        return 0.1
    else:
        return 0


def cosine_similarity(model_answer, student_answer, synonyms):
    # convert the strings to lowercase
    model_answer = model_answer.lower()
    student_answer = student_answer.lower()

    # replace each word in the input strings with its synonyms
    for word, syns in synonyms.items():
        for syn in syns:
            model_answer = re.sub(r'\b{}\b'.format(re.escape(syn)), word, model_answer)
            student_answer = re.sub(r'\b{}\b'.format(re.escape(syn)), word, student_answer)

    # split the strings into words
    words1 = re.findall('\w+', model_answer)
    words2 = re.findall('\w+', student_answer)

    # create a set of unique words from both strings
    words_set = set(words1).union(set(words2))

    # create a dictionary to store the word frequency in each string
    freq_dict1 = Counter(words1)
    freq_dict2 = Counter(words2)

    # create a vector for each string
    vector1 = [freq_dict1.get(word, 0) for word in words_set]
    vector2 = [freq_dict2.get(word, 0) for word in words_set]

    # calculate the dot product and the norm for each vector
    dot_product = sum(vector1[i] * vector2[i] for i in range(len(words_set)))
    norm1 = math.sqrt(sum(vector1[i]**2 for i in range(len(words_set))))
    norm2 = math.sqrt(sum(vector2[i]**2 for i in range(len(words_set))))

    # calculate the cosine similarity
    if norm1 == 0 or norm2 == 0:
        return 0
    else:
        return dot_product / (norm1 * norm2)

def get_score(student_answer, model_answer, keywords):
    synonyms = get_synonyms_for_keywords(keywords)
    similarity = cosine_similarity(model_answer, student_answer, synonyms)
    len_score=length_score(student_answer, model_answer)
    score=(similarity+similarity*len_score)/2
    return score
    



f_ma=open("model_answer.txt", 'r')
model_answer=f_ma.read()
f_ma.close()
f_sa=open("student_answer.txt", 'r')
student_answer=f_sa.read()
f_sa.close()

keywords=get_keywords(model_answer)
print(keywords)

score=get_score(student_answer, model_answer, keywords)
print("Score:", score)
if score >=0.95:
    print("The student's answer is an exact match with the model answer.")
elif score >= 0.75:
    print("The student's answer is very similar to the model answer.")
elif score >= 0.4:
    print("The student's answer is somewhat similar to the model answer.")
else:
    print("The student's answer is not similar to the model answer.")