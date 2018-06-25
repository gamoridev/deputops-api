# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

# Retorna todos os deputados existentes da API da Câmara
class Deputados(Resource):
    deputados = []
    def get(self):
        # Retorna os dados recursivamente a partir da página 1
        # Se existirem outras páginas ele irá percorrir e adicionar à lista 'deputados'
        self.paging('https://dadosabertos.camara.leg.br/api/v2/deputados?pagina=1&itens=30&ordem=ASC&ordenarPor=nome')
        return self.deputados
    
    # Função recursiva para percorrer todas as páginas dos resultados dos deputados
    def paging(self, url):
        data = requests.get(url)
        for d in data.json()['dados']:
            # Filtro e limpeza dos dados da API
            self.deputados.append({
                'id': d['id'],
                'nome': d['nome'], 
                'foto': d['urlFoto']})
        for l in data.json()['links']:
            # Verifica se há a existência de páginas seguintes
            if 'next' == l['rel']:
                return self.paging(l['href'])

# Definição do endpoint para requisição de todos os deputados
api.add_resource(Deputados, '/deputados')

# Retorna detalhes de deputado específico com os dados da API da Câmara
class Detalhes(Resource):
    def get(self, _id):
        detalhes = []
        data = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados?id='+_id)
        
        try: 
            detalhes.append({
                'id': data.json()['dados'][0]['id'],
                'nome': data.json()['dados'][0]['nome'], 
                'partido': data.json()['dados'][0]['siglaPartido'], 
                'uf': data.json()['dados'][0]['siglaUf'], 
                'foto': data.json()['dados'][0]['urlFoto']})
        except:
            return 'Parametros incorretos ou ID inexistente.'
        return detalhes

# Endpoint para detalhes de deputado em script, recebendo o id do deputado como parâmetro
api.add_resource(Detalhes, '/deputados/detalhes/<string:_id>')

if __name__ == '__main__':
    app.run(debug=True)