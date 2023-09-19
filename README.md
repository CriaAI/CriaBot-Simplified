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
    </code>
</pre>

- Antes de rodar o script extractMessages, abrir o WhatsApp web e a aba inspecionar do navegador
- O script irá percorrer apenas a lista de usuários que possuem mensagens a serem lidas
- Rodar o script e ir até a página do whats. O script começará a rodar em 4 segundos
<br>

`Observação: ` Algumas informações deverão ser mudadas para as informações do Caio (eu deixei especificado em comentários no código)

### Para rodar o streamlit: 
- streamlit run c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/generateAnswers/generateAnswers.py