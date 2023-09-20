# CriaAI ChatBot

## Para rodar o projeto:
- Preencha o arquivo .env com as seguintes informações:
<pre>
    <code>
        project_id = xxxxxxxxx
        private_key_id = xxxxxxxxxx
        private_key = xxxxxxxxxxx
        client_email = xxxxxxxxx
        client_id = xxxxxxxxxxxx
        auth_uri = xxxxxxxxxxxxx
        token_uri = xxxxxxxxxxx
        auth_provider_x509_cert_url = xxxxxxxxxxx
        client_x509_cert_url = xxxxxxxxxxx
        universe_domain = xxxxxxxxxxx

        BASE_URL = xxxxxxxxxxxxx
        API_KEY = xxxxxxxxxxxxx
    </code>
</pre>

### Script Extract Messages
- Abrir o WhatsApp web e a aba inspecionar do navegador
- Rodar o script e ir até a página do whats. O script começará a rodar em 4 segundos
- OBS: O script irá percorrer apenas a lista de usuários que possuem mensagens a serem lidas
<br>

### Script Generate Answers
- Para rodar o strealit, digitar no cmd o caminho para o arquivo:
    - Exemplo do meu pc: streamlit run c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/generateAnswers/generateAnswers.py
- Ao rodar esse comando, uma aba será aberta no navegador automaticamente
<br>

### Script Send Messages
- Abrir o WhatsApp web SEM a aba inspecionar aberta
- Rodar o script e ir até a página do whats. O script começará a rodar em 4 segundos
<br>

`Observação:` Algumas informações deverão ser mudadas para as informações da pessoa que estiver testando (eu deixei especificado em comentários no código)