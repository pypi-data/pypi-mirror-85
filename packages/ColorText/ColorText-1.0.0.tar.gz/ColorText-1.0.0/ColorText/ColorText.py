class ColorText:
    @staticmethod
    def mudaCor(word = 'Texto Exemplo',color = 'white',style = 'neg'):
        """
             O metodo irá mudar a cor do texto referenciado e também permitirá mudar para negrito ou sublinhado
        Argumentos:
            -Word: O texto ou caracter que vai ter a cor mudada
            -Color: A cor escolhida. Para isso, o usuario deve digitar uma cor(em inglês)
            -Style: Define se o texto ficara em negrito ou sublinhado. Para isso digite: neg ou sub
        Uso exemplo:
            ColorText.mudacor('Ola mundo!','red',1) --> Retorna Ola Mundo em vermelho e negrito
        Erros:
            -O usario digitar uma cor fora do permitido
            -O usuario digitar um style fora do permitido
        """
        cores = {'white':'30','red':'31','green':'32','yellow':'33','blue':'34',
        'purple':'35','gray':'37'}
        styles = {'norm':'0','neg':'1','sub':'4'}
        words = word
        wordChanged = f'\033[{styles[style]};{cores[color]}m{words}\033[m'
        return wordChanged

        