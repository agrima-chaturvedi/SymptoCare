from flask import Flask, render_template, request, redirect, url_for, session, flash
from joblib import load
import pandas as pd
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mahi123'
app.config['MYSQL_DB'] = 'disease_prediction'

mysql = MySQL(app)
bcrypt = Bcrypt(app)




# Load ML model and data
model = load("decision_tree_model (1).joblib")
df = pd.read_csv("Symptom-severity.csv")
disc = pd.read_csv("symptom_Description.csv")
precaut = pd.read_csv("symptom_precaution.csv")
doctors = pd.read_csv('Doctor_final.csv', encoding='latin1')

doctors.rename(columns={"Name of Doctor": "Name"}, inplace=True)
disease_to_specialist = {
    # 🦠 Infections & Allergies
    'Fungal infection': 'Dermatologist',
    'Allergy': 'Dermatologist',
    'Chickenpox': 'Dermatologist',
    'Common Cold': 'Infectious Disease Specialist',
    'Pneumonia': 'Pulmonologist',

    # 🍽️ Digestive Issues
    'GERD': 'Gastroenterologist',
    'Chronic cholestasis': 'Gastroenterologist',
    'Peptic ulcer disease': 'Gastroenterologist',
    'Gastroenteritis': 'Gastroenterologist',
    'Jaundice': 'Gastroenterologist',
    'Hemorrhoids': 'Proctologist',

    # 🚨 Serious Conditions
    'AIDS': 'Immunologist',
    'Diabetes': 'Endocrinologist',
    'Heart attack': 'Cardiologist',
    'Hypertension': 'Cardiologist',
    'Tuberculosis': 'Infectious Disease Specialist',

    # 🧠 Neurological Disorders
    'Migraine': 'Neurologist',
    'Paralysis (brain hemorrhage)': 'Neurologist',
    'Vertigo': 'Neurologist',

    # 🏥 Liver Diseases
    'Hepatitis A': 'Gastroenterologist',
    'Hepatitis B': 'Gastroenterologist',
    'Hepatitis C': 'Gastroenterologist',
    'Hepatitis D': 'Gastroenterologist',
    'Hepatitis E': 'Gastroenterologist',
    'Alcoholic hepatitis': 'Gastroenterologist',

    # 🦟 Mosquito-Borne Diseases
    'Malaria': 'Infectious Disease Specialist',
    'Dengue': 'Infectious Disease Specialist',
    'Typhoid': 'Infectious Disease Specialist',

    # 🧬 Thyroid & Hormonal Disorders
    'Hypothyroidism': 'Endocrinologist',
    'Hyperthyroidism': 'Endocrinologist',
    'Hypoglycemia': 'Endocrinologist',

    # 🫁 Respiratory
    'Bronchial Asthma': 'Pulmonologist',

    # 🦴 Joint & Bone
    'Osteoarthritis': 'Orthopedist',
    'Arthritis': 'Orthopedist',
    'Cervical spondylosis': 'Neurologist',

    # 🧖 Skin Conditions
    'Acne': 'Dermatologist',
    'Psoriasis': 'Dermatologist',
    'Impetigo': 'Dermatologist',

    # 💊 Other
    'Drug Reaction': 'Immunologist',
    'Urinary tract infection': 'Urologist',
    'Varicose veins': 'Proctologist',
}

@app.route("/home", methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier') 
        password = request.form.get('password')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE patient_name = %s OR email = %s", (identifier, identifier))
        user = cur.fetchone()
        cur.close()

        print(f"Entered Identifier: {identifier}")
        print(f"Entered Password: {password}")

        if user:
            print(f"User found: {user}")

            # Assuming password is stored in 4th column (index 3)
            if bcrypt.check_password_hash(user[4], password):
                session['patient_name'] = user[3]  # Assuming name is at index 3
                return redirect(url_for('home'))
            else:
                flash("Incorrect password. Please try again.", "danger")
        else:
            flash("User not found. Please check your credentials.", "danger")

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        patient_name = request.form.get('patient_name')
        password = request.form.get('new-password')
        print("Received Signup Data:", name, email, patient_name, password)
        if not password:
            flash("Password cannot be empty.", "warning")
            return redirect(url_for('signup'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (name,email,patient_name,password) VALUES (%s,%s, %s, %s)",
                        (name,email,patient_name,hashed_pw))
        print("Received Signup Data:", name, email, phone, patient_name, password)
        mysql.connection.commit()
        cur.close()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

        

    return render_template('login.html')


@app.route("/predict", methods=["POST"])
def predict():
    # Extract symptoms and prediction
    symptoms = [request.form.get(f"S{i}") for i in range(1, 9)]
    city = request.form.get("City", "").strip()
    state = request.form.get("State", "").strip()

    a = np.array(df["Symptom"])
    b = np.array(df["weight"])
    weights = []

    for s in symptoms:
        found = False
        for k in range(len(a)):
            if s == a[k]:
                weights.append(b[k])
                found = True
                break
        if not found:
            weights.append(0)

    psy = [weights]
    pred = model.predict(psy)[0]

    # Description & precautions
    description = disc[disc["Disease"] == pred].values[0][1]
    c = np.where(precaut["Disease"] == pred)[0][0]
    precaution_list = [precaut.iloc[c, i] 
    for i in range(1, len(precaut.iloc[c])) 
    if isinstance(precaut.iloc[c, i], str)]

    # Doctor recommendation
    specialist = disease_to_specialist.get(pred, "General Physician")
    matched = [
    {
        "name": str(row.get("Name", "N/A")),
        "specialist": str(row.get("Speciality", "N/A")),
        "city": str(row.get("City", "N/A")),
        "state": str(row.get("State", "N/A")),
        "phone": str(row.get("Phone No", "N/A")),
        "rating":str(row.get("Rating","N/A"))
    }
    for _, row in doctors.iterrows()
    if str(row.get("Speciality", "")).lower() == specialist.lower()
       and city.lower() in str(row.get("City", "")).lower()
]
    level = "City"
    region = city

    if not matched:
        matched = [
        {
            "name": str(row.get("Name", "N/A")).strip(),
            "specialist": str(row.get("Speciality", "N/A")).strip(),
            "city": str(row.get("City", "N/A")).strip(),
            "state": str(row.get("State", "N/A")).strip(),
        }
        for _, row in doctors.iterrows()
        if str(row.get("Speciality", "")).strip().lower() == specialist.lower()
           and state.lower() in str(row.get("State", "")).strip().lower()
    ]
    level = "State"
    region = state

    # Insert the patient name and predicted disease into the database
    patient_name = session.get('patient_name', None)  # Get logged-in patient's name from session
    print(f"Patient Name: {patient_name}")
    if patient_name:
        # Insert into patients table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO patients (patient_name, predicted_disease) VALUES (%s, %s)", (patient_name, pred))
        mysql.connection.commit()
        cur.close()

    # Return the result
    result = {
        "disease": pred,
        "description": description,
        "precautions": precaution_list,
        "doctors": matched,
        "level": level,
        "region": region
    }

    return render_template("predict.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

