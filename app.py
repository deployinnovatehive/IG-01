from flask import Flask
from AdminSide.app import admin_bp
from UserSide.UserSide.app import user_bp

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-innovate-guide'

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)