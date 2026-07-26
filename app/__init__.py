from flask import Flask # type: ignore
from flask_restful import Api # type: ignore
from app.models.models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academia.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api = Api(app)

    # 1. Importando os novos recursos configurados nos controllers (Adicionado o Personal)
    from app.controllers.aluno_controller import AlunoResource
    from app.controllers.equipamento_controller import EquipamentoResource
    from app.controllers.exercicio_controller import ExercicioResource
    from app.controllers.serie_controller import SerieResource
    from app.controllers.personal_controller import PersonalListResource, PersonalResource

    # 2. Registrando as rotas com suporte a ID para operações de PUT/DELETE
    api.add_resource(AlunoResource, '/alunos', '/alunos/<int:id>')
    api.add_resource(EquipamentoResource, '/equipamentos', '/equipamentos/<int:id>')
    api.add_resource(ExercicioResource, '/exercicios', '/exercicios/<int:id>')
    api.add_resource(SerieResource, '/series', '/series/<int:id>')
    api.add_resource(PersonalListResource, '/personais')
    api.add_resource(PersonalResource, '/personais/<int:id>')

    with app.app_context():
        db.create_all()  # Garante a criação das tabelas corretas no banco SQLite (incluindo os personais)

    return app