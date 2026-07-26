from app.models.models import db, Serie, Aluno, Exercicio
from app.controllers.base_controller import BaseResource

class SerieResource(BaseResource):
    """
    Resource para gerenciar as Séries (fichas de pesos e repetições dos alunos).
    """

    modelo = Serie
    nome_entidade = 'Serie'

    def _serializar(self, obj):
        """Serializa os dados da série para formato JSON."""
        return obj.to_dict()

    def _validar_e_criar(self, dados):
        """Valida as chaves estrangeiras e os limites numéricos da série."""
        try:
            aluno_id = int(dados.get('aluno_id', 0))
            exercicio_id = int(dados.get('exercicio_id', 0))
            quantidade_series = int(dados.get('quantidade_series', 0))
            repeticoes = int(dados.get('repeticoes', 0))
            carga_peso = float(dados.get('carga_peso', 0.0))
        except (ValueError, TypeError):
            return {'mensagem': 'Todos os campos de séries exigem valores numéricos válidos'}, 400

        # Validação de integridade: Aluno e Exercício precisam existir
        if not Aluno.query.get(aluno_id):
            return {'mensagem': f'Aluno com ID {aluno_id} não existe'}, 404
            
        if not Exercicio.query.get(exercicio_id):
            return {'mensagem': f'Exercício com ID {exercicio_id} não existe'}, 404

        # Regra de negócio: Carga, séries e repetições não podem ser zeradas ou negativas
        if quantidade_series <= 0 or repeticoes <= 0:
            return {'mensagem': 'Quantidade de séries e repetições devem ser maiores que zero'}, 400
        if carga_peso < 0:
            return {'mensagem': 'A carga de peso não pode ser um valor negativo'}, 400

        try:
            nova_serie = Serie(
                aluno_id=aluno_id,
                exercicio_id=exercicio_id,
                quantidade_series=quantidade_series,
                repeticoes=repeticoes,
                carga_peso=carga_peso
            )
            db.session.add(nova_serie)
            db.session.commit()
            return {'mensagem': 'Série adicionada com sucesso à ficha do aluno!'}, 201

        except Exception as e:
            db.session.rollback()
            return {'mensagem': 'Erro ao salvar série', 'erro': str(e)}, 500

    def _atualizar(self, obj, dados):
        """Atualiza os valores de carga ou repetições de uma série existente."""
        try:
            obj.quantidade_series = int(dados.get('quantidade_series', obj.quantidade_series))
            obj.repeticoes = int(dados.get('repeticoes', obj.repeticoes))
            obj.carga_peso = float(dados.get('carga_peso', obj.carga_peso))

            if obj.quantidade_series <= 0 or obj.repeticoes <= 0 or obj.carga_peso < 0:
                return {'mensagem': 'Valores numéricos inválidos para atualização'}, 400

            db.session.commit()
            return {'mensagem': 'Série de exercícios atualizada com sucesso!'}, 200

        except (ValueError, TypeError):
            return {'mensagem': 'Verifique se os dados informados são numéricos'}, 400
        except Exception as e:
            db.session.rollback()
            return {'mensagem': 'Erro ao atualizar série', 'erro': str(e)}, 500