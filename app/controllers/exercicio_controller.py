from app.models.models import db, Exercicio, Equipamento
from app.controllers.base_controller import BaseResource

class ExercicioResource(BaseResource):
    """
    Resource para gerenciar os Exercícios da academia.
    Cada exercício depende de um equipamento cadastrado.
    """

    modelo = Exercicio
    nome_entidade = 'Exercicio'

    def _serializar(self, obj):
        """Retorna o dicionário do exercício usando o encapsulamento do model."""
        return obj.to_dict()

    def _validar_e_criar(self, dados):
        """Valida e cria um novo exercício vinculado a um equipamento."""
        nome = dados.get('nome', '').strip()
        grupo_muscular = dados.get('grupo_muscular', '').strip()
        equipamento_id = dados.get('equipamento_id')

        if not nome or not grupo_muscular or not equipamento_id:
            return {'mensagem': 'Nome, grupo muscular e ID do equipamento são obrigatórios'}, 400

        try:
            equipamento_id = int(equipamento_id)
        except (ValueError, TypeError):
            return {'mensagem': 'O ID do equipamento deve ser um número inteiro válido'}, 400

        # Regra de negócio: O equipamento precisa existir no banco de dados
        equipamento = Equipamento.query.get(equipamento_id)
        if not equipamento:
            return {'mensagem': f'Equipamento com ID {equipamento_id} não foi encontrado'}, 404

        # Regra de negócio extra: Não faz sentido usar um equipamento em manutenção
        if equipamento.status == 'Manutenção':
            return {'mensagem': f'O equipamento "{equipamento.nome}" está em manutenção e não pode receber novos exercícios'}, 400

        # Evita duplicar o mesmo exercício para o mesmo grupo muscular
        if Exercicio.query.filter_by(nome=nome, grupo_muscular=grupo_muscular).first():
            return {'mensagem': 'Este exercício já está cadastrado para este grupo muscular'}, 400

        try:
            exercicio = Exercicio(
                nome=nome,
                grupo_muscular=grupo_muscular,
                equipamento_id=equipamento_id
            )
            db.session.add(exercicio)
            db.session.commit()
            return {'mensagem': 'Exercício cadastrado com sucesso!'}, 201
            
        except Exception as e:
            db.session.rollback()
            return {'mensagem': 'Erro ao cadastrar exercício', 'erro': str(e)}, 500

    def _atualizar(self, obj, dados):
        """Atualiza os dados de um exercício cadastrado."""
        try:
            if 'equipamento_id' in dados:
                eq_id = int(dados['equipamento_id'])
                equipamento = Equipamento.query.get(eq_id)
                if not equipamento:
                    return {'mensagem': 'Equipamento informado não existe'}, 404
                obj.equipamento_id = eq_id

            obj.nome = dados.get('nome', obj.nome).strip()
            obj.grupo_muscular = dados.get('grupo_muscular', obj.grupo_muscular).strip()

            db.session.commit()
            return {'mensagem': 'Exercício atualizado com sucesso!'}, 200

        except (ValueError, TypeError):
            return {'mensagem': 'O ID do equipamento deve ser um número inteiro'}, 400
        except Exception as e:
            db.session.rollback()
            return {'mensagem': 'Erro ao atualizar exercício', 'erro': str(e)}, 500