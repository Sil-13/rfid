from app import db
from datetime import datetime

class Bem(db.Model):
    __tablename__ = 'bens'
    id_bem = db.Column(db.Integer, primary_key=True)
    tag_rfid = db.Column(db.String(255), unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    numero_serie = db.Column(db.String(255), unique=True)
    id_ambiente_atual = db.Column(db.Integer, db.ForeignKey('ambientes.id_ambiente'))
    data_aquisicao = db.Column(db.Date)
    valor_aquisicao = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50), default='Disponível')
    ambiente_atual = db.relationship('Ambiente', backref='bens_no_ambiente') 

    def __repr__(self):
        return f'<Bem {self.nome} ({self.tag_rfid})>'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    tag_rfid = db.Column(db.String(255), unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.String(50), nullable=False)
    matricula_ou_registro = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    telefone = db.Column(db.String(20))

    def __repr__(self):
        return f'<Usuario {self.nome} ({self.tag_rfid})>'

class Ambiente(db.Model):
    __tablename__ = 'ambientes'
    id_ambiente = db.Column(db.Integer, primary_key=True)
    nome_ambiente = db.Column(db.String(255), unique=True, nullable=False)
    localizacao = db.Column(db.String(255))
    tag_rfid_ativo = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<Ambiente {self.nome_ambiente}>'

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    id_movimentacao = db.Column(db.Integer, primary_key=True)
    tag_rfid_item = db.Column(db.String(255), nullable=False)
    tipo_item = db.Column(db.Enum('bem', 'usuario'), nullable=False)
    id_ambiente_leitor = db.Column(db.Integer, db.ForeignKey('ambientes.id_ambiente'))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo_movimentacao = db.Column(db.Enum('entrada', 'saida'), nullable=False)
    ambiente_leitor = db.relationship('Ambiente', backref='movimentacoes_por_ambiente') 

    def __repr__(self):
        return f'<Movimentacao {self.tag_rfid_item} em {self.data_hora}>'
