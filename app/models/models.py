from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'matricula': self.matricula}


class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False, default='')
    peso_maximo = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), nullable=False, default='Ativo')
    exercicios = db.relationship('Exercicio', backref='equipamento', lazy=True)

    def to_dict(self):
        return {
            'id': self.id, 'nome': self.nome, 'marca': self.marca,
            'peso_maximo': self.peso_maximo, 'status': self.status
        }


class Exercicio(db.Model):
    __tablename__ = 'exercicios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    grupo_muscular = db.Column(db.String(100), nullable=False)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id, 'nome': self.nome,
            'grupo_muscular': self.grupo_muscular, 'equipamento_id': self.equipamento_id
        }


class Serie(db.Model):
    __tablename__ = 'series'
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    exercicio_id = db.Column(db.Integer, db.ForeignKey('exercicios.id'), nullable=False)
    quantidade_series = db.Column(db.Integer, nullable=False)
    repeticoes = db.Column(db.Integer, nullable=False)
    carga_peso = db.Column(db.Float, nullable=False, default=0.0)

    def to_dict(self):
        return {
            'id': self.id, 'aluno_id': self.aluno_id, 'exercicio_id': self.exercicio_id,
            'quantidade_series': self.quantidade_series, 'repeticoes': self.repeticoes,
            'carga_peso': self.carga_peso
        }


class Personal(db.Model):
    __tablename__ = 'personais'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id, 'nome': self.nome, 'cpf': self.cpf,
            'telefone': self.telefone, 'usuario': self.usuario, 'senha': self.senha
        }