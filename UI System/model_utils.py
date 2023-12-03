from joblib import load

class ModelUtils:
    def __init__(self):
        # load model
        self.model = load('/Users/wantingdu/Downloads/Final_Project/logistic_regression_model.joblib')
        self.tfidf_vectorizer = load('/Users/wantingdu/Downloads/Final_Project/tfidf_vectorizer.joblib')

    def predict_sentiment(self, text):
        text_tfidf = self.tfidf_vectorizer.transform([text])
        # predict
        return self.model.predict(text_tfidf)[0]
