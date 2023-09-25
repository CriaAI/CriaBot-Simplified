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

## Abrir o streamlit para rodar os scripts
- Para rodar o streamlit, digitar no cmd o caminho para o arquivo:
    - Exemplo do meu pc: streamlit run c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/scripts/generateAnswers/generateAnswers.py
- Ao rodar esse comando, uma aba será aberta no navegador automaticamente
- Inicialmente, havendo leads que estão esperando por respostas, a página irá carregar a geração de mensagens
- Após todas as mensagens terem sido geradas, aparecerão 3 botões na tela, um para cada script (enviar primeira mensagem, extrair mensagens e enviar mensagens)
- Ao clicar em cada um desses botões, o respectivo script será rodado (deve-se ir até a página do whats app web)
<br>

`Observação:` Algumas informações deverão ser mudadas para as informações da pessoa que estiver testando (eu deixei especificado em comentários no código)