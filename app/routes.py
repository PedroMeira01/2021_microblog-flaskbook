from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

# Os decorators abaixo significam que ambas as rotas irão retornar o método definido
@app.route('/')
@app.route('/index')
# O decorator abaixo serve para indicar que a rota é protegida por autenticação
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    # Exemplo de retorno de templates e de dados para o template
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verifica se o usuário está logado através da variável
    # "current_user" que é automáticamente setada pelo package Flask Login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Recebe a instância da classe de login criada com o package Flask Forms
    form = LoginForm()
    # O método abaixo verifica se a validação do Flask Form obteve sucesso
    if form.validate_on_submit():
        # Consulta a tabela 'user' onde o campo 'username' seja igual ao recebido pelo form
        user = User.query.filter_by(username=form.username.data).first()
        # Valida se há um usuário no banco com o username digitado
        # E se a senha digitada bate com criptografia da senha guardada no banco
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Através deste método do pkg Flask Form o usuário é logado
        login_user(user, remember=form.remember_me.data)
        # O next_page é um parâmetro que é retornado da proteção do
        #  Flask Login a rotas restritas a usuários logados
        next_page = request.args.get('next')
        # Verifica se houve a tentativa de acesso a uma página restrita
        if not next_page or url_parse(next_page).net_loc != '':
            next_page = url_for('index')
        
        return redirect(next_page)
    # Se não passar na validação do Flask Form, redireciona para o login
    return render_template('login.html', title='Sign In', form=form)

# Método de logout
@app.route('/logout')
def logout():
    # A função abaixo é uma função pronta do Flask Login
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations! You are now a registered user!')
        
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)