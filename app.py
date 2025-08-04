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
        # These are the 8 fields used in your HTML form
        fields = ['2B', '3B', 'BB', 'SO', 'SB', 'CG', 'SHO', 'E']
        
        # Collect input values from form
        input_features = [float(request.form[field]) for field in fields]
        final_input = [input_features]  # model expects a 2D array

        # Predict using the model
        predicted_wins = model.predict(final_input)[0]
        return render_template('index.html', prediction_text=f"Predicted Wins: {round(predicted_wins, 2)}")
    
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
