# 🧠 Disease Prediction and Doctor Recommendation System

A web-based intelligent health assistant that predicts diseases based on symptoms and recommends doctors based on location and specialization. Built using **Flask**, **MySQL**, and **Machine Learning**.

## 🔍 Overview

This system allows users to:

- Sign up and log in securely.
- Enter symptoms to predict the most likely disease using a trained Decision Tree model.
- View disease description and health precautions.
- Get a list of relevant doctors in their city/state based on specialization.
- Save predicted disease records in the MySQL database.

---

## 🚀 Features

- 🔐 Secure user authentication using bcrypt.
- 💡 Disease prediction from symptoms via ML model.
- 📖 Detailed disease information and precautions.
- 👨‍⚕️ Doctor recommendations with contact & ratings.
- 📊 Patient prediction history stored in a database.

---

## 🛠️ Tech Stack

| Technology | Purpose                     |
|------------|-----------------------------|
| Flask      | Web framework (backend)     |
| HTML/CSS   | Frontend templates          |
| MySQL      | Database                    |
| joblib     | Load ML model               |
| pandas     | Data manipulation           |
| bcrypt     | Password hashing            |
| scikit-learn | ML model (Decision Tree)  |

---

## 📁 Project Structure
project-root/<br>
│<br>
├── app.py # Main Flask application<br>
├── decision_tree_model.joblib # Trained ML model<br>
├── Symptom-severity.csv # Symptom severity data<br>
├── symptom_Description.csv # Disease descriptions<br>
├── symptom_precaution.csv # Disease precautions<br>
├── Doctor_final.csv # Doctor info dataset<br>
│<br>
├── templates/<br>
│ ├── login.html<br>
│ ├── index.html<br>
│ └── predict.html<br>
│<br>
├── static/<br>
│ └── (CSS/JS/images files)<br>
│<br>
└── README.md<br>

---

## 🧪 Setup Instructions (Local)

### 1. Clone the repository
git clone https://github.com/agrima-chaturvedi/SymptoCare.git
cd SymptoCare

### 2. Configure MySQL

Create a database named disease_prediction.<br>
Create the following tables:<br>
CREATE TABLE user (<br>
    id INT AUTO_INCREMENT PRIMARY KEY,<br>
    name VARCHAR(100),<br>
    email VARCHAR(100),<br>
    patient_name VARCHAR(100),<br>
    password VARCHAR(255)<br>
);<br>

CREATE TABLE patients (<br>
    id INT AUTO_INCREMENT PRIMARY KEY,<br>
    patient_name VARCHAR(100),<br>
    predicted_disease VARCHAR(100)<br>
);<br>

### 3. Update your MySQL credentials in app.py:

app.config['MYSQL_HOST'] = 'localhost'<br>
app.config['MYSQL_USER'] = 'your_username'<br>
app.config['MYSQL_PASSWORD'] = 'your_password'<br>
app.config['MYSQL_DB'] = 'disease_prediction'<br>

### 4. Run the application<br>

python app.py<br>
Visit http://127.0.0.1:5000 in your browser.
---

## 📸 Screenshots
🔐 Login Page
![image](https://github.com/user-attachments/assets/fd44b7da-39d1-4a04-8fca-649720ccf861)
📝 Signup Page
![image](https://github.com/user-attachments/assets/4c6ff78a-f597-4708-84b5-553011922549)
🏠 Home Page
![image](https://github.com/user-attachments/assets/8de8a36c-6cef-470d-89e5-603862c230d3)
![image](https://github.com/user-attachments/assets/257dde6a-c8d0-4ace-abdc-87b55d29eba2)
📄 Prediction Results & 👨‍⚕️ Doctor Recommendations
![image](https://github.com/user-attachments/assets/6ada807f-72b8-46bd-9326-9d787bd7f7e9)


🌱 Future Improvements

Here are some potential enhancements:

  📍 Add location-based map integration for doctor clinics using Google Maps API.<br>
  🗣️ Integrate chatbot for symptom input via natural language.<br>
  🛡️ Add session management and CSRF protection for security.<br>
  📈 Admin dashboard for analytics and doctor/patient management.<br>
  📆 Doctor appointment booking system with calendar integration.<br>
  
🧑‍💻 Author

Agrima Chaturvedi<br>
Email: [agrimachaturvedi6@gmail.com]<br>
GitHub: https://github.com/agrima-chaturvedi

  Ensure the CSV files and model are placed in the root directory.<br>
  If deploying with SQLite instead of MySQL for simplicity, minor code changes are needed.<br>
  Keep your secret key and DB passwords secure (use .env files in production).<br>

📜 License

This project is licensed under the MIT License.

🩺 Empowering proactive health with intelligent diagnostics.
---


