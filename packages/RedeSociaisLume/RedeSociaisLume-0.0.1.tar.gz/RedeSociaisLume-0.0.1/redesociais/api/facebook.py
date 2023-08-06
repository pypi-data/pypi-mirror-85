import requests

from redesociais.utils import gerar_url


class Facebook:
    def __init__(self, id_pagina: int, token_usuario: str) -> None:
        """
        Classe responsavel por a fazer a conexção com o Facebook

        Args:
            id_pagina (int): ID da pagina 
            token_usuario (str): token de usuário
        """

        self.caminho = gerar_url("https://graph.facebook.com/v8.0", id_pagina)
        self.token_pagina = self.gerar_token_acesso_pagina(token_usuario)

    def criando_publicacao(self, **kwargs) -> None:
        """
        Escreve publicação na rede social.

        **kwargs:
            message (str): Mensagem que será salva no post
            link (str): Url do link que deseja se exibido
        """

        kwargs.update(
            {
                "access_token": self.token_pagina
            }
        )
        resposta = requests.post(
            gerar_url(
                self.caminho,
                "feed"
            ),
            data=kwargs,
        )

        return resposta

    def gerar_token_acesso_pagina(self, token: str) -> str:
        """
        Gera token de pagina para acessa-lá

        Args:
            token (str): Token de usuário

        Returns:
            str: Token de pagina
        """
        token = requests.get(
            self.caminho,
            params={
                "fields": "access_token",
                "access_token": token
            }
        )

        return token.json()['access_token']
