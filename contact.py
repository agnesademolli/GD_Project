from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.example.com'  
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USERNAME'] = 'your_email@example.com'  
app.config['MAIL_PASSWORD'] = 'your_email_password'  
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Create the email message
        msg = Message('New Contact Form Submission',
                      sender='your_email@example.com',
                      recipients=['support@example.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        
        # Send the email
        try:
            mail.send(msg)
            return jsonify({"message": "Your message has been sent!"}), 200
        except Exception as e:
            return jsonify({"message": f"Failed to send email. Error: {str(e)}"}), 500

    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
