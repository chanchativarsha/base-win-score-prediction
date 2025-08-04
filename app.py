from flask import Flask, request, render_template
import pickle
import os

app = Flask(__name__)

# Load the model
with open("Wins-Score.pkl", "rb") as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        fields = ['R', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'SO',
                  'SB', 'RA', 'ER', 'ERA', 'CG', 'SHO', 'SV', 'E']
        input_features = [float(request.form[field]) for field in fields]
        final_input = [input_features]  # plain Python list of lists

        predicted_wins = model.predict(final_input)[0]
        return render_template('index.html', prediction_text=f"Predicted Wins: {round(predicted_wins, 2)}")
    
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
