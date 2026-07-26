from flask_restful import Resource, reqparse # type: ignore
from app.models.models import db, Personal

# Configuração dos argumentos que a API espera receber no POST
parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, required=True, help="O campo 'nome' é obrigatório.")
parser.add_argument('cpf', type=str, required=True, help="O campo 'cpf' é obrigatório.")
parser.add_argument('telefone', type=str, required=False)
parser.add_argument('usuario', type=str, required=True, help="O campo 'usuario' é obrigatório.")
parser.add_argument('senha', type=str, required=True, help="O campo 'senha' é obrigatório.")

class PersonalListResource(Resource):
    def get(self):
        # Busca todos os personais cadastrados
        personais = Personal.query.all()
        return [personal.to_dict() for personal in personais], 200

    def post(self):
        # Pega os dados enviados pela interface/Insomnia
        args = parser.parse_args()
        
        # Verifica se o CPF ou Usuário já existem para não duplicar
        if Personal.query.filter_by(cpf=args['cpf']).first():
            return {"message": "Já existe um Personal cadastrado com este CPF."}, 400
        if Personal.query.filter_by(usuario=args['usuario']).first():
            return {"message": "Este nome de usuário já está em uso."}, 400

        # Cria a nova instância do modelo
        novo_personal = Personal(
            nome=args['nome'],
            cpf=args['cpf'],
            telefone=args.get('telefone'),
            usuario=args['usuario'],
            senha=args['senha'] # Em produção usaríamos hash aqui, mas para o escopo atual está ótimo!
        )
        
        # Salva fisicamente no banco de dados SQLite
        db.session.add(novo_personal)
        db.session.commit()
        
        return novo_personal.to_dict(), 201

class PersonalResource(Resource):
    def delete(self, id):
        personal = Personal.query.get(id)
        if not personal:
            return {"message": "Personal não encontrado."}, 404
        
        db.session.delete(personal)
        db.session.commit()
        return {"message": f"Personal {id} deletado com sucesso."}, 200