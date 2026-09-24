import tkinter as tk
from tkinter import messagebox

from dados import (
    carregar_perguntas,
    carregar_resultados,
    salvar_resultado
)

from validacoes import validar_nome


class QuizViandido:

    def __init__(self, janela):

        self.janela = janela

        self.janela.title("Quiz Viandido")
        self.janela.geometry("700x500")
        self.janela.resizable(False, False)

        self.perguntas = carregar_perguntas()

        self.nome = ""
        self.questao_atual = 0
        self.pontos = 0

        self.criar_tela_inicial()

    def limpar_tela(self):

        for widget in self.janela.winfo_children():
            widget.destroy()

    def criar_tela_inicial(self):

        self.limpar_tela()

        titulo = tk.Label(
            self.janela,
            text="⚽ QUIZ VIANDIDO ⚽",
            font=("Arial", 28, "bold")
        )

        titulo.pack(pady=50)

        descricao = tk.Label(
            self.janela,
            text="Teste seus conhecimentos sobre futebol!",
            font=("Arial", 16)
        )

        descricao.pack(pady=10)

        self.campo_nome = tk.Entry(
            self.janela,
            font=("Arial", 16),
            width=30
        )

        self.campo_nome.pack(pady=20)

        self.campo_nome.insert(
            0,
            "Digite seu nome"
        )

        botao = tk.Button(
            self.janela,
            text="COMEÇAR QUIZ",
            font=("Arial", 14, "bold"),
            command=self.iniciar_quiz,
            width=20
        )

        botao.pack(pady=20)

        historico = tk.Button(
            self.janela,
            text="Ver histórico",
            font=("Arial", 12),
            command=self.mostrar_historico
        )

        historico.pack()

    def iniciar_quiz(self):

        nome = self.campo_nome.get()

        if not validar_nome(nome):

            messagebox.showwarning(
                "Nome inválido",
                "Digite um nome válido."
            )

            return

        if not self.perguntas:

            messagebox.showerror(
                "Erro",
                "Nenhuma pergunta foi encontrada."
            )

            return

        self.nome = nome.strip()
        self.questao_atual = 0
        self.pontos = 0

        self.mostrar_pergunta()

    def mostrar_pergunta(self):

        self.limpar_tela()

        pergunta = self.perguntas[
            self.questao_atual
        ]

        numero = self.questao_atual + 1
        total = len(self.perguntas)

        contador = tk.Label(
            self.janela,
            text=f"Pergunta {numero} de {total}",
            font=("Arial", 14)
        )

        contador.pack(pady=20)

        texto = tk.Label(
            self.janela,
            text=pergunta["pergunta"],
            font=("Arial", 18, "bold"),
            wraplength=600
        )

        texto.pack(pady=30)

        for indice, opcao in enumerate(
            pergunta["opcoes"],
            start=1
        ):

            botao = tk.Button(
                self.janela,
                text=f"{indice} - {opcao}",
                font=("Arial", 13),
                width=45,
                command=lambda i=indice:
                    self.responder(i)
            )

            botao.pack(pady=5)

    def responder(self, resposta):

        pergunta = self.perguntas[
            self.questao_atual
        ]

        if resposta == pergunta["resposta"]:
            self.pontos += 1

            messagebox.showinfo(
                "Resposta",
                "✓ Resposta correta!"
            )

        else:

            correta = pergunta["opcoes"][
                pergunta["resposta"] - 1
            ]

            messagebox.showinfo(
                "Resposta",
                f"✗ Resposta incorreta!\n\n"
                f"Resposta correta: {correta}"
            )

        self.questao_atual += 1

        if self.questao_atual >= len(self.perguntas):
            self.mostrar_resultado()

        else:
            self.mostrar_pergunta()

    def mostrar_resultado(self):

        self.limpar_tela()

        total = len(self.perguntas)

        porcentagem = (
            self.pontos / total
        ) * 100

        titulo = tk.Label(
            self.janela,
            text="🏆 RESULTADO FINAL",
            font=("Arial", 26, "bold")
        )

        titulo.pack(pady=40)

        resultado = tk.Label(
            self.janela,
            text=(
                f"Jogador: {self.nome}\n\n"
                f"Acertos: {self.pontos}/{total}\n\n"
                f"Pontuação: {porcentagem:.1f}%"
            ),
            font=("Arial", 18)
        )

        resultado.pack(pady=20)

        if porcentagem == 100:

            mensagem = "Parabéns! Você acertou tudo!"

        elif porcentagem >= 70:

            mensagem = "Muito bom! Você conhece bastante futebol!"

        elif porcentagem >= 50:

            mensagem = "Bom trabalho! Continue estudando!"

        else:

            mensagem = "Continue estudando a história do futebol!"

        mensagem_label = tk.Label(
            self.janela,
            text=mensagem,
            font=("Arial", 14)
        )

        mensagem_label.pack(pady=10)

        resultado_json = {
            "nome": self.nome,
            "acertos": self.pontos,
            "total": total,
            "porcentagem": round(porcentagem, 1)
        }

        salvar_resultado(resultado_json)

        botao = tk.Button(
            self.janela,
            text="Voltar ao início",
            font=("Arial", 13),
            command=self.criar_tela_inicial
        )

        botao.pack(pady=25)

    def mostrar_historico(self):

        self.limpar_tela()

        titulo = tk.Label(
            self.janela,
            text="📊 HISTÓRICO",
            font=("Arial", 24, "bold")
        )

        titulo.pack(pady=30)

        resultados = carregar_resultados()

        if not resultados:

            texto = tk.Label(
                self.janela,
                text="Nenhum resultado registrado.",
                font=("Arial", 14)
            )

            texto.pack(pady=20)

        else:

            for resultado in resultados:

                texto = (
                    f"{resultado['nome']} - "
                    f"{resultado['acertos']}/"
                    f"{resultado['total']} - "
                    f"{resultado['porcentagem']}%"
                )

                label = tk.Label(
                    self.janela,
                    text=texto,
                    font=("Arial", 13)
                )

                label.pack(pady=5)

        botao = tk.Button(
            self.janela,
            text="Voltar",
            font=("Arial", 12),
            command=self.criar_tela_inicial
        )

        botao.pack(pady=30)


def iniciar_aplicacao():

    janela = tk.Tk()

    QuizViandido(janela)

    janela.mainloop()
