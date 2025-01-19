import pandas as pd
import joblib
import cProfile

# Load preprocessed data and trained model
data = pd.read_csv('preprocessed_data.csv')
algo = joblib.load('svd_model.pkl')

def get_recommendations(user_id, num_recommendations=5):
    user_id = str(user_id)
    all_items = data['itemId'].unique()
    rated_items = data[data['userId'] == user_id]['itemId'].unique()
    unrated_items = [item for item in all_items if item not in rated_items]

    # Make batch predictions
    predictions = algo.test([(user_id, item, 0) for item in unrated_items])
    predictions.sort(key=lambda x: x.est, reverse=True)

    return [pred.iid for pred in predictions[:num_recommendations]]

def main():
    # Example usage
    user_ids_to_test = [1, 2, 3]
    for uid in user_ids_to_test:
        print(f"Recommendations for user {uid}: {get_recommendations(uid)}")

# Profile the code
cProfile.run('main()')