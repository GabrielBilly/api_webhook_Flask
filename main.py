import os
import requests
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '5320382698234bf2f27af1ab4f35ae47c31b2953eb016c67'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'criar_conta'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/", methods=['GET', 'POST'])
def criar_conta():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        token = request.form.get('token')

        if not email or not password or not confirm_password or not token:
            flash('Todos os campos devem ser preenchidos', 'error')
            return redirect(url_for('criar_conta'))

        if password != confirm_password:
            flash('A senha e a confirmação de senha devem ser iguais', 'error')
            return redirect(url_for('criar_conta'))

        if token != 'uhdfaAADF123':
            flash('Token inválido', 'error')
            return redirect(url_for('criar_conta'))

        if User.query.filter_by(email=email).first():
            flash('Este email já está registrado', 'error')
            return redirect(url_for('criar_conta'))

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash('Conta criada com sucesso', 'success')
        return redirect(url_for('pagina_protegida'))

    if current_user.is_authenticated:
        return redirect(url_for('pagina_protegida'))

    return render_template('criar_conta.html')


@app.route("/login", methods=['POST'])
def fazer_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        flash('E-mail ou senha inválidos', 'error')
        return redirect(url_for('criar_conta'))

    login_user(user)
    return redirect(url_for('pagina_protegida'))


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Você fez logout com sucesso', 'success')
    return redirect(url_for('criar_conta'))


class Webhook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(120), nullable=False)
    parcelas = db.Column(db.Integer, nullable=False)
    acao = db.Column(db.String(120), nullable=True)


@app.route("/webhook", methods=['POST'])
def receber_webhook():
    webhook_data = request.get_json(force=True)

    if not webhook_data:
        return jsonify({'error': 'Dados não encontrados'}), 400

    nome = webhook_data.get('nome')
    email = webhook_data.get('email')
    status = webhook_data.get('status')
    valor = webhook_data.get('valor')
    forma_pagamento = webhook_data.get('forma_pagamento')
    parcelas = webhook_data.get('parcelas')

    if not all([nome, email, status, valor, forma_pagamento, parcelas]):
        return jsonify({'error': 'Dados incompletos'}), 400

    webhook = Webhook(
        nome=nome,
        email=email,
        status=status,
        valor=valor,
        forma_pagamento=forma_pagamento,
        parcelas=parcelas
    )

    # Realizar tratamento com base no campo 'status'
    if status == 'aprovado':
        webhook.acao = f'Liberar acesso de {email}'
    elif status == 'recusado':
        webhook.acao = 'Pagamento recusado'
    elif status == 'reembolsado':
        webhook.acao = 'Acesso recusado'

    db.session.add(webhook)
    db.session.commit()

    return jsonify({'message': 'Webhook recebido com sucesso'})


@app.route("/pagina_protegida", methods=['GET'])
@login_required
def pagina_protegida():
    webhooks = Webhook.query.all()

    return render_template("tratativas.html", webhooks=webhooks)


if __name__ == "__main__":
    app.run(debug=True)
