**Português (BR)** | [English (US)](/docs/CONTRIBUTING-en-US.md)

# Contribuindo
O Querido Diário possui um [Guia para Contribuição](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/guia-de-contribuicao.html#contribuindo) principal que é relevante para todos os seus repositórios. Este guia traz informações gerais sobre como interagir com o projeto, o código de conduta que você adere ao contribuir, a lista de repositórios do ecossistema e as primeiras ações que você pode tomar. Recomendamos sua leitura antes de continuar.

Já leu? Então vamos às informações específicas deste repositório:
- [Arquitetura](#arquitetura)
- [Como configurar o ambiente de desenvolvimento](#como-configurar-o-ambiente-de-desenvolvimento)
    - [Em Linux](#em-linux)
- [Mantendo](#mantendo)

## Arquitetura

![arquitetura](/docs/images/arquitetura.png)

Uma breve descrição dos componentes do repositório:

| **Tipo**  | **Nome**                                          | **Descrição**                                                                               | **Dependências**    |
|-----------|---------------------------------------------------|---------------------------------------------------------------------------------------------|---------------------|
| Módulo    | [`config`](/app/config)                           | Configurações do Django e Celery.                                                           |                     |
| Módulo    | [`libs`](/app/libs)                               | Contratos e implementações de APIs externas.                                                |                     |
| Serviço   | [`libs/ibge`](/app/libs/ibge)                     | Consultas à API de cidades do IBGE.                                                         |                     |
| Serviço   | [`libs/querido_diario`](/app/libs/querido_diario) | Consultas à API aberta do Querido Diário.                                                   |                     |
| Aplicação | [`accounts`](/app/accounts)                       | Gerenciamento de informações básicas e de autenticação de usuários.                         |                     |
| Aplicação | [`querido_diario`](/app/querido_diario)           | API intermediária de consultas ao Querido Diário.                                           |                     |
| Aplicação | [`alerts`](/app/alerts)                           | Gerenciamento de alertas de busca.                                                          | accounts, libs/ibge |
| Recurso   | Postgres                                          | Banco de dados principal. Contém informações básicas de usuários e alertas.                 |                     |
| Recurso   | Redis                                             | Banco de dados utilizado para processamento de tarefas assíncronas como o envio de alertas. |


## Como configurar o ambiente de desenvolvimento

O projeto utiliza [Django](https://www.djangoproject.com/), [Django REST frawework](https://www.django-rest-framework.org/), [Celery](https://github.com/celery/celery), [Redis](https://redis.io/) e [Postgres](https://www.postgresql.org/). Para saber as versões do Django, DRF e Celery, verifique o [`requirements.txt`](app/requirements.txt). As versões dos bancos de dados são as mais recentes disponíveis.

A seguir, veja como instalar todas essas ferramentas em seu sistema operacional.

1. [Instale o podman](https://podman.io/getting-started/installation.html) e verifique a versão do Python (3.6+)

2. Com o Python e podman instalados, ative o ambiente virtual:

```console
python3 -m venv .venv
source .venv/bin/activate
```
_Observação_: Em Windows, o segundo comando deve ser substituído por `.venv/Scripts/activate.bat` o sentido da barra (`/` ou `\`) pode variar a depender da utilização de [WSL](https://learn.microsoft.com/pt-br/windows/wsl/about)).

3. Instale as dependências de desenvolvimento para poder interagir com a interface de linha de comando disponível em `cli`:

```console
pip install -r requirements-dev.txt
```

4. Agora, para fazer o setup do projeto (instalar `pre-commit`, criar variáveis de ambiente e containers), execute:

```console
python -m cli setup
```

Para mais informações sobre a interface de linha de comando, execute:

```console
python -m cli --help
```

5. Pronto! Agora você já pode começar a editar o código.

# Mantendo
As pessoas mantenedoras devem seguir as diretrizes do [Guia para Mantenedoras](https://docs.queridodiario.ok.org.br/pt-br/latest/contribuindo/guia-de-contribuicao.html#mantendo) do Querido Diário.
