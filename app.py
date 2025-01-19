from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

# Load preprocessed data and trained model
data = pd.read_csv('preprocessed_data.csv')
algo = joblib.load('svd_model.pkl')

app = Flask(__name__)

def get_recommendations(user_id, num_recommendations=5):
    user_id = str(user_id)
    all_items = data['itemId'].unique()
    rated_items = data[data['userId'] == user_id]['itemId'].unique()
    unrated_items = [item for item in all_items if item not in rated_items]

    predictions = [algo.predict(user_id, item) for item in unrated_items]
    predictions.sort(key=lambda x: x.est, reverse=True)

    return [pred.iid for pred in predictions[:num_recommendations]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('userId')
    recommendations = get_recommendations(user_id)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)