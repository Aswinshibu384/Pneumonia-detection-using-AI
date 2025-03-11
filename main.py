from flask import Flask, render_template, request, redirect, jsonify, session
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pymysql
from functools import wraps
import jwt
import datetime
from flask_cors import CORS

from flask_cors import CORS
import mysql.connector
import traceback
import bcrypt  

app = Flask(__name__)
CORS(app)  # Enable CORS to prevent cross-origin issues
app.secret_key = 'your_secret_key'

# ✅ Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shibu",
    database="pneumonia_db"
)
cursor = db.cursor()

# ✅ Home Route
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Register & Login Page Routes
@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

# ✅ Register API (Using Bcrypt for Password Hashing)
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid JSON format'}), 400

        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not username or not password or role not in ['doctor', 'patient']:
            return jsonify({'message': 'Invalid input data'}), 400

        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 409

        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                       (username, hashed_password, role))
        db.commit()

        return jsonify({'message': f'User {username} registered successfully as {role}', 'redirect': '/login'}), 201

    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

# ✅ Login API (Now Using Hashed Password Verification)
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        cursor.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'message': 'Invalid username or password'}), 401

        stored_password = user[1]

        # ✅ Check if password is already hashed
        if stored_password.startswith('$2b$'):  # Bcrypt hashes always start with $2b$
            if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return jsonify({'message': 'Invalid username or password'}), 401
        else:
            # 🔥 Convert old plaintext passwords to hashed ones
            new_hashed_password = bcrypt.hashpw(stored_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hashed_password, user[0]))
            db.commit()

            # Now check with newly hashed password
            if not bcrypt.checkpw(password.encode('utf-8'), new_hashed_password.encode('utf-8')):
                return jsonify({'message': 'Invalid username or password'}), 401

        session['user_id'] = user[0]
        session['username'] = username
        session['role'] = user[2]

        role_redirects = {
            'admin': '/admin_dashboard',
            'doctor': '/doctor_dashboard',
            'patient': '/patient_dashboard'
        }

        return jsonify({'message': 'Login successful', 'redirect': role_redirects.get(user[2], '/'), 'role': user[2]})

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500




# ✅ Dashboard Routes
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('Admin/admin_dashboard.html')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('Doctor/doctor_dashboard.html')

@app.route('/patient_dashboard')
def patient_dashboard():
    return render_template('Patient/patient_dashboard.html')

def decode_auth_token(auth_token):
    """ Decodes the authentication token """
    try:
        payload = jwt.decode(auth_token, app.secret_key, algorithms=["HS256"])
        return payload["user_id"]  # Ensure it returns user ID
    except jwt.ExpiredSignatureError:
        return None  # Expired token
    except jwt.InvalidTokenError:
        return None  # Invalid token





@app.route('/patient/profile', methods=['GET'])
def get_patient_profile():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = session['user_id']

    cursor.execute("SELECT name, age, gender, contact FROM patients WHERE user_id=%s", (user_id,))
    patient = cursor.fetchone()

    if patient:
        return jsonify({"name": patient[0], "age": patient[1], "gender": patient[2], "contact": patient[3]})

    return jsonify({"message": "Profile not found"}), 404

# Login Route
@app.route('/login', methods=['POST'])
def patient_login():  # Change from 'login' to 'patient_login'
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cursor.execute("SELECT id, role FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if not user or user[1] != 'patient':
        return jsonify({"message": "Invalid credentials"}), 401

    session['user_id'] = user[0]  # Store user ID in session

    return jsonify({"message": "Login successful"})


# Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"})

#Book Appointment
@app.route('/api/doctors', methods=['GET'])
def fetch_doctors():
    try:
        cursor.execute("SELECT id, name, specialization FROM doctors")
        doctors = cursor.fetchall()
        
        if not doctors:
            return jsonify([]), 200  # Return empty list if no doctors
         
        doctor_list = [{"id": d[0], "name": d[1], "specialization": d[2]} for d in doctors]
        return jsonify(doctor_list), 200
    except Exception as e:
        print("Error fetching doctors:", e)
        return jsonify({"error": "Failed to fetch doctors"}), 500


@app.route('/api/book_appointment', methods=['POST'])
def book_appointment():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        data = request.get_json()
        doctor_id = data.get("doctor_id")
        appointment_date = data.get("appointment_date")
        patient_id = session['user_id']

        if not doctor_id or not appointment_date:
            return jsonify({"message": "All fields are required"}), 400

        cursor.execute(
            "INSERT INTO appointments (doctor_id, patient_id, appointment_date) VALUES (%s, %s, %s)",
            (doctor_id, patient_id, appointment_date)
        )
        db.commit()

        return jsonify({"message": "Appointment booked successfully"}), 201

    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        return jsonify({"message": "Failed to book appointment", "error": str(e)}), 500

@app.route('/api/get_appointments', methods=['GET'])
def get_appointments():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401

    try:
        patient_id = session['user_id']
        cursor.execute("""
            SELECT doctors.name, doctors.specialization, appointments.appointment_date 
            FROM appointments 
            INNER JOIN doctors ON appointments.doctor_id = doctors.id 
            WHERE appointments.patient_id = %s
        """, (patient_id,))
        appointments = cursor.fetchall()

        appointment_list = [{"doctor_name": a[0], "specialization": a[1], "appointment_date": a[2]} for a in appointments]
        return jsonify(appointment_list), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"message": "Failed to fetch appointments", "error": str(e)}), 500





@app.route('/patient/upload_xray', methods=['POST'])
def upload_xray():
    file = request.files['xray_image']
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join("uploads", filename)
        file.save(file_path)

        # ✅ Pass the image to the pneumonia detection model
        result = predict_pneumonia(file_path)  # Function to predict pneumonia

        return jsonify({"message": "X-ray uploaded successfully", "result": result})
    return jsonify({"message": "Failed to upload X-ray"}), 400

@app.route('/patient/prescriptions', methods=['GET'])
def get_prescriptions():
    token = request.headers.get('x-access-token')
    user_data = decode_auth_token(token)
    if not user_data:
        return jsonify({"message": "Invalid or expired token"}), 401
    user_id = user_data


    cursor.execute("""
        SELECT d.name as doctor_name, p.medicine, p.date 
        FROM prescriptions p
        JOIN doctors d ON p.doctor_id = d.id
        WHERE p.patient_id = (SELECT id FROM patients WHERE user_id = %s)
    """, (user_id,))

    prescriptions = cursor.fetchall()
    if prescriptions:
        return jsonify([{"doctor_name": p[0], "medicine": p[1], "date": p[2]} for p in prescriptions])
    return jsonify([])


@app.route('/api/register_patient', methods=['POST'])
def register_patient():
    try:
        data = request.get_json()
        name = data.get("name")
        age = data.get("age")
        gender = data.get("gender")
        contact = data.get("contact")
        password = data.get("password")

        if not name or not password or not age or not gender or not contact:
            return jsonify({"message": "All fields are required"}), 400

        # ✅ Hash the password before storing
        #hashed_password = generate_password_hash(password)

        # ✅ Insert into `users` table
        
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (name, password, 'patient')
        )
        db.commit()

        # ✅ Get the `user_id` of the newly created user
        user_id = cursor.lastrowid

        # ✅ Insert into `patients` table
        cursor.execute(
            "INSERT INTO patients (name, age, gender, contact, user_id) VALUES (%s, %s, %s, %s, %s)",
            (name, age, gender, contact, user_id)
        )
        db.commit()

        return jsonify({"message": "Patient registered successfully"}), 201

    except mysql.connector.Error as err:
        db.rollback()
        print("MySQL Error:", err)  # Debugging
        return jsonify({"message": "Database Error", "error": str(err)}), 500

    except Exception as e:
        db.rollback()
        print("General Error:", e)  # Debugging
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500

@app.route('/admin/patients', methods=['GET'])
def get_patients():
    """ Fetch all patients """
    try:
        cursor.execute("SELECT id, name, age, gender, contact FROM patients")
        patients = cursor.fetchall()
        patient_list = [
            {"id": p[0], "name": p[1], "age": p[2], "gender": p[3], "contact": p[4]}
            for p in patients
        ]
        return jsonify(patient_list), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch patients", "error": str(e)}), 500

@app.route('/admin/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    """ View and update patient details """
    try:
        if request.method == 'GET':
            # Fetch patient details
            cursor.execute("SELECT id, name, age, gender, contact FROM patients WHERE id=%s", (patient_id,))
            patient = cursor.fetchone()

            if not patient:
                return "Patient not found", 404

            return render_template("Admin/edit_patient.html", patient={
                "id": patient[0], "name": patient[1], "age": patient[2], "gender": patient[3], "contact": patient[4]
            })

        if request.method == 'POST':
            name = request.form.get("name")
            age = request.form.get("age")
            gender = request.form.get("gender")
            contact = request.form.get("contact")

            if not name or not age or not gender or not contact:
                return jsonify({"message": "All fields are required"}), 400

            cursor.execute(
                "UPDATE patients SET name=%s, age=%s, gender=%s, contact=%s WHERE id=%s",
                (name, age, gender, contact, patient_id)
            )
            db.commit()

            return redirect(url_for('manage_patient'))


    except Exception as e:
        db.rollback()
        
@app.route('/admin/delete_patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """ Delete a patient from the database """
    try:
        cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
        db.commit()
        return jsonify({"message": "Patient deleted successfully"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"message": "Failed to delete patient", "error": str(e)}), 500




@app.route('/manage_doctors')
def manage_doctors():
    return render_template('Admin/manage_doctor.html')

@app.route('/manage_patient')
def manage_patient():
    return render_template('Admin/manage_patients.html')

@app.route('/admin_doctors')
def admin_doctors():
    return render_template('Admin/admin_doctors.html')

@app.route('/admin_patient')
def admin_patient():
    return render_template('Admin/admin_patients.html')

@app.route('/edit_doctor.html')
def edit_doctor_page():
    return render_template('Admin/edit_doctor.html')

@app.route('/admin/update_doctor/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    try:
        data = request.get_json()
        name = data.get("name")
        specialization = data.get("specialization")
        contact = data.get("contact")

        if not name or not specialization or not contact:
            return jsonify({"message": "All fields are required"}), 400

        cursor.execute(
            "UPDATE doctors SET name = %s, specialization = %s, contact = %s WHERE id = %s",
            (name, specialization, contact, doctor_id)
        )
        db.commit()

        return jsonify({"message": "Doctor details updated successfully"}), 200

    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        return jsonify({"message": "Failed to update doctor", "error": str(e)}), 500




# ✅ Doctor Management APIs
@app.route('/admin/doctors', methods=['GET'])
def get_doctors():
    try:
        cursor.execute("SELECT id, name, specialization, contact FROM doctors")
        doctors = cursor.fetchall()
        doctor_list = [{"id": doc[0], "name": doc[1], "specialization": doc[2], "contact": doc[3]} for doc in doctors]

        return jsonify(doctor_list), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"message": "Failed to retrieve doctors", "error": str(e)}), 500

@app.route('/admin/delete_doctor/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    try:
        cursor.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
        db.commit()
        return jsonify({'message': 'Doctor deleted successfully'}), 200

    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        return jsonify({'message': 'Failed to delete doctor', 'error': str(e)}), 500

@app.route('/admin/get_doctor/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    try:
        cursor.execute("SELECT id, name, specialization, contact FROM doctors WHERE id = %s", (doctor_id,))
        doctor = cursor.fetchone()

        if not doctor:
            return jsonify({'message': 'Doctor not found'}), 404

        return jsonify({'id': doctor[0], 'name': doctor[1], 'specialization': doctor[2], 'contact': doctor[3]}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'message': 'Failed to fetch doctor details', 'error': str(e)}), 500

# @app.route('/edit_doctor')
# def edit_doctor_page():
#     return render_template('edit_doctor.html')

@app.route('/api/register_doctor', methods=['POST'])
def register_doctor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid JSON format'}), 400

        name = data.get('name')
        specialization = data.get('specialization')
        contact = data.get('contact')
        password = data.get('password')

        if not name or not specialization or not contact or not password:
            return jsonify({'message': 'All fields are required'}), 400

        # Hash the password before storing
        # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert into `users` table (Role = doctor)
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                       (name, password, 'doctor'))
        db.commit()
        user_id = cursor.lastrowid  # Get the inserted user ID

        # Insert into `doctors` table
        cursor.execute("INSERT INTO doctors (name, specialization, contact, user_id) VALUES (%s, %s, %s, %s)",
                       (name, specialization, contact, user_id))
        db.commit()

        return jsonify({'message': 'Doctor registered successfully'}), 201

    except Exception as e:
        db.rollback()
        print(traceback.format_exc())
        return jsonify({'message': 'Doctor registration failed', 'error': str(e)}), 500

# ✅ Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
