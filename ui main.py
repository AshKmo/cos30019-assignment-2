import math
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from test_file_lib import read_test_file
from BFS import breadth_first_search
from DFS import depth_first_search
from A_star import a_star_search
from GBFS import greedy_best_first_search
from CUS1 import uniform_cost_search
from beam_search import beam_search

import heuristics

class SearchUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Route Finding Visualiser")
        self.root.geometry("1350x850")
        self.root.minsize(1100, 700)

        self.filename = None
        self.origin = None
        self.destinations = None
        self.graph_nodes = None
        self.current_path = None

        # stores canvas positions for each node
        self.node_positions = {}

        self.setup_style()
        self.setup_ui()



    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#f4f6f8")
        style.configure("TLabel", background="#f4f6f8", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#f4f6f8", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TCombobox", padding=4)

    def setup_ui(self):
        # main layout
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(main)
        top.pack(fill=tk.X, pady=(0, 10))

        middle = ttk.Frame(main)
        middle.pack(fill=tk.BOTH, expand=True)

        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X, pady=(10, 0))

        # top controls
        ttk.Button(top, text="Load Test File", command=self.load_file).pack(side=tk.LEFT, padx=(0, 10))

        self.file_label = ttk.Label(top, text="No file loaded")
        self.file_label.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(top, text="Algorithm:").pack(side=tk.LEFT, padx=(0, 5))
        self.method_var = tk.StringVar(value="BFS")
        self.method_box = ttk.Combobox(
            top,
            textvariable=self.method_var,
            state="readonly",
            width=28,
            values=[
                "BFS",
                "DFS",
                "GBFS",
                "A*",
                "CUS1 - Uniform Cost Search",
                "CUS2 - Beam Search"
            ]
        )
        self.method_box.pack(side=tk.LEFT, padx=(0, 15))
        self.method_box.bind("<<ComboboxSelected>>", self.on_method_change)

        ttk.Label(top, text="Heuristic:").pack(side=tk.LEFT, padx=(0, 5))
        self.heuristic_var = tk.StringVar(value="distance")
        self.heuristic_box = ttk.Combobox(
            top,
            textvariable=self.heuristic_var,
            state="readonly",
            width=12,
            values=["distance", "angle"]
        )
        self.heuristic_box.pack(side=tk.LEFT, padx=(0, 15))

        self.beam_label = ttk.Label(top, text="Beam Width:")
        self.beam_width_var = tk.StringVar(value="2")
        self.beam_width_entry = ttk.Entry(top, textvariable=self.beam_width_var, width=6)

        ttk.Button(top, text="Run Search", command=self.run_search).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(top, text="Reset", command=self.reset_path).pack(side=tk.LEFT)

        # graph panel
        graph_card = ttk.Frame(middle, padding=10)
        graph_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(graph_card, text="Graph View", style="Header.TLabel").pack(anchor="w", pady=(0, 8))

        self.canvas = tk.Canvas(
            graph_card,
            bg="white",
            highlightthickness=1,
            highlightbackground="#cfd8dc"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # redraw graph automatically when window size changes
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # right info panel
        side = ttk.Frame(middle, padding=(12, 10))
        side.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(side, text="Run Information", style="Header.TLabel").pack(anchor="w", pady=(0, 8))

        self.info_text = tk.Text(
            side,
            width=34,
            height=20,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#ffffff",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#cfd8dc"
        )
        self.info_text.pack(fill=tk.BOTH, expand=False)

        ttk.Label(side, text="Legend", style="Header.TLabel").pack(anchor="w", pady=(15, 8))

        legend = tk.Text(
            side,
            width=34,
            height=8,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg="#ffffff",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#cfd8dc"
        )
        legend.pack(fill=tk.X)
        legend.insert(
            tk.END,
            "Green   = Origin\n"
            "Yellow  = Destination\n"
            "Red     = Path node\n"
            "Red edge = Final path\n"
            "Blue    = Edge cost\n"
        )
        legend.config(state=tk.DISABLED)

        # bottom output panel
        ttk.Label(bottom, text="Program Output", style="Header.TLabel").pack(anchor="w", pady=(0, 8))

        self.output_text = tk.Text(
            bottom,
            height=10,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#ffffff",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#cfd8dc"
        )
        self.output_text.pack(fill=tk.X)

        # apply initial control visibility
        self.on_method_change()

    def on_method_change(self, event=None):
        method = self.method_var.get()

        # show beam width only for Beam Search
        if method == "CUS2 - Beam Search":
            self.beam_label.pack(side=tk.LEFT, padx=(0, 5))
            self.beam_width_entry.pack(side=tk.LEFT, padx=(0, 15))
        else:
            self.beam_label.pack_forget()
            self.beam_width_entry.pack_forget()

        # show heuristic only for informed methods
        if method in ["GBFS", "A*", "CUS2 - Beam Search"]:
            self.heuristic_box.config(state="readonly")
        else:
            self.heuristic_box.config(state="disabled")


    def load_file(self):
        filename = filedialog.askopenfilename(
            title="Select Test File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if not filename:
            return

        try:
            self.origin, self.destinations, self.graph_nodes = read_test_file(filename)
            self.filename = filename
            self.file_label.config(text=filename)
            self.current_path = None
            self.draw_graph()
            self.write_info("File loaded successfully.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def get_heuristic(self):
        if self.heuristic_var.get() == "angle":
            return heuristics.AngleHeuristic(self.origin, self.destinations, self.graph_nodes)
        return heuristics.DistanceHeuristic(self.origin, self.destinations, self.graph_nodes)

    def run_search(self):
        if self.graph_nodes is None:
            messagebox.showwarning("No File", "Please load a test file first.")
            return

        method = self.method_var.get()
        result = None

        try:
            if method == "BFS":
                result = breadth_first_search(self.origin)

            elif method == "DFS":
                result = depth_first_search(self.origin)

            elif method == "GBFS":
                result = greedy_best_first_search(self.origin, self.get_heuristic())

            elif method == "A*":
                result = a_star_search(self.origin, self.get_heuristic())

            elif method == "CUS1 - Uniform Cost Search":
                result = uniform_cost_search(self.origin)

            elif method == "CUS2 - Beam Search":
                beam_width = int(self.beam_width_var.get())
                if beam_width < 1:
                    raise ValueError("Beam width must be at least 1.")
                result = beam_search(self.origin, self.get_heuristic(), beam_width)

            else:
                messagebox.showerror("Error", f"Unknown method: {method}")
                return

        except Exception as e:
            messagebox.showerror("Error", f"Search failed:\n{e}")
            return

        path = result[0]
        node_count = result[1]

        self.current_path = path
        self.draw_graph()

        self.output_text.delete("1.0", tk.END)
        self.info_text.delete("1.0", tk.END)

        if path is None:
            self.output_text.insert(tk.END, f"{self.filename} {method}\nNo goal found {node_count}\n")
            self.info_text.insert(tk.END, f"Method: {method}\n")
            self.info_text.insert(tk.END, f"Nodes created: {node_count}\n")
            self.info_text.insert(tk.END, "No path found.\n")
            return

        # show output in assignment-style format
        self.output_text.insert(tk.END, f"{self.filename} {method}\n")
        self.output_text.insert(tk.END, f"{path[-1]} {node_count}\n")
        for location in path:
            self.output_text.insert(tk.END, f"{location}\n")

        path_cost = self.calculate_path_cost(path)

        self.info_text.insert(tk.END, f"Method: {method}\n")
        if method in ["GBFS", "A*", "CUS2 - Beam Search"]:
            self.info_text.insert(tk.END, f"Heuristic: {self.heuristic_var.get()}\n")
        if method == "CUS2 - Beam Search":
            self.info_text.insert(tk.END, f"Beam Width: {self.beam_width_var.get()}\n")
        self.info_text.insert(tk.END, f"Goal reached: {path[-1].name}\n")
        self.info_text.insert(tk.END, f"Nodes created: {node_count}\n")
        self.info_text.insert(tk.END, f"Moves: {len(path) - 1}\n")
        self.info_text.insert(tk.END, f"Path cost: {path_cost}\n\n")
        self.info_text.insert(tk.END, "Path:\n")
        self.info_text.insert(tk.END, " -> ".join(str(node.name) for node in path))

    def calculate_path_cost(self, path):
        if path is None or len(path) < 2:
            return 0

        total = 0

        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]

            for edge in current_node.edges:
                if edge.node_to == next_node:
                    total += edge.cost
                    break

        return total
    

    def reset_path(self):
        self.current_path = None
        self.output_text.delete("1.0", tk.END)
        self.info_text.delete("1.0", tk.END)
        self.draw_graph()

    def write_info(self, message):
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, message)

    def on_canvas_resize(self, event):
        if self.graph_nodes is not None:
            self.draw_graph()

    def draw_graph(self):
        self.canvas.delete("all")
        self.node_positions.clear()

        if self.graph_nodes is None:
            return

        width = max(self.canvas.winfo_width(), 700)
        height = max(self.canvas.winfo_height(), 500)

        margin = 80
        node_radius = 22

        # get coordinate range for scaling
        xs = [node.x for node in self.graph_nodes.values()]
        ys = [node.y for node in self.graph_nodes.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        x_range = max(max_x - min_x, 1)
        y_range = max(max_y - min_y, 1)

        # work out where each node goes on the canvas
        for node in self.graph_nodes.values():
            canvas_x = margin + ((node.x - min_x) / x_range) * (width - 2 * margin)
            canvas_y = height - (margin + ((node.y - min_y) / y_range) * (height - 2 * margin))
            self.node_positions[node.name] = (canvas_x, canvas_y)

        # draw background grid
        for i in range(0, width, 50):
            self.canvas.create_line(i, 0, i, height, fill="#f1f3f5")
        for j in range(0, height, 50):
            self.canvas.create_line(0, j, width, j, fill="#f1f3f5")

        # draw edges first
        for node in self.graph_nodes.values():
            x1, y1 = self.node_positions[node.name]

            for edge in node.edges:
                x2, y2 = self.node_positions[edge.node_to.name]

                dx = x2 - x1
                dy = y2 - y1
                dist = math.sqrt(dx * dx + dy * dy)

                if dist == 0:
                    continue

                ux = dx / dist
                uy = dy / dist

                start_x = x1 + ux * node_radius
                start_y = y1 + uy * node_radius
                end_x = x2 - ux * node_radius
                end_y = y2 - uy * node_radius

                edge_colour = "#7f8c8d"
                edge_width = 2

                # highlight edges that are part of the final path
                if self.edge_in_current_path(node, edge.node_to):
                    edge_colour = "#e53935"
                    edge_width = 4

                self.canvas.create_line(
                    start_x, start_y, end_x, end_y,
                    arrow=tk.LAST,
                    arrowshape=(12, 14, 5),
                    width=edge_width,
                    fill=edge_colour,
                    smooth=True
                )

                # draw edge cost near the middle
                mid_x = (start_x + end_x) / 2
                mid_y = (start_y + end_y) / 2

                self.canvas.create_text(
                    mid_x + 10, mid_y - 12,
                    text=str(edge.cost),
                    fill="#1565c0",
                    font=("Segoe UI", 9, "bold")
                )

        # draw nodes after edges so they appear on top
        for node in self.graph_nodes.values():
            x, y = self.node_positions[node.name]

            fill_colour = "#dfe6e9"
            outline_colour = "#2d3436"
            line_width = 2

            if node.is_origin:
                fill_colour = "#a5d6a7"
                outline_colour = "#2e7d32"

            if node.is_destination:
                fill_colour = "#fff59d"
                outline_colour = "#f9a825"

            if self.node_in_current_path(node):
                fill_colour = "#ef9a9a"
                outline_colour = "#c62828"
                line_width = 3

            if node.is_origin and self.node_in_current_path(node):
                fill_colour = "#81c784"
            if node.is_destination and self.node_in_current_path(node):
                fill_colour = "#ffcc80"

            self.canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=fill_colour,
                outline=outline_colour,
                width=line_width
            )

            self.canvas.create_text(
                x, y - 1,
                text=str(node.name),
                font=("Segoe UI", 10, "bold"),
                fill="#212121"
            )

            self.canvas.create_text(
                x, y + 32,
                text=f"({node.x},{node.y})",
                font=("Segoe UI", 8),
                fill="#616161"
            )

    def node_in_current_path(self, node):
        return self.current_path is not None and node in self.current_path

    def edge_in_current_path(self, node_from, node_to):
        if self.current_path is None or len(self.current_path) < 2:
            return False

        for i in range(len(self.current_path) - 1):
            if self.current_path[i] == node_from and self.current_path[i + 1] == node_to:
                return True

        return False
    def reset_path(self):
        self.current_path = None
        self.output_text.delete("1.0", tk.END)
        self.draw_graph()

    def on_canvas_resize(self, event):
        if self.graph_nodes:
            self.draw_graph()


if __name__ == "__main__":
    root = tk.Tk()
    app = SearchUI(root)
    root.mainloop()