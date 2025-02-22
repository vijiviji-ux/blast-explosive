from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import joblib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Load the model
loaded_model = joblib.load('mlp_model.pkl')

# Dummy user credentials (replace with your authentication logic)
USER_CREDENTIALS = {'username': 'admin', 'password': 'password'}

# Email configurations
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_FROM = 'daminmain@gmail.com'
EMAIL_PASSWORD = 'kpqtxqskedcykwjz'
EMAIL_TO = 'dinorni97@gmail.com'

# Prediction function
def predict_explosiveness(input_data):
    prediction = loaded_model.predict(input_data)
    if prediction == 1:
        return 'Explosive'
    else:
        return 'Non-Explosive'

def send_email(result):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = 'Prediction Result'

    body = f'The prediction result is: {result}'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_FROM, EMAIL_TO, text)
    server.quit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input data from the form
        input_data = {
            'Oxygen Balance': float(request.form['oxygen_balance']),
            'Carbon Content': float(request.form['carbon_content']),
            'Nitrogen Content': float(request.form['nitrogen_content']),
            'Hydrogen Content': float(request.form['hydrogen_content']),
            'Sulfur Content': float(request.form['sulfur_content']),
            'Density': float(request.form['density']),
            'Melting Point': float(request.form['melting_point']),
            'Boiling Point': float(request.form['boiling_point'])
        }
        
        input_df = pd.DataFrame(input_data, index=[0])  # Convert input data to DataFrame
        result = predict_explosiveness(input_df)
        send_email(result)  # Send email with prediction result
        return render_template('result.html', result=result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
