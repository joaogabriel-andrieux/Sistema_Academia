from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# Instancia o db aqui, mas não o associa ao app ainda
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academia.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    api = Api(app)

    # Importa os modelos e recursos DENTRO do app_context para evitar o erro circular
    with app.app_context():
        from app.models.models import Aluno, Equipamento, Exercicio, Serie, Personal
        
        from app.controllers.aluno_controller import AlunoResource
        from app.controllers.equipamento_controller import EquipamentoResource
        from app.controllers.exercicio_controller import ExercicioResource
        from app.controllers.serie_controller import SerieResource
        from app.controllers.personal_controller import PersonalListResource, PersonalResource

        api.add_resource(AlunoResource, '/alunos', '/alunos/<int:id>')
        api.add_resource(EquipamentoResource, '/equipamentos', '/equipamentos/<int:id>')
        api.add_resource(ExercicioResource, '/exercicios', '/exercicios/<int:id>')
        api.add_resource(SerieResource, '/series', '/series/<int:id>')
        api.add_resource(PersonalListResource, '/personais')
        api.add_resource(PersonalResource, '/personais/<int:id>')

        db.create_all()

    return app