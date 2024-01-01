import tkinter as tk
from tkinter import ttk
from datetime import datetime

class FinancasApp:
    def __init__(self):
        self.salario_liquido = 0.0
        self.saldo_minimo = 0.0
        self.despesas = {}
        self.historico = []

    def adicionar_despesa(self, categoria, valor):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if categoria in self.despesas:
            self.despesas[categoria] += valor
        else:
            self.despesas[categoria] = valor
        self.historico.append({"data": data, "categoria": categoria, "valor": valor})

    def obter_historico(self):
        return self.historico

    def calcular_saldo_disponivel(self):
        total_despesas = sum(self.despesas.values())
        saldo_disponivel = self.salario_liquido - total_despesas
        return saldo_disponivel

    def feedback_usuario(self):
        saldo_disponivel = self.calcular_saldo_disponivel()
        if saldo_disponivel >= self.saldo_minimo:
            return f"Saldo disponível: R$ {saldo_disponivel:.2f}. Você está dentro do orçamento."
        else:
            return f"Saldo disponível: R$ {saldo_disponivel:.2f}. Pare de gastar! Você atingiu ou ultrapassou o limite do salário disponível."

class FinancasAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Finanças App")

        # Definindo a largura e altura da janela principal e posição inicial
        self.root.geometry("600x400+0+0")  # Ajuste conforme necessário
        self.root.resizable(True, True)  # Permitir redimensionamento em largura e altura

        # Variáveis
        self.salario_var = tk.DoubleVar()
        self.saldo_minimo_var = tk.DoubleVar()
        self.categoria_var = tk.StringVar()
        self.valor_var = tk.DoubleVar()

        # Widgets
        tk.Label(root, text="Salário Líquido do Mês:").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.salario_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Saldo Mínimo:").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.saldo_minimo_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Categoria da Despesa:").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.categoria_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Valor da Despesa:").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(root, textvariable=self.valor_var).grid(row=3, column=1, padx=10, pady=5)

        tk.Button(root, text="Adicionar Despesa", command=self.adicionar_despesa).grid(row=4, column=0, columnspan=2, pady=10)

        # Área de exibição do histórico usando Treeview
        self.historico_tree = ttk.Treeview(root, columns=("Data", "Categoria", "Valor"), show="headings", height=10)
        self.historico_tree.heading("Data", text="Data")
        self.historico_tree.heading("Categoria", text="Categoria")
        self.historico_tree.heading("Valor", text="Valor")
        self.historico_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Criar instância do aplicativo financeiro
        self.app = FinancasApp()

    def adicionar_despesa(self):
        self.app.salario_liquido = self.salario_var.get()
        self.app.saldo_minimo = self.saldo_minimo_var.get()

        categoria = self.categoria_var.get()
        valor = self.valor_var.get()

        if categoria and valor:
            self.app.adicionar_despesa(categoria, valor)

            # Atualizar a área de exibição do histórico
            historico = self.app.obter_historico()
            self.historico_tree.delete(*self.historico_tree.get_children())
            for entrada in historico:
                self.historico_tree.insert("", "end", values=(entrada['data'], entrada['categoria'], f"R$ {entrada['valor']:.2f}"))

            # Limpar os campos de entrada
            self.categoria_var.set("")
            self.valor_var.set("")

            # Chamar a função feedback_usuario e mostrar a mensagem
            feedback = self.app.feedback_usuario()
            tk.messagebox.showinfo("Feedback", feedback)

if __name__ == "__main__":
    root = tk.Tk()
    app_gui = FinancasAppGUI(root)
    root.mainloop()
