# CriaAI ChatBot

## Configurando o ambiente
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

        OPENAI_API_TYPE = xxxxxx
        OPENAI_API_BASE = xxxxxxxxxxxxxxxxxxxxx
        OPENAI_API_KEY = xxxxxxxxxxxxxxxxxxxxxxxxx
        OPENAI_API_VERSION = xxxxxxxx

        PINECONE_API_KEY = xxxxxxxxxxxxxxxxxxxxxx
        PINECONE_ENVIRONMENT = xxxxxxxxx
    </code>
</pre>
<br>

- Vá para o arquivo config.py e preencha as variáveis de acordo com o seu caso específico
- No arquivo run_app.bat, preencha o caminho para o seu arquivo generateAnswers.py

## Para rodar o projeto:
- Na linha de comando, digite: `./run_app.bat`
- Uma aba será aberta no navegador automaticamente
- Inicialmente, havendo leads que estão esperando por respostas, a página irá carregar a geração de mensagens
- Após todas as mensagens terem sido geradas, aparecerão 4 botões na tela, um para cada script (enviar primeira mensagem, extrair mensagens e enviar mensagens) e um botão para cancelar a ação do script
- Ao clicar em cada um desses botões, o respectivo script será rodado (deve-se ir até a página do whatsapp web)
<br>