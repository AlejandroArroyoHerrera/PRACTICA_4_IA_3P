# -*- coding: utf-8 -*-
"""
@author: arroy
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq

class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador del Algoritmo de Prim")
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack()

        self.nodes = {}
        self.edges = {}
        self.selected_node = None

        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-3>", self.select_node)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.menu.add_command(label="Agregar Arista", command=self.add_edge)
        self.menu.add_command(label="Calcular Árbol Parcial Mínimo", command=self.calculate_mst)

    def add_node(self, event):
        node_id = simpledialog.askstring("Input", "Ingrese el nombre del nodo:")
        if node_id and node_id not in self.nodes:
            self.nodes[node_id] = (event.x, event.y)
            self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill="blue")
            self.canvas.create_text(event.x, event.y, text=node_id, fill="white")

    def select_node(self, event):
        nearest_node = None
        min_distance = float("infinity")
        for node, (x, y) in self.nodes.items():
            distance = (x - event.x)**2 + (y - event.y)**2
            if distance < min_distance:
                nearest_node = node
                min_distance = distance

        if nearest_node:
            if self.selected_node:
                self.canvas.itemconfig(self.selected_node, fill="blue")
            self.selected_node = self.canvas.find_closest(event.x, event.y)[0]
            self.canvas.itemconfig(self.selected_node, fill="red")

    def add_edge(self):
        if self.selected_node:
            from_node = simpledialog.askstring("Input", "Ingrese el nodo de origen:")
            to_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:")
            weight = simpledialog.askinteger("Input", "Ingrese el peso de la arista:")

            if from_node in self.nodes and to_node in self.nodes and weight:
                self.edges.setdefault(from_node, {})[to_node] = weight
                self.edges.setdefault(to_node, {})[from_node] = weight  # Asumimos grafo no dirigido

                x1, y1 = self.nodes[from_node]
                x2, y2 = self.nodes[to_node]
                self.canvas.create_line(x1, y1, x2, y2)
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(weight), fill="black")

    def calculate_mst(self):
        if not self.nodes or not self.edges:
            messagebox.showwarning("Advertencia", "Debe agregar nodos y aristas primero.")
            return

        start_node = simpledialog.askstring("Input", "Ingrese el nodo de inicio:")
        if start_node in self.nodes:
            mst, total_weight = self.prim(self.edges, start_node)
            messagebox.showinfo("Resultado", f"Peso total del Árbol Parcial Mínimo: {total_weight}")
            self.show_mst(mst)
        else:
            messagebox.showwarning("Advertencia", "Nodo de inicio no válido.")

    def prim(self, graph, start):
        mst = []
        visited = set()
        edges = [(0, start, start)]
        total_weight = 0

        while edges:
            weight, frm, to = heapq.heappop(edges)
            if to not in visited:
                visited.add(to)
                mst.append((frm, to, weight))
                total_weight += weight

                for next_to, next_weight in graph[to].items():
                    if next_to not in visited:
                        heapq.heappush(edges, (next_weight, to, next_to))

        return mst[1:], total_weight  # Exclude the initial dummy edge

    def show_mst(self, mst):
        for frm, to, weight in mst:
            if frm != to:  # Skip the initial dummy edge
                x1, y1 = self.nodes[frm]
                x2, y2 = self.nodes[to]
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
