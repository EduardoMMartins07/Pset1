# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: 'Eduardo Moisés Martins'
#    Matrícula: '202202118'
#    Turma: 'CC3M'
#    Email: 'dudummartins7@gmail.com'
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.
#


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage
# Havia um erro de 'reportMissingModuleSource' e não conseguia importar PIL.Image,
# para solucionar só intalei localmente o modulo Pillow.

# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        # para retornar o endereço do indice dentro de um array unidimencional
        # tem que fazer o calculo com a formula: (largura * x) + y.
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x >= self.altura:
            x = self.altura - 1
        if y >= self.largura:
            y = self.largura - 1
        return self.pixels[(self.largura * x) + y]
        # Se algum parâmetro estiver fora dos limites, atribui a ele o valor limite daquela direção.

    def set_pixel(self, x, y, c):
        self.pixels[(self.largura * x) + y] = c
        # da mesma maneira que na função get_pixel a indexação estava incorreta
        # nesta função também precisou ser corrigida para a forma atual.

    def aplicar_por_pixel(self, func):
        resultado = Imagem.nova(self.largura, self.altura)
        # inverti a ordem dos parâmetros da função 'nova'
        # para que o 1° agumento seja a largura e depois a altura.
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(y, x)
                # Inverti a ordem para que ficasse coerênte com a formula usada na função.
                nova_cor = func(cor)
                resultado.set_pixel(y, x, nova_cor)
                # a linha de cima não estava dentro deste 'for', dei um 'tab' nela
                # para que a mudança ocorresse a todos os pixeis e não uma vez por linha.
        return resultado
    
    def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255 - c)
        # o valor máximo na escala RGB é ff, ou 255, que é o branco
        # por isso o valor que será subtraido por 'c' tem que ser 255.

    def correlacao(self, kernel, n):
        # Essa função recebe um Kernel que é representado por uma lista e o valor de n.
        resultado = Imagem.nova(self.largura, self.altura)
        # Criando uma nova imagem para fazer o correlacionamento.
        m = int((n - 1) / 2)
        # Considerando que quailquer valor de n seja um número impar.
        for x in range(self.largura):
            for y in range(self.altura):
            # Os dois loops acima são para que seja feito em cada pixel da imagem.
                soma_kernel = 0
                i = 0
                for l in range((x - m), (x + m + 1)):
                    for a in range((y - m), (y + m + 1)):
                    # Os dois loops acima, é feito para fazer o calculo de correlacionamento entre a imagem e o kernel.
                        soma_kernel += self.get_pixel(a, l) * kernel[i]
                        i += 1
                        # Soma todos os valores do correlacionamento de cada pixel com seu respectivo valor do kernel.
                soma_kernel = round(soma_kernel)
                # Para que n haja valores float.
                if soma_kernel > 255:
                    soma_kernel = 255
                    # Limitando o valor máximo a 255.
                if soma_kernel < 0:
                    soma_kernel = 0
                    # Limitando o valor mínimo a 0.
                resultado.set_pixel(y, x, soma_kernel)
                # Aplicando o valor resultante ao respectivo pixel.
        return resultado

    # Essa função recebe n, e cria uma lista de tamanha n*n e preenche ela inteira com o valor de 1/(n*n)
    # para que a soma de todos os valores da lista seja igual a 1. No retorn dela, ela chama a função correlação
    # enviando como parametros a lista e n.
    def borrada(self, n):
        kernel = []
        valores_kernel = 1 / (n*n)
        for i in range(n*n):
            kernel.append(valores_kernel)
        return self.correlacao(kernel, n)
            
    # A função cria uma nova imagem e uma imagem borrada, aplica a formula e retorna a imagem filtrada.
    def focada(self, n):
        im = Imagem.nova(self.largura, self.altura)  
        borrada = self.borrada(n)
        for x in range(self.largura):
            for y in range(self.altura):
                pixel_borrado = borrada.get_pixel(y, x)
                # Armazena o valor do pixel da imagem borrada, de cada coordenada individual.
                pixel_normal = self.get_pixel(y, x)
                # Armazena o valor do pixel da imagem normal, de cada coordenada individual.
                resultado_parcial = (pixel_normal*2) - pixel_borrado
                if resultado_parcial > 255:
                    resultado_parcial = 255
                if resultado_parcial < 0:
                    resultado_parcial = 0
                # Aplica a formula e condiciona para estar entre [0, 255] e aplica o valor.
                im.set_pixel(y, x, resultado_parcial)
        return im
    
    def bordas(self):
        resultado = Imagem.nova(self.largura, self.altura)
        # O Kernel de Kx:
        kernel_x = [-1, 0, 1,
                    -2, 0, 2,
                    -1, 0, 1]
        # O Kernel de Ky:
        kernel_y = [-1, -2, -1,
                     0,  0,  0,
                     1,  2,  1]
        
        # Faz 1 imagem com cada Kernel.
        o_x = self.correlacao(kernel_x, 3)
        o_y = self.correlacao(kernel_y, 3)

        for x in range(self.largura):
            for y in range(self.altura):
                # Aplicando a formula para cada valor de Ox e Oy.
                valor_parcial = round(math.sqrt( ((o_x.get_pixel(y, x))**2) + ((o_y.get_pixel(y, x))**2) ))
                if valor_parcial < 0:
                    valor_parcial = 0
                if valor_parcial > 255:
                    valor_parcial = 255
                # Aplicando o valor resultante em sua determinada coordenada.
                resultado.set_pixel(y, x, valor_parcial)
        return resultado
        # A função de bordas não está 100%, ao fazer os testes há falhas.

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.largura, event.altura), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.altura, width=event.largura)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.altura, width=e.largura))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
