# <img src="https://avatars1.githubusercontent.com/u/7063040?v=4&s=200.jpg" alt="HU" width="24" /> Desafio Bravo

# Api de conversão de moedas

## Pré-requisitos
- Docker: https://docs.docker.com/install/

## Instruções para configuração/instalação
A aplicação roda dentro de uma imagem docker, portanto todo o ambiente é instalado diretamente através da mesma.

### Configuração
A configuração do sistema é baseada nos valores do arquivo de configurações <root>/config/bravo.yaml

| Chave | Descrição |
| --- | --- |
| postgres | configurações do banco postgres da aplicação |
| --- | --- |
| database | banco utilizado pela aplicação |
| user | usuário de acesso ao banco |
| password | senha do usuário para acesso ao banco |
| host | hostname do servidor do banco |
| port | porta de acesso ao banco |
| --- | --- |
| cron | configurações da tarefa que executa em segundo plano atualizado as cotações |
| --- | --- |
| update_frequency | frequencia de atualização das cotações das moedas |

* O banco de dados e a tarefa são executados em dois dockers separados da aplicação principal. O banco necessita ser postgres mas a aplicação pode apontar para um outro banco já instanciado.
* No path <root>/migrations arquivos que povoam um novo banco.

### Instalação
Os comandos a seguir criam e rodam a aplicação dentro de uma rede docker. Dentro da pasta raiz do repositório:
  - `docker-compose build --no-cache` - Cria imagem chamada flima/bravo-ch:0.1 durante build os testes unitários são executados.
  - `docker-compose up -d` - Executa imagem em daemon (e cria se o passo anterior não tiver sido executado previamente). Dentro do arquivo <root>/docker-compose.yml estão as configurações de portas que o sistema irá utilizar por default a aplicação irá utilizar a porta 5678.

### Execução dos testes
- Dentro do docker da aplicação na pasta `/app/`, executar
`python3 -m pytest`
- Também realizei um teste de estresse utilizando o software k6, executar de preferência de fora do docker ou wsl já que haverá concorrência.
`k6 run test_script.js` (de dentro do windows obtive entre 1450 e 2100 req/s, já no wsl obtive algo em torno de 500 req/s)

stage 1 - 2 segs de ramp-up até 3300 vus

stage 2 - 1 min em 3300 vus

stage 3 - 2 segs de ramp-down

    | checks                    | 100.00% ✓ 120371 ✗ 0 |
    | data_received             | 20 MB   318 kB/s |
    | data_sent                 | 15 MB   226 kB/s |
    | http_req_blocked          | avg=5.74ms  min=0s       med=0s    max=1.31s    p(90)=0s    p(95)=0s |
    | http_req_connecting       | avg=5.55ms  min=0s       med=0s    max=1.19s    p(90)=0s    p(95)=0s |
    | http_req_duration         | avg=1.6s    min=3.99ms   med=1.48s max=18.84s   p(90)=2s    p(95)=2.41s |
    | http_req_receiving        | avg=58.08µs min=0s       med=0s    max=144.73ms p(90)=0s    p(95)=0s |
    | http_req_sending          | avg=89.44µs min=0s       med=0s    max=579.07ms p(90)=0s    p(95)=0s |
    | http_req_tls_handshaking  | avg=0s      min=0s       med=0s    max=0s       p(90)=0s    p(95)=0s |
    | http_req_waiting          | avg=1.6s    min=3.99ms   med=1.48s max=18.84s   p(90)=1.99s p(95)=2.41s |
    | http_reqs                 | 120371  1868.794252/s |
    | iteration_duration        | avg=1.71s   min=104.99ms med=1.58s max=20.11s   p(90)=2.12s p(95)=2.51s |
    | iterations                | 120371  1868.794252/s |
    | vus                       | 1214    min=1214 max=3300 |
    | vus_max                   | 3300    min=3300 max=3300 |

## Documentação do endpoint de conversão

### Endpoint de consulta de moedas cadastradas:

`GET http://localhost:5678/`

Retorna todas as moedas cadastradas com suas cotações e momento de ultima atualização

### Endpoint da chamada de conversão:

`GET http://localhost:5678/currency/convert`

Parâmetros:
- from: (string) 3-4 caracteres com código de moeda cadastrada
- to: (string) 3-4 caracteres com código de moeda cadastrada
- amount: (string) decimal positivo com separador decimal `.`

todos os campos são obrigatórios.


Ex.: `http://localhost:5678/currency/convert?from=BTC&to=EUR&amount=123.45`

 - Caso algum campo ou formato não venha como desejado ou uma moeda não cadastrada seja requisitada haverá retorno de um Bad Request 

Essa api utiliza um cache de 15 segundos dos valores das moedas. e a aplicação leva `update_frequency` (valor configurável) para atualizar os valores das moedas em uma api externa. Logo os valores das moedas não são exatamente os valores atuais, podendo ter atrasos de (`update_frequency`+15) segundos em seu valor 

### Endpoint da registro de conversão:

`PUT http://localhost:5678/currency:code`

- Caso `code` não estiver na lista de possíveis moedas ou for vazio, haverá retorno de um Bad Request 
 - Caso `code` já cadastrado, haverá retorno de um OK 
 - Caso `code` não cadastrado, haverá retorno de um OK e adição da moeda

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
 - certificado SSL OK
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
 - A aplicação realiza um cache para conseguir atingir as necessárias 1000 requisições por segundo. Esse cache ainda não é compartilhado impossibilitando a pulverizaçao das requests em varios possiveis dockers com a aplicação principal. Esse cache dura 15s e não é configuravel. é necessario utilizar um biblioteca como o REDIS (https://redis.io)
 - Subir a cobertura do código da aplicação.
 - utilizar alguma biblioteca para criação automatica da documentação.
 - criar uma validação para os códigos da moedas. Essas estão sendo validadas pela api externa.
 
## Moedas disponiveis na API

 - `AED`: United Arab Emirates Dirham

 - `AFN`: Afghan Afghani

 - `ALL`: Albanian Lek

 - `AMD`: Armenian Dram

 - `ANG`: Netherlands Antillean Gulden

 - `AOA`: Angolan Kwanza

 - `ARS`: Argentine Peso

 - `AUD`: Australian Dollar

 - `AWG`: Aruban Florin

 - `AZN`: Azerbaijani Manat

 - `BAM`: Bosnia and Herzegovina Convertible Mark

 - `BBD`: Barbadian Dollar

 - `BDT`: Bangladeshi Taka

 - `BGN`: Bulgarian Lev

 - `BHD`: Bahraini Dinar

 - `BIF`: Burundian Franc

 - `BMD`: Bermudian Dollar

 - `BND`: Brunei Dollar

 - `BOB`: Bolivian Boliviano

 - `BRL`: Brazilian Real

 - `BSD`: Bahamian Dollar

 - `BTN`: Bhutanese Ngultrum

 - `BWP`: Botswana Pula

 - `BYN`: Belarusian Ruble

 - `BYR`: Belarusian Ruble

 - `BZD`: Belize Dollar

 - `CAD`: Canadian Dollar

 - `CDF`: Congolese Franc

 - `CHF`: Swiss Franc

 - `CLF`: Unidad de Fomento

 - `CLP`: Chilean Peso

 - `CNH`: Chinese Renminbi Yuan Offshore

 - `CNY`: Chinese Renminbi Yuan

 - `COP`: Colombian Peso

 - `CRC`: Costa Rican Colón

 - `CUC`: Cuban Convertible Peso

 - `CVE`: Cape Verdean Escudo

 - `CZK`: Czech Koruna

 - `DJF`: Djiboutian Franc

 - `DKK`: Danish Krone

 - `DOP`: Dominican Peso

 - `DZD`: Algerian Dinar

 - `EEK`: Estonian Kroon

 - `EGP`: Egyptian Pound

 - `ERN`: Eritrean Nakfa

 - `ETB`: Ethiopian Birr

 - `EUR`: Euro

 - `FJD`: Fijian Dollar

 - `FKP`: Falkland Pound

 - `GBP`: British Pound

 - `GEL`: Georgian Lari

 - `GGP`: Guernsey Pound

 - `GHS`: Ghanaian Cedi

 - `GIP`: Gibraltar Pound

 - `GMD`: Gambian Dalasi

 - `GNF`: Guinean Franc
 
 - `GTQ`: Guatemalan Quetzal
 
 - `GYD`: Guyanese Dollar
 
 - `HKD`: Hong Kong Dollar
 
 - `HNL`: Honduran Lempira
 
 - `HRK`: Croatian Kuna
 
 - `HTG`: Haitian Gourde
 
 - `HUF`: Hungarian Forint
 
 - `IDR`: Indonesian Rupiah
 
 - `ILS`: Israeli New Sheqel
 
 - `IMP`: Isle of Man Pound
 
 - `INR`: Indian Rupee
 
 - `IQD`: Iraqi Dinar
 
 - `ISK`: Icelandic Króna
 
 - `JEP`: Jersey Pound
 
 - `JMD`: Jamaican Dollar
 
 - `JOD`: Jordanian Dinar
 
 - `JPY`: Japanese Yen
 
 - `KES`: Kenyan Shilling
 
 - `KGS`: Kyrgyzstani Som
 
 - `KHR`: Cambodian Riel
 
 - `KMF`: Comorian Franc
 
 - `KRW`: South Korean Won
 
 - `KWD`: Kuwaiti Dinar
 
 - `KYD`: Cayman Islands Dollar
 
 - `KZT`: Kazakhstani Tenge
 
 - `LAK`: Lao Kip
 
 - `LBP`: Lebanese Pound
 
 - `LKR`: Sri Lankan Rupee
 
 - `LRD`: Liberian Dollar
 
 - `LSL`: Lesotho Loti
 
 - `LTL`: Lithuanian Litas
 
 - `LVL`: Latvian Lats
 
 - `LYD`: Libyan Dinar
 
 - `MAD`: Moroccan Dirham
 
 - `MDL`: Moldovan Leu
 
 - `MGA`: Malagasy Ariary
 
 - `MKD`: Macedonian Denar
 
 - `MMK`: Myanmar Kyat
 
 - `MNT`: Mongolian Tögrög
 
 - `MOP`: Macanese Pataca
 
 - `MRO`: Mauritanian Ouguiya
 
 - `MTL`: Maltese Lira
 
 - `MUR`: Mauritian Rupee
 
 - `MVR`: Maldivian Rufiyaa
 
 - `MWK`: Malawian Kwacha
 
 - `MXN`: Mexican Peso
 
 - `MYR`: Malaysian Ringgit
 
 - `MZN`: Mozambican Metical
 
 - `NAD`: Namibian Dollar
 
 - `NGN`: Nigerian Naira
 
 - `NIO`: Nicaraguan Córdoba
 
 - `NOK`: Norwegian Krone
 
 - `NPR`: Nepalese Rupee
 
 - `NZD`: New Zealand Dollar
 
 - `OMR`: Omani Rial
 
 - `PAB`: Panamanian Balboa
 
 - `PEN`: Peruvian Sol
 
 - `PGK`: Papua New Guinean Kina
 
 - `PHP`: Philippine Peso
 
 - `PKR`: Pakistani Rupee
 
 - `PLN`: Polish Złoty
 
 - `PYG`: Paraguayan Guaraní
 
 - `QAR`: Qatari Riyal
 
 - `RON`: Romanian Leu
 
 - `RSD`: Serbian Dinar
 
 - `RUB`: Russian Ruble
 
 - `RWF`: Rwandan Franc
 
 - `SAR`: Saudi Riyal
 
 - `SBD`: Solomon Islands Dollar
 
 - `SCR`: Seychellois Rupee
 
 - `SEK`: Swedish Krona
 
 - `SGD`: Singapore Dollar
 
 - `SHP`: Saint Helenian Pound
 
 - `SLL`: Sierra Leonean Leone
 
 - `SOS`: Somali Shilling
 
 - `SRD`: Surinomese Dollar
 
 - `SSP`: South Sudanese Pound
 
 - `STD`: São Tomé and Príncipe Dobra
 
 - `SVC`: Salvadoran Colón
 
 - `SZL`: Swazi Lilangeni
 
 - `THB`: Thai Baht
 
 - `TJS`: Tajikistani Somoni
 
 - `TMT`: Turkmenistani Manat
 
 - `TND`: Tunisian Dinar
 
 - `TOP`: Tongan Paʻanga
 
 - `TRY`: Turkish Lira
 
 - `TTD`: Trinidad and Tobago Dollar
 
 - `TWD`: New Taiwan Dollar
 
 - `TZS`: Tanzanian Shilling
 
 - `UAH`: Ukrainian Hryvnia
 
 - `UGX`: Ugandan Shilling
 
 - `USD`: US Dollar
 
 - `UYU`: Uruguayan Peso
 
 - `UZS`: Uzbekistan Som
 
 - `VEF`: Venezuelan Bolívar
 
 - `VES`: Venezuelan Bolívar Soberano
 
 - `VND`: Vietnomese Đồng
 
 - `VUV`: Vanuatu Vatu
 
 - `WST`: Samoan Tala
 
 - `XAF`: Central African Cfa Franc
 
 - `XAG`: Silver (Troy Ounce)
 
 - `XAU`: Gold (Troy Ounce)
 
 - `XCD`: East Caribbean Dollar
 
 - `XDR`: Special Drawing Rights
 
 - `XOF`: West African Cfa Franc
 
 - `XPD`: Palladium
 
 - `XPF`: Cfp Franc
 
 - `XPT`: Platinum
 
 - `YER`: Yemeni Rial
 
 - `ZAR`: South African Rand
 
 - `ZMK`: Zambian Kwacha
 
 - `ZMW`: Zambian Kwacha
 
 - `ZWL`: Zimbabwean Dollar
 