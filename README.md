# <img src="https://avatars1.githubusercontent.com/u/7063040?v=4&s=200.jpg" alt="HU" width="24" /> Desafio Bravo

# Api de conversão de moedas

## Pré-requisitos
- Docker: https://docs.docker.com/install/

## Instruções para configuração/instalação
A aplicação roda dentro de uma imagem docker, portanto todo o ambiente é instalado diretamente através da mesma.

### Configuração
A configuração do sistema é baseada nos valores do arquivo de configurações <root>/config/bravo.yaml

| Chave | Descrição |
| -------- | -------- |
| postgres | configurações do banco postgres da aplicação |
| -------- | -------- |
| database | banco utilizado pela aplicação |
| user | usuário de acesso ao banco |
| password | senha do usuário para acesso ao banco |
| host | hostname do servidor do banco |
| port | porta de acesso ao banco |
| -------- | -------- |
| cron | configurações da tarefa que executa em segundo plano atualizado as cotações |
| -------- | -------- |
| update_frequency | frequencia de atualização das cotações das moedas |
| -------- | -------- |
| redis | configurações do cache com as cotações da moedas |
| -------- | -------- |
| host | hostname do servidor do cache |
| port | porta de acesso do cache |

Além disso o redis tem um arquivo de configuração que se encontra no path <root>/config/redis.conf (não foi alterado, está utilizando as configurações default do redis)

### Instalação
Os comandos a seguir criam e rodam a aplicação dentro de uma rede docker. Dentro da pasta raiz do repositório:
  - `docker-compose build --no-cache` - Cria imagem chamada flima/bravo-ch:0.1 durante build os testes unitários são executados.
  - `docker-compose up -d` - Executa imagem em daemon (e cria se o passo anterior não tiver sido executado previamente). Dentro do arquivo <root>/docker-compose.yml estão as configurações de portas que o sistema irá utilizar por default a aplicação irá utilizar a porta 5678.

### Execução dos testes
#### Unitarios: 
 - Depois de construida a imagem docker: `docker run -it --entrypoint "python" flima/bravo-ch:0.1 -m pytest` (isso irá gerar mais uma instancia dessa imagem)
 - Com a instancia default: `docker exec challenge-bravo_app_1 python -m pytest`
 - Ou de dentro do docker da aplicação: no pwd `/app/`, executar `python3 -m pytest`
 #### Load
- Também realizei alguns teste de estresse utilizando o software k6, executar de preferência de fora do docker ou wsl já que haverá concorrência: `k6 run test_script.js` (de dentro do windows obtive entre 1100 e 2100 req/s dependendo dos recursos disponíveis, já no wsl obtive algo em torno de 500 req/s)

stage 1 - 2 segs de ramp-up até 3300 vus

stage 2 - 1 min em 3300 vus

stage 3 - 2 segs de ramp-down

    | checks                     | 100 00% ✓ 71717  ✗ 0 |
    | data_received              | 11 MB   173 kB/s |
    | data_sent                  | 8 7 MB  134 kB/s |
    | http_req_blocked           | avg=5 71µs  min=0s      med=0s   max=7.99ms  p(90)=0s   p(95)=0s |
    | http_req_connecting        | avg=2.14µs  min=0s      med=0s   max=3.99ms  p(90)=0s   p(95)=0s |
    | http_req_duration          | avg=2.79s   min=17.75ms med=2.7s max=18.67s  p(90)=3.5s p(95)=4.14s |
    | http_req_receiving         | avg=66.69µs min=0s      med=0s   max=40.99ms p(90)=0s   p(95)=986.41µs |
    | http_req_sending           | avg=7.81µs  min=0s      med=0s   max=11.99ms p(90)=0s   p(95)=0s |
    | http_req_tls_handshaking   | avg=0s      min=0s      med=0s   max=0s      p(90)=0s   p(95)=0s |
    | http_req_waiting           | avg=2.79s   min=17.75ms med=2.7s max=18.67s  p(90)=3.5s p(95)=4.14s |
    | http_reqs                  | 71717   1110.963002/s |
    | iteration_duration         | avg=2.89s   min=120ms   med=2.8s max=18.77s  p(90)=3.6s p(95)=4.24s |
    | iterations                 | 71717   1110.963002/s |
    | vus                        | 1623    min=1623 max=3300 |
    | vus_max                    | 3300    min=3300 max=3300 |


## Documentação do endpoint de conversão

### Endpoint de consulta de moedas cadastradas:

`GET http://localhost:5678/currency`

Retorna todas as moedas cadastradas com suas cotações e momento de ultima atualização

### Endpoint da chamada de conversão:

`GET http://localhost:5678/currency/convert`

Parâmetros:
- from: (string) 3 caracteres com código de moeda cadastrada
- to: (string) 3 caracteres com código de moeda cadastrada
- amount: (string) decimal positivo com separador decimal `.`

todos os campos são obrigatórios.


Ex.: `http://localhost:5678/currency/convert?from=BTC&to=EUR&amount=123.45`

 - Caso algum campo ou formato não venha como desejado ou uma moeda não cadastrada seja requisitada haverá retorno de um Bad Request 

Essa api utiliza um cache dos valores das moedas. e a aplicação leva `update_frequency` (valor configurável) para atualizar os valores das moedas em uma api externa. Logo os valores das moedas não são exatamente os valores atuais, podendo ter atrasos de `update_frequency` segundos em seu valor 

### Endpoint da registro de conversão:

`PUT http://localhost:5678/currency:code`

 - Caso `code` não estiver na lista de possíveis moedas ou for vazio, haverá retorno de um Bad Request 
 - Caso `code` já cadastrado, haverá retorno de um OK 
 - Caso `code` não cadastrado, haverá retorno de um OK e adição da moeda

 [Moedas disponiveis na API](/docs/currencies.md)

### Endpoint da desregistro de conversão:

`DEL http://localhost:5678/currency:code`

 - Caso `code` já cadastrado, haverá retorno de um OK e remoção da moeda.
 - Caso `code` não cadastrado, haverá retorno de um Bad Request 

## Escolhas técnicas
### Framework
Foi utilizado o aiohttp para criação de um micro servidor asincrono. Biblioteca com ótima documentação e comunidade ativa.
### Deploy Method
Docker foi utilizado para simplicidade de criação e execução de um ambiente isolado e replicável.
### Integração para conversão de moedas
Foi utilizada a api CoinBase (https://api.coinbase.com/v2/exchange-rates). Escolha baseada em:
 - variedade de moedas e acessos ilimitados a api sem necessidade de subscription ou pagamentos.
 - certificado SSL OK (2021-01-28)
 - acesso a todas as conversões basedas em um lastro.
 - documentação disponivel

### Lib de testes
Para execuçao dos testes no formato unittest, foi utilizado o pytest biblioteca com ótima documentação e comunidade ativa.

## Links
- https://docs.docker.com
- https://docs.aiohttp.org/en/stable/index.html
- https://docs.pytest.org/en/stable/
- https://developers.coinbase.com/api/v2


## TODO:
 - utilizar alguma biblioteca para criação automatica da documentação.
 - criar uma validação para os códigos da moedas. Essas estão sendo validadas pela api externa.
 - criar um dockerfile com diferentes targets (retirando os arquivos de teste do ambiente produtivo)
 - healthcheck endpoint
 
