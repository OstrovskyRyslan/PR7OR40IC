import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import pickle
import pingpong 
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Меню гри")
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)
menu_items = ["Почати гру", "Завантажити файл", "Зберегти гру", "Вийти"]
selected_item = 0
def get_file():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename()  
    return file_path
def save_game(game_data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(game_data, file)
        print(f"Гра збережена в файл: {filename}")
def load_game(filename):
    with open(filename, 'rb') as file:
        game_data = pickle.load(file)
        print(f"Гра завантажена з файлу: {filename}")
        return game_data
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(menu_items)
            if event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(menu_items)
            if event.key == pygame.K_RETURN:
                if selected_item == 0:
                    print("Гра запускається...")
                    pingpong.start_game()  
                    running = False 
                elif selected_item == 1:
                    file_path = get_file()
                    if file_path:
                        game_data = load_game(file_path)
                elif selected_item == 2:
                    file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
                    if file_path:
                        game_data = {
                            "score": 10,
                            "paddle_positions": (100, 500),
                            "ball_position": (400, 300),
                            "ball_direction": (1, 1)
                        }
                        save_game(game_data, file_path)
                elif selected_item == 3:
                    running = False
    screen.fill((0, 0, 0))
    for i, item in enumerate(menu_items):
        color = (255, 255, 255) if i == selected_item else (100, 100, 100)
        text_surface = small_font.render(item, True, color)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + i * 60))
        screen.blit(text_surface, text_rect)
    pygame.display.flip()
pygame.quit()
sys.exit()
