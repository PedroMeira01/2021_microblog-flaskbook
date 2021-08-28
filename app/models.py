from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Model de usuário
# A model determina a estrutura da tabela que é gerada
#  pela Migration e salva no arquivo SQLite "app.db"
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Este é um dunder method do Python para exibir a forma de retorno de um objeto
    def __repr__(self):
        return f'<User {self.username}>'
    # O método abaixo encriptografa a senha do usuário
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # O método abaixo compara uma senha criptografada com uma senha no formato String
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Model de Posts
# A model determina a estrutura da tabela que é gerada
#  pela Migration e salva no arquivo SQLite "app.db"
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.body}>'