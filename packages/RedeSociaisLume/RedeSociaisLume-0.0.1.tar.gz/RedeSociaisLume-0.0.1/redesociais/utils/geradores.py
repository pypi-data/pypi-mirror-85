def gerar_url(*args) -> str:
    """
        Cria o caminho da url de para os endpoints

        Returns:
            str: URL montada
        """

    return "/".join(args)
