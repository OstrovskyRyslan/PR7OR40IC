import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import pickle
import os
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пінг-понг")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_SPEED = 5
left_paddle = pygame.Rect(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
BALL_RADIUS = 15
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 5
ball_speed_y = 5
left_score = 0
right_score = 0
font = pygame.font.Font(None, 74)
game_folder = r"C:\Users\Ruslan Ostrovsky\Desktop\igra z zberejeniam\мои игры"
if not os.path.exists(game_folder):
    os.makedirs(game_folder)
save_file_path = os.path.join(game_folder, 'pingpong_save.pkl')
def save_game():
    game_data = {
        "score": (left_score, right_score),
        "paddle_positions": (left_paddle.y, right_paddle.y),
        "ball_position": (ball.x, ball.y),
        "ball_speed": (ball_speed_x, ball_speed_y)
    }
    with open(save_file_path, 'wb') as file:
        pickle.dump(game_data, file)
        print(f"Игра сохранена в: {save_file_path}")
def load_game(filename):
    global left_score, right_score, left_paddle, right_paddle, ball, ball_speed_x, ball_speed_y
    with open(filename, 'rb') as file:
        game_data = pickle.load(file)
        score = game_data["score"]
        if isinstance(score, tuple) and len(score) == 2:
            left_score, right_score = score
        left_paddle.y, right_paddle.y = game_data["paddle_positions"]
        ball_position = game_data["ball_position"]
        ball_speed_x, ball_speed_y = game_data["ball_speed"]
        ball = pygame.Rect(ball_position[0], ball_position[1], BALL_RADIUS * 2, BALL_RADIUS * 2)
        print(f"Игра загружена из файла: {filename}")
def start_game():
    global left_score, right_score, left_paddle, right_paddle, ball_speed_x, ball_speed_y, ball
    ball_speed_x = 5
    ball_speed_y = 5
    ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1
        if ball.left <= 0:
            right_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1
        if ball.right >= WIDTH:
            left_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x *= -1
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 20))
        screen.blit(right_text, (WIDTH * 3 // 4, 20))
        pygame.display.flip()
        clock.tick(60)
        if keys[pygame.K_p]:
            show_menu()
def show_menu():
    global left_score, right_score, left_paddle, right_paddle, ball, ball_speed_x, ball_speed_y
    menu_running = True
    selected_item = 0
    menu_items = ["Почати гру", "Завантажити файл", "Зберегти гру", "Вийти"]
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        start_game()
                    elif selected_item == 1:
                        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
                        if file_path:
                            load_game(file_path)
                    elif selected_item == 2:
                        save_game()
                    elif selected_item == 3:
                        menu_running = False
        screen.fill(BLACK)
        for i, item in enumerate(menu_items):
            color = (255, 255, 255) if i == selected_item else (100, 100, 100)
            text_surface = font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            screen.blit(text_surface, text_rect)
        pygame.display.flip()
show_menu()
pygame.quit()
sys.exit()
