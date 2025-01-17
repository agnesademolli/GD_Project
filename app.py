from flask import Flask, send_from_directory, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
import re
import os

app = Flask(__name__, static_folder='gdPROJECT (1)/', template_folder='gdPROJECT (1)')


# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///services.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['MAIL_SERVER'] = 'smtp.ubt-uni.net'  
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USERNAME'] = 'ubt@ubt-uni.net'  
app.config['MAIL_PASSWORD'] = 'Ubt123'  
app.config['MAIL_DEFAULT_SENDER'] = 'ubt123@ubt-uni.net'  


db = SQLAlchemy(app)




login_manager = LoginManager(app)
from auth import auth
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index (1).html')

# Define the Service model
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Serve the main HTML files
@app.route('/')
def index():
    return render_template('index (1).html')

@app.route('/service')
def service():
    return render_template('service (1).html')

@app.route('/about')
def about():
    return render_template('about (1).html')

@app.route('/team')
def team():
    return render_template('team (1).html')

@app.route('/why')
def why():
    return render_template('why (1).html')

# Serve static files (CSS, JS, Images, Fonts)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.static_folder), filename)

# CRUD Operations for Services

# Create a new service
@app.route('/api/services', methods=['POST'])
def create_service():
    data = request.get_json()
    new_service = Service(name=data['name'], description=data['description'])
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message": "Service created successfully!"}), 201

# Read all services
@app.route('/api/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    services_list = [{"id": s.id, "name": s.name, "description": s.description} for s in services]
    return jsonify(services_list)

# Update a service
@app.route('/api/services/<int:id>', methods=['PUT'])
def update_service(id):
    data = request.get_json()
    service = Service.query.get_or_404(id)
    service.name = data['name']
    service.description = data['description']
    db.session.commit()
    return jsonify({"message": "Service updated successfully!"})

# Delete a service
@app.route('/api/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully!"})


@app.route('/monthly_payment', methods=['POST'])
def monthly_payment():
    try:
        principal = float(request.json.get('principal', 0))
        annual_interest_rate = float(request.json.get('annual_interest_rate', 0))
        years = int(request.json.get('years', 0))

        if principal <= 0 or annual_interest_rate <= 0 or years <= 0:
            return jsonify({"error": "Invalid input values"}), 400

        monthly_rate = annual_interest_rate / 12 / 100
        total_payments = years * 12
        monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -total_payments)

        return jsonify({
            "principal": principal,
            "annual_interest_rate": annual_interest_rate,
            "years": years,
            "monthly_payment": round(monthly_payment, 2)
        }), 200
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input data"}), 400




#Contact form************

# Helper function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Ensure the email provided is valid
        if not is_valid_email(email):
            return jsonify({"message": "Invalid email address."}), 400
        
        # Use the user's email as the sender
        msg = Message('New Contact Form Submission',
                      sender=email,  # Dynamic sender address from the form
                      recipients=['support@ubt-uni.net.com']) 
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        
        # Send the email
        try:
            mail.send(msg)
            return jsonify({"message": "Your message has been sent!"}), 200
        except Exception as e:
            return jsonify({"message": f"Failed to send email. Error: {str(e)}"}), 500

    return render_template('ContactForm.html')




if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)