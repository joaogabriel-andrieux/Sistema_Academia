from app.models.models import db, Equipamento
from app.controllers.base_controller import BaseResource


class EquipamentoResource(BaseResource):
    """
    Resource para gerenciar Equipamentos da academia.
    Herda de BaseResource e cobre as regras de negócio associadas.
    """

    modelo = Equipamento
    nome_entidade = 'Equipamento'

    def _serializar(self, obj):
        """Converte um Equipamento para dicionário usando o encapsulamento do model."""
        return obj.to_dict()

    def _validar_e_criar(self, dados):
        """Valida os dados e cadastra um novo equipamento."""
        if not dados.get('nome'):
            return {'mensagem': 'O nome do equipamento é obrigatório'}, 400

        try:
            peso_maximo = float(dados.get('peso_maximo', 0.0))
        except (ValueError, TypeError):
            return {'mensagem': 'O peso máximo deve ser um valor numérico válido'}, 400

        # Regra de negócio (Requisito 1): Peso não pode ser negativo
        if peso_maximo < 0:
            return {'mensagem': 'O peso máximo do equipamento não pode ser negativo'}, 400

        status = dados.get('status', 'Ativo').strip()
        if status not in ['Ativo', 'Manutenção']:
            return {'mensagem': 'Status inválido! Escolha entre Ativo ou Manutenção'}, 400

        # Evita duplicar equipamentos com nomes idênticos da mesma marca
        marca = dados.get('marca', '').strip()
        if Equipamento.query.filter_by(nome=dados['nome'], marca=marca).first():
            return {'mensagem': 'Este equipamento desta marca já está cadastrado'}, 400

        # Construtor explícito do models.py
        equipamento = Equipamento(
            nome=dados['nome'].strip(),
            marca=marca,
            peso_maximo=peso_maximo,
            status=status
        )
        db.session.add(equipamento)
        db.session.commit()
        return {'mensagem': 'Equipamento cadastrado com sucesso!'}, 201

    def _atualizar(self, obj, dados):
        """Atualiza os dados de um equipamento."""
        try:
            if 'peso_maximo' in dados:
                peso = float(dados['peso_maximo'])
                if peso < 0:
                    return {'mensagem': 'O peso máximo não pode ser negativo'}, 400
                obj.peso_maximo = peso

            status = dados.get('status', obj.status)
            if status not in ['Ativo', 'Manutenção']:
                return {'mensagem': 'Status inválido! Escolha entre Ativo ou Manutenção'}, 400

            obj.nome = dados.get('nome', obj.nome).strip()
            obj.marca = dados.get('marca', obj.marca).strip()
            obj.status = status

            db.session.commit()
            return {'mensagem': 'Equipamento atualizado com sucesso!'}, 200

        except (ValueError, TypeError):
            return {'mensagem': 'O peso máximo deve ser um valor numérico válido'}, 400
        except Exception as e:
            db.session.rollback()
            return {'mensagem': 'Erro ao atualizar equipamento', 'erro': str(e)}, 500

    def delete(self, id):
        """Impede a exclusão do equipamento se ele estiver vinculado a algum exercício."""
        obj, erro = self._buscar_por_id(id)
        if erro:
            return erro
            
        # Regra de Integridade Referencial: Se houver exercícios usando este aparelho, bloqueia
        if obj.exercicios:
            return {
                'mensagem': f'Não é possível excluir o equipamento "{obj.nome}" porque ele está sendo utilizado em exercícios cadastrados!'
            }, 400
            
        db.session.delete(obj)
        db.session.commit()
        return {'mensagem': 'Equipamento excluído com sucesso!'}, 200