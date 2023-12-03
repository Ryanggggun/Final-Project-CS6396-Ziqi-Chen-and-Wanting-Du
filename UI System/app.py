from flask import Flask, request, render_template, send_file
import pandas as pd
import io
from io import BytesIO
from model_utils import ModelUtils   
from reply_generator import get_chatgpt_response 
from preprocess import preprocess_text

app = Flask(__name__)
model_utils = ModelUtils()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # read data
        df = pd.read_csv(uploaded_file)
        df['content_cleaned'] = df['content'].apply(preprocess_text)

        # sentiment analysis
        df['sentiment'] = df['content_cleaned'].apply(model_utils.predict_sentiment)

        # reply negative review
        product_url = request.form['product_url']
        df['reply'] = df.apply(lambda x: get_chatgpt_response(x['content'], product_url) if x['sentiment'] == 0 else '', axis=1)

        # CSV
        selected_df = df[['content', 'reply', 'sentiment']]
        buffer = io.StringIO()
        selected_df.to_csv(buffer, index=False)
        buffer.seek(0)
        
        # show results
        global result_data
        result_data = buffer.getvalue()

        return render_template('index.html', data=selected_df.to_html(), file_ready=True)
    return 'No file uploaded'

@app.route('/download')
def download_file():
    buffer = BytesIO()
    buffer.write(result_data.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='processed_results.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)
