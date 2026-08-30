import customtkinter as ctk
from functions_utils import (
        retornar_estados,
        resultado_total,
        COMBUSTIVEIS
    )


    # =========================
    # PEGAR ESTADOS
    # =========================
def gui():
    df_pegando_estados = retornar_estados()


    # =========================
    # CONFIGURAÇÃO DA JANELA
    # =========================

    app = ctk.CTk()

    ctk.set_appearance_mode("dark")

    app.title("ANÁLISE DE COMBUSTÍVEIS")

    app.geometry("600x800")

    app.minsize(
        600,
        600
    )

    app.maxsize(
        600,
        800
    )


    # =========================
    # FUNÇÃO DO BOTÃO
    # =========================

    def verificar_selecionados():

        # =========================
        # PEGAR ESTADO
        # =========================

        estado = opcoes_estado.get()


        # =========================
        # PEGAR COMBUSTÍVEIS
        # =========================

        combustiveis_selecionados = []

        for combustivel, checkbox in checkbox_combustiveis.items():

            if checkbox.get() == 1:

                combustiveis_selecionados.append(
                    combustivel
                )


        # =========================
        # LIMPAR TEXTBOX
        # =========================

        resultado_texto.delete(
            "1.0",
            "end"
        )


        # =========================
        # VERIFICAR SE SELECIONOU
        # =========================

        if not combustiveis_selecionados:

            resultado_texto.insert(
                "1.0",
                "Selecione pelo menos um combustível."
            )

            return


        # =========================
        # RODAR ANÁLISE
        # =========================

        df_resultado = resultado_total(
            estado,
            combustiveis_selecionados
        )


        # =========================
        # VERIFICAR SE ENCONTROU DADOS
        # =========================

        if df_resultado.empty:

            resultado_texto.insert(
                "1.0",
                "Nenhum dado encontrado."
            )

            return


        # =========================
        # MAIOR PREÇO
        # =========================

        maior = (
            df_resultado
            .sort_values(
                by="maior_preco",
                ascending=False
            )
            .groupby("Produto")
            .head(1)
        )


        # =========================
        # MAIOR MÉDIA
        # =========================

        media = (
            df_resultado
            .sort_values(
                by="media_preco",
                ascending=False
            )
            .groupby("Produto")
            .head(1)
        )


        # =========================
        # MENOR PREÇO
        # =========================

        menor = (
            df_resultado
            .sort_values(
                by="menor_preco",
                ascending=True
            )
            .groupby("Produto")
            .head(1)
        )


        # =========================
        # CRIAR TEXTO
        # =========================

        texto = ""


        # =========================
        # MAIOR PREÇO
        # =========================

        texto += (
            "========== MAIOR PREÇO ==========\n\n"
        )

        for _, linha in maior.iterrows():

            texto += (
                f"Combustível: {linha['Produto']}\n"
                f"Estado:      {linha['Estado - Sigla']}\n"
                f"Município:   {linha['Municipio']}\n"
                f"Preço:       R${linha['maior_preco']:.2f}\n"
                "\n"
            )


        # =========================
        # MAIOR MÉDIA
        # =========================

        texto += (
            "\n========== MAIOR MÉDIA ==========\n\n"
        )

        for _, linha in media.iterrows():

            texto += (
                f"Combustível: {linha['Produto']}\n"
                f"Estado:      {linha['Estado - Sigla']}\n"
                f"Município:   {linha['Municipio']}\n"
                f"Média:       R${linha['media_preco']:.2f}\n"
                "\n"
            )


        # =========================
        # MENOR PREÇO
        # =========================

        texto += (
            "\n========== MENOR PREÇO ==========\n\n"
        )

        for _, linha in menor.iterrows():

            texto += (
                f"Combustível: {linha['Produto']}\n"
                f"Estado:      {linha['Estado - Sigla']}\n"
                f"Município:   {linha['Municipio']}\n"
                f"Preço:       R${linha['menor_preco']:.2f}\n"
                "\n"
            )


        # =========================
        # MOSTRAR NO TEXTBOX
        # =========================

        resultado_texto.insert(
            "1.0",
            texto
        )


    # =========================
    # OPTION MENU DOS ESTADOS
    # =========================

    opcoes_estado = ctk.CTkOptionMenu(

        app,

        values=df_pegando_estados,

        width=200

    )

    opcoes_estado.pack(
        pady=30
    )


    # =========================
    # TÍTULO
    # =========================

    titulo = ctk.CTkLabel(

        app,

        text="Selecione os combustíveis:",

        font=ctk.CTkFont(
            size=18,
            weight="bold"
        )

    )

    titulo.pack(
        pady=(20, 10)
    )


    # =========================
    # CHECKBOXES
    # =========================

    checkbox_combustiveis = {}


    for combustivel in COMBUSTIVEIS:

        checkbox = ctk.CTkCheckBox(

            app,

            text=combustivel

        )

        checkbox.pack(

            anchor="w",

            padx=100,

            pady=5

        )

        # Guarda cada checkbox no dicionário
        checkbox_combustiveis[
            combustivel
        ] = checkbox


    # =========================
    # BOTÃO
    # =========================

    botao = ctk.CTkButton(

        app,

        text="Selecionar",

        command=verificar_selecionados

    )

    botao.pack(
        pady=30
    )


    # =========================
    # TEXTBOX
    # =========================

    resultado_texto = ctk.CTkTextbox(

        app,

        width=500,

        height=300,

        font=(
            "Consolas",
            14
        )

    )

    resultado_texto.pack(

        pady=20,

        padx=20,

        fill="both",

        expand=True

    )


    # =========================
    # INICIAR APP
    # =========================

    app.mainloop()