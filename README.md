# Information Retrival and Sentiment Analysis on Indeed Reviews

This project performs sentiment analysis on company reviews collected from [Indeed Salaries](https://www.indeed.com/career/salaries).

---

## 🧩 Project Components
1. **Data Crawling**
   - Collected reviews of top-paying companies by industry.
   - Focused on formal review content, minimizing noise like emojis and slang.

2. **Indexing and Search**
   - Preprocessed text using **NLTK** (tokenization, stemming, cleanup).  
   - Built **Elasticsearch inverted index** for near-real-time full-text search.  
   - Developed a simple **UI** with bar charts, line charts, histograms, word clouds, and interactive search.

3. **Sentiment Analysis**
   - Created training, validation, and test sets with labeled data.  
   - Compared embedding methods: **BERT outperformed BoW**, capturing context effectively.  
   - Evaluated models: Multinomial Naive Bayes, SVM, XGBoost, and BERT.

4. **Enhanced Classification**
   - Applied **ensemble methods** (majority voting, stacking with logistic regression, random forest, XGBoost).  
   - **Best results:** 94.3% accuracy for polarity detection, 73.5% for subjectivity detection.

---

## 🧰 Tech Stack
- Python, NLTK, Scikit-learn, BERT (Transformers), XGBoost  
- Elasticsearch, Flask/Streamlit for UI  
- Pandas, NumPy, Matplotlib, WordCloud  

---

## 🏁 Key Outcomes
- Successfully crawled and indexed company reviews with searchable interface.  
- Demonstrated strong sentiment analysis performance using **BERT** and ensembles.  
- Explored ensemble techniques for improved generalization and subjectivity detection.
