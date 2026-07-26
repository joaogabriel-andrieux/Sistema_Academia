from flask import request
from flask_restful import Resource
from app.models.models import db


class BaseResource(Resource):
    """
    Classe base para todos os recursos da API.
    Define comportamento padrão para get, post, put e delete.
    As subclasses devem sobrescrever os métodos para implementar
    comportamento específico (polimorfismo).
    """

    # Atributos que as subclasses devem definir
    modelo = None          # Ex: Aluno, Plano...
    nome_entidade = None   # Ex: 'Aluno', 'Plano'...

    def _buscar_por_id(self, id):
        """Busca um registro pelo ID e retorna 404 se não encontrado."""
        obj = self.modelo.query.get(id)
        if not obj:
            return None, ({'mensagem': f'{self.nome_entidade} não encontrado(a)'}, 404)
        return obj, None

    def _serializar(self, obj):
        """
        Serializa um objeto para dicionário.
        Deve ser sobrescrito pelas subclasses (polimorfismo).
        """
        raise NotImplementedError

    def _validar_e_criar(self, dados):
        """
        Valida os dados e cria um novo objeto.
        Deve ser sobrescrito pelas subclasses (polimorfismo).
        """
        raise NotImplementedError

    def _atualizar(self, obj, dados):
        """
        Atualiza os campos de um objeto existente.
        Deve ser sobrescrito pelas subclasses (polimorfismo).
        """
        raise NotImplementedError

    def get(self, id=None):
        """Retorna um registro por ID ou lista todos."""
        if id:
            obj, erro = self._buscar_por_id(id)
            if erro:
                return erro
            return self._serializar(obj)
        registros = self.modelo.query.all()
        return [self._serializar(r) for r in registros]

    def post(self):
        """Cria um novo registro."""
        dados = request.get_json()
        return self._validar_e_criar(dados)

    def put(self, id):
        """Atualiza um registro existente."""
        obj, erro = self._buscar_por_id(id)
        if erro:
            return erro
        dados = request.get_json()
        return self._atualizar(obj, dados)

    def delete(self, id):
        """Remove um registro pelo ID."""
        obj, erro = self._buscar_por_id(id)
        if erro:
            return erro
        db.session.delete(obj)
        db.session.commit()
        return {'mensagem': f'{self.nome_entidade} excluído(a) com sucesso!'}
