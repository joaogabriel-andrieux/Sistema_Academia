from flask_restful import Resource # type: ignore
from app.models.models import db, Aluno
from app.controllers.base_controller import BaseResource

class AlunoResource(BaseResource):
    """
    Resource responsável por gerenciar alunos no novo escopo da academia.
    """

    modelo = Aluno
    nome_entidade = 'Aluno'

    def _serializar(self, obj):
        """Converte objeto Aluno para dicionário (Encapsulamento)."""
        return {
            'id': obj.id,
            'nome': obj.nome,
            'matricula': obj.matricula
        }

    def _validar_e_criar(self, dados):
        """Valida os dados e cria um novo aluno."""

        campos_obrigatorios = ['nome', 'matricula']

        # Verifica campos obrigatórios
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return {
                    'mensagem': f'O campo {campo} é obrigatório'
                }, 400

        nome = dados['nome'].strip()
        matricula = dados['matricula'].strip()

        # --- REQUISITOS DE VALIDAÇÃO ---
        if len(nome) < 3:
            return {
                'mensagem': 'O nome do aluno deve conter pelo menos 3 caracteres'
            }, 400

        # Verifica matrícula duplicada
        if Aluno.query.filter_by(matricula=matricula).first():
            return {
                'mensagem': 'Esta matrícula já está cadastrada no sistema'
            }, 400
        # -------------------------------

        try:
            aluno = Aluno(
                nome=nome,
                matricula=matricula
            )

            db.session.add(aluno)
            db.session.commit()

            return {
                'mensagem': 'Aluno cadastrado com sucesso!'
            }, 201

        except Exception as e:
            db.session.rollback()
            return {
                'mensagem': 'Erro ao cadastrar aluno',
                'erro': str(e)
            }, 500

    def _atualizar(self, obj, dados):
        """Atualiza os dados de um aluno."""

        try:
            novo_nome = dados.get('nome', obj.nome).strip()
            nova_matricula = dados.get('matricula', obj.matricula).strip()

            if len(novo_nome) < 3:
                return {
                    'mensagem': 'O nome do aluno deve conter pelo menos 3 caracteres'
                }, 400

            # Se estiver tentando mudar a matrícula, checa se a nova já existe em outro aluno
            if nova_matricula != obj.matricula:
                if Aluno.query.filter_by(matricula=nova_matricula).first():
                    return {
                        'mensagem': 'Esta matrícula já pertence a outro aluno'
                    }, 400

            obj.nome = novo_nome
            obj.matricula = nova_matricula

            db.session.commit()

            return {
                'mensagem': 'Aluno atualizado com sucesso!'
            }, 200

        except Exception as e:
            db.session.rollback()
            return {
                'mensagem': 'Erro ao atualizar aluno',
                'erro': str(e)
            }, 500