# app.py

from flask import Flask, request, render_template
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load the model
with open("Wins-Score.pkl", "rb") as f:
    model = pickle.load(f)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features in correct order
        fields = ['R', 'AB', 'H', '2B', '3B', 'HR', 'BB', 'SO',
                  'SB', 'RA', 'ER', 'ERA', 'CG', 'SHO', 'SV', 'E']
        input_features = [float(request.form[field]) for field in fields]
        final_input = np.array([input_features])
        
        # Make prediction
        predicted_wins = model.predict(final_input)[0]
        return render_template('index.html', prediction_text=f"Predicted Wins: {round(predicted_wins, 2)}")
    
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
