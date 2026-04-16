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
