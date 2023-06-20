import tkinter as tk
import math
from PIL import Image, ImageTk

class ClosestPairGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Par de Pontos Mais Próximos")
        
        self.canvas_width = 900
        self.canvas_height = 720
        
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        
        # Carregar a imagem de fundo
        image = Image.open(r"DC_CARTEIRO_G25\assets\map.png")
        image = image.resize((self.canvas_width, self.canvas_height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(image)
        
        # Desenhar a imagem de fundo no canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        
        self.points = []
        self.line_item = None  # Referência à linha vermelha
        self.circle_item = None  # Referência ao círculo vermelho
        
        self.canvas.bind("<Button-1>", self.add_point)
        self.button = tk.Button(self.master, text="Encontrar Par Mais Próximo", command=self.find_closest_pair)
        self.button.pack()
        self.reset_button = tk.Button(self.master, text="Resetar", command=self.reset_canvas)
        self.reset_button.pack()
    
    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        
        if len(self.points) == 1:  # Verificar se é o primeiro ponto
            # Carregar a imagem para o primeiro ponto
            image = Image.open(r"DC_CARTEIRO_G25\assets\carteiro.png")
            image = image.resize((40, 40), Image.ANTIALIAS)
            self.point_image = ImageTk.PhotoImage(image)
            
            # Substituir o primeiro ponto pela imagem no canvas
            self.canvas.create_image(x-10, y-10, anchor="nw", image=self.point_image, tags="point")
        else:
            point_item = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black", tags="point")
        
    def find_closest_pair(self):
        if len(self.points) < 2:
            print("Insira pelo menos 2 pontos.")
            return
        
        principal = self.points[0]  # Definindo o primeiro ponto como o ponto principal
        
        if self.line_item is not None:
            self.canvas.delete(self.line_item)  # Excluir a linha vermelha anterior
        
        if self.circle_item is not None:
            self.canvas.delete(self.circle_item)  # Excluir o círculo vermelho anterior
        
        closest_pair = self.closest_pair_divide_and_conquer(self.points[1:], principal)
        
        if closest_pair is not None:
            self.line_item = self.canvas.create_line(principal[0], principal[1], closest_pair[0][0], closest_pair[0][1], fill="red", width=2)
            self.canvas.create_oval(principal[0]-3, principal[1]-3, principal[0]+3, principal[1]+3, outline="red")
            self.circle_item = self.canvas.create_oval(closest_pair[0][0]-3, closest_pair[0][1]-3, closest_pair[0][0]+3, closest_pair[0][1]+3, outline="red")
        else:
            print("Nenhum ponto mais próximo encontrado.")
    
    def closest_pair_divide_and_conquer(self, points, principal):
        points_sorted_by_x = sorted(points, key=lambda point: point[0])
        points_sorted_by_y = sorted(points, key=lambda point: point[1])
        return self.closest_pair_recursion(points_sorted_by_x, points_sorted_by_y, principal)
    
    def closest_pair_recursion(self, points_sorted_by_x, points_sorted_by_y, principal):
        n = len(points_sorted_by_x)

        if n <= 3:
            return self.brute_force_closest_pair(points_sorted_by_x, principal)

        mid = n // 2
        mid_point = points_sorted_by_x[mid]

        left_points_sorted_by_x = points_sorted_by_x[:mid]
        right_points_sorted_by_x = points_sorted_by_x[mid:]

        left_points_sorted_by_y = []
        right_points_sorted_by_y = []

        for point in points_sorted_by_y:
            if point in left_points_sorted_by_x:
                left_points_sorted_by_y.append(point)
            else:
                right_points_sorted_by_y.append(point)

        closest_pair_left = self.closest_pair_recursion(left_points_sorted_by_x, left_points_sorted_by_y, principal)
        closest_pair_right = self.closest_pair_recursion(right_points_sorted_by_x, right_points_sorted_by_y, principal)

        delta = min(self.distance(principal, closest_pair_left[0]), self.distance(principal, closest_pair_right[0]))
        closest_split_pair = self.closest_split_pair(points_sorted_by_x, points_sorted_by_y, delta, principal)

        if closest_split_pair:
            return closest_split_pair
        elif self.distance(principal, closest_pair_left[0]) < self.distance(principal, closest_pair_right[0]):
            return closest_pair_left
        else:
            return closest_pair_right
    
    def brute_force_closest_pair(self, points, principal):
        min_distance = float("inf")
        closest_pair = None

        for i in range(len(points)):
            dist = self.distance(points[i], principal)
            if dist < min_distance:
                min_distance = dist
                closest_pair = (points[i], principal)

        return closest_pair
    
    def closest_split_pair(self, points_sorted_by_x, points_sorted_by_y, delta, principal):
        n = len(points_sorted_by_x)
        mid_point = points_sorted_by_x[n // 2]

        s_y = [point for point in points_sorted_by_y if mid_point[0] - delta <= point[0] <= mid_point[0] + delta]

        min_distance = delta
        closest_pair = None

        for i in range(len(s_y)):
            dist = self.distance(principal, s_y[i])
            if dist < min_distance:
                min_distance = dist
                closest_pair = (s_y[i], principal)

        return closest_pair
    
    def distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def reset_canvas(self):
        if self.line_item is not None:
            self.canvas.delete(self.line_item)  # Excluir a linha vermelha, se existir
            self.line_item = None
        
        if self.circle_item is not None:
            self.canvas.delete(self.circle_item)  # Excluir o círculo vermelho, se existir
            self.circle_item = None
        
        # Excluir apenas os itens que representam os pontos
        for item in self.canvas.find_withtag("point"):
            self.canvas.delete(item)
      
        self.points = []
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ClosestPairGUI(root)
    root.mainloop()
