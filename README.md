<H1 align="center">FasterTag</H1>
<H3 align="center">An NLP tool to grade answers based on a model answer</H3>

## How it works
- First the keywords are extracted from the model answer using spacy.
- Next, using an API, we get the synonyms for the keywords.
- Next a modified cosine similarity algorithm is run, that takes into account the synonyms.
- Finally a score is assigned based on factors like the cosine similarity, length etc.

## Steps to run Code

- Clone the repository
```
git clone https://github.com/Sahil-Amritkar/GradingBuddy.git
```

- Goto the cloned folder.
```
cd GradingBuddy
```

- Add the Model Answer to model_answer.txt
- Add the Student Answer to student_answer.txt

- Run similarity.py
```
python similarity.py
```

## Upcoming Features
- Image to text, for handwritten answers.
- More extensive NLP and context understanding for better grading.