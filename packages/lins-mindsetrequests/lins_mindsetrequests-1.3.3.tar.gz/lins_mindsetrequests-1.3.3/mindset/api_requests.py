from os import environ
from .utils.request_base import mindset_request
from .utils.date_utils import make_aware
from datetime import datetime


class Servico:

    def __init__(self, nome_servico):
        self.nome_servico = nome_servico
        self.id = self.get_id()
        self.service_params = {
            'servico': self.nome_servico,
            'hora_agendamento': '01:00',
            'forcar_execucao': True,
            'ativo': True,
            'tipo': 'entrada',
        }

    def get_or_create(self, service_params={}):
        response = mindset_request('GET', '/servicos', query_params={'servico': self.nome_servico})
        if not response.ok:
            return response, {}
        if not response.json():
            self.service_params.update(service_params)
            response = mindset_request('POST', '/servicos', json=self.service_params)
            self.id = self.get_id()
            return (response, response.json()) if response.ok else (response, {})
        return (response, response.json()[0])

    def ativo(self):
        response = mindset_request('GET', '/servicos', query_params={'servico': self.nome_servico})
        if response.ok and response.json():
            return response.json()[0]['ativo']

    @staticmethod
    def filtrar(filter_params={}):
        return mindset_request('GET', '/servicos', query_params=filter_params)

    def forcar_execucao(self):
        response = mindset_request('GET', '/servicos', query_params={'servico': self.nome_servico})
        if not response.ok:
            raise ConnectionError(f'Status code {response.status_code} em "{response.url}"')
        return response.json()[0]['forcar_execucao']

    def get_id(self):
        response = mindset_request('GET', '/servicos', query_params={'servico': self.nome_servico})
        if response.ok and response.json():
            return response.json()[0]['_id']

    def inicia_integracao(self):
        return mindset_request('POST', f'/servicos/{self.id}/inicia_integracao')

    def sucesso_integracao(self):
        return mindset_request('POST', f'/servicos/{self.id}/sucesso_integracao')

    def falha_integracao(self):
        return mindset_request('POST', f'/servicos/{self.id}/falha_integracao')

    def get_data_ultima_integracao(self, filter_params={}):
        query_params = {
            '_id_servico': self.id,
            'status': 'S',
            'fields': 'inicio_execucao',
            'sort': '-inicio_execucao',
            'per_page': 1,
        }
        query_params.update(filter_params)
        valor_padrao = {'inicio_execucao': environ.get('DATA_PADRAO_INTEGRACAO')}
        response = Status.get(query_params)
        data = response.json()[0] if response.ok and response.json() else valor_padrao
        data = make_aware(datetime.strptime(data.get('inicio_execucao'), '%Y-%m-%dT%H:%M:%S.%f'))
        return datetime.strftime(data, '%Y-%m-%dT%H:%M:%S')

    def delete(self):
        return mindset_request('DELETE', f'/servicos/{self.id}')

    def update(self, json):
        return mindset_request('PATCH', f'/servicos/{self.id}', json=json)

    def status(self):
        return mindset_request('GET', f'/servicos/{self.id}/status')

    def em_execucao(self):
        json = self.status().json()
        return False if not json else "E" == json[0].get('status', False)

    def executado(self):
        response = Controle.get({'servico': self.id})
        if response.ok and not response.json():
            return False
        if response.ok and response.json():
            return response.json()[0]['executado']

    def pode_integrar(self):
        response = self.status()
        if not response.json() and self.ativo():
            return True
        if self.em_execucao():
            return False
        if self.forcar_execucao():
            return True
        hoje, json = datetime.now(), response.json()[0]
        fim_execucao = {
            19: f'{json.get("fim_execucao")}.0'
        }.get(len(json.get('fim_execucao')), json.get('fim_execucao'))
        no_horario = hoje.time() >= datetime.strptime(
            json.get('hora_agendamento', '01:00:00'), '%H:%M:%S',
        ).time()
        executou_hoje = all([
            json.get('status') == 'S',
            fim_execucao,
            datetime.strptime(fim_execucao, '%Y-%m-%dT%H:%M:%S.%f').date() == hoje.date(),
        ])
        return all(
            [
                self.ativo(),
                not self.executado(),
                no_horario,
                not executou_hoje,
            ]
        )


class Controle:

    @staticmethod
    def get(filter_params={}):
        return mindset_request('GET', '/controle', query_params=filter_params)

    @staticmethod
    def limpar(json={}):
        return mindset_request('POST', '/controle/limpar_controles', json=json)


class Status:

    @staticmethod
    def get(filter_params={}):
        return mindset_request('GET', '/status', query_params=filter_params)

    @staticmethod
    def atuais():
        return mindset_request('GET', '/status/atual')
