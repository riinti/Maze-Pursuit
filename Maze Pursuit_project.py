import turtle
import random
from collections import deque

# 게임 종료 여부 설정
game_running = True
score = 0

def generate_maze(size): # Prim's Algorithm으로 미로 생성 함수
    maze = [[1 for _ in range(size)] for _ in range(size)]
    
    def get_neighbors(x, y):
        # 현재 위치에서 상하좌우 이웃 셀을 구함
        neighbors = []
        if x > 1: neighbors.append((x - 2, y))
        if x < size - 2: neighbors.append((x + 2, y))
        if y > 1: neighbors.append((x, y - 2))
        if y < size - 2: neighbors.append((x, y + 2))
        return neighbors

    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    walls = [(start_x + dx, start_y + dy) for dx, dy in [(0, 2), (2, 0)] if start_x + dx < size and start_y + dy < size]

    # 미로를 생성하면서 랜덤하게 벽을 제거하여 길을 만듦
    while walls:
        x, y = random.choice(walls)
        walls.remove((x, y))

        neighbors = get_neighbors(x, y)
        open_neighbors = [(nx, ny) for nx, ny in neighbors if maze[ny][nx] == 0]

        if open_neighbors:
            nx, ny = random.choice(open_neighbors)
            if x == nx:
                maze[(y + ny) // 2][x] = 0
            else:
                maze[y][(x + nx) // 2] = 0
            maze[y][x] = 0

            for neighbor in get_neighbors(x, y):
                if maze[neighbor[1]][neighbor[0]] == 1:
                    walls.append(neighbor)

    maze[0][1] = 'S'  # 시작점 설정
    maze[size - 1][size - 2] = 'E'  # 종료점 설정
    return maze

# 미로 사이즈 설정
maze_size = 25
maze = generate_maze(maze_size)

# 화면 설정
screen = turtle.Screen()
screen.title("Game Start Screen")
screen.setup(width=800, height=800)
screen.bgcolor("black")
screen.tracer(0) 

# 텍스트 표시 설정
start_text = turtle.Turtle()
start_text.hideturtle()


def display_text_with_border(x, y, message): # 시작 화면 글씨 테두리 표시 함수
    start_text.color("black")
    start_text.penup()
    start_text.goto(0, 0)
    
    # 테두리 그리기
    offsets = [(0, 2), (2, 0), (0, -2), (-2, 0), (2, 2), (-2, -2), (2, -2), (-2, 2)]  # 8방향
    for dx, dy in offsets:
        start_text.goto(0 + dx, 0 + dy)
        start_text.write(message, align="center", font=("Arial", 24, "bold"))
    # 본래 텍스트 그리기
    start_text.color("white")
    start_text.penup()
    start_text.goto(0, 0)
    start_text.write(message, align="center", font=("Arial", 24, "bold"))


# 미로와 게임 캐릭터 관련 설정
t = turtle.Turtle()
t.speed('fastest')  # 터틀 이동 속도를 빠르게 설정
t.hideturtle()

# 플레이어 생성
player = turtle.Turtle()
player.shape('circle')
player.color('blue')
player.penup()

# 적 캐릭터 리스트 생성
enemies = []

# 플레이어가 방문한 칸을 추적하는 세트
visited_cells = set()

# 점수 표시를 위한 터틀 설정
score_turtle = turtle.Turtle()
score_turtle.hideturtle()
score_turtle.penup()
score_turtle.goto(-maze_size * 10, maze_size * 10 + 20)
score_turtle.color("blue")
score_turtle.write(f"Score: {score}", align="left", font=("Arial", 16, "bold"))


def start_game(): # 게임 시작 함수
    global game_running
    if not game_running: # 게임이 종료된 경우 실행하지 않음
        return
    
    screen.bgcolor("white")
    place_player()  # 플레이어 위치 설정
    place_enemies() # 적 위치 설정
    key_ctrl()  # 키보드 컨트롤 설정
    start_text.clear()  # 시작 텍스트 지움
    drawmaze(maze)  # 미로 그리기


def drawmaze(maze): # 미로 그리기 함수
    if not game_running:  # 게임이 종료된 경우 실행하지 않음
        return
    
    t.penup()
    start_x, start_y = -maze_size * 10, maze_size * 10
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            t.goto(start_x + x * 20, start_y - y * 20)
            if maze[y][x] == 1:
                # 벽 그리기
                t.pendown()
                t.fillcolor('black')
                t.begin_fill()
                for _ in range(4):
                    t.forward(20)
                    t.right(90)
                t.end_fill()
                t.penup()
            elif maze[y][x] == 'S':
                # 시작점 표시
                t.pendown()
                t.fillcolor('green')
                t.begin_fill()
                for _ in range(4):
                    t.forward(20)
                    t.right(90)
                t.end_fill()
                t.penup()
            elif maze[y][x] == 'E':
                # 종료점 표시
                t.pendown()
                t.fillcolor('red')
                t.begin_fill()
                for _ in range(4):
                    t.forward(20)
                    t.right(90)
                t.end_fill()
                t.penup()
    screen.update()  

def place_player(): # 플레이어 위치 설정 함수
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 'S':
                # 시작점 위치로 플레이어 이동
                start_x = -maze_size * 10 + x * 20 + 10
                start_y = maze_size * 10 - y * 20 - 10
                player.goto(start_x, start_y)
                visited_cells.add((x, y))
                return

drawmaze(maze)
screen.tracer(1)  # 화면 갱신


def update_score(): # 점수 업데이트 함수
    global score
    score += 1
    score_turtle.clear()
    score_turtle.write(f"Score: {score}", align="left", font=("Arial", 16, "bold"))



def find_path(start_x, start_y, goal_x, goal_y): # BFS로 최단 경로를 찾는 함수
    queue = deque([(start_x, start_y)])
    visited = set()
    visited.add((start_x, start_y))
    parent_map = {}

    while queue:
        x, y = queue.popleft()
        
        # 플레이어 위치에 도달하면 경로 반환
        if (x, y) == (goal_x, goal_y):
            path = []
            while (x, y) != (start_x, start_y):
                path.append((x, y))
                x, y = parent_map[(x, y)]
            path.reverse()
            return path

        # 상하좌우 이동 가능한지 체크
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] != 1 and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent_map[(nx, ny)] = (x, y)

    return []  # 플레이어에게 도달 불가능할 경우 빈 리스트 반환
    

def move_enemies(): # 적 이동 함수
    global game_running
    if not game_running:  # 게임이 종료된 경우 실행하지 않음
        return
    
    for enemy in enemies:
        player_x, player_y = player.pos()
        enemy_x, enemy_y = enemy.pos()
        
        # 적 위치와 플레이어 위치를 비교해 이동
        enemy_grid_x = int((enemy_x + maze_size * 10) // 20)
        enemy_grid_y = int((maze_size * 10 - enemy_y) // 20)
        player_grid_x = int((player_x + maze_size * 10) // 20)
        player_grid_y = int((maze_size * 10 - player_y) // 20)
        
        # 최단 경로 불러오기
        path = find_path(enemy_grid_x, enemy_grid_y, player_grid_x, player_grid_y)
        
        # 경로가 있다면 다음 좌표로 이동
        if path:
            next_x, next_y = path[0]
            new_enemy_x = -maze_size * 10 + next_x * 20 + 10
            new_enemy_y = maze_size * 10 - next_y * 20 - 10
            enemy.goto(new_enemy_x, new_enemy_y)
                
        # 게임 오버 조건 설정
        if enemy.distance(player) < 20:
            game_running = False
            print("게임 오버!")
            turtle.bye()
            return
    
    screen.ontimer(move_enemies, 500)  # 적의 이동 속도 설정


def place_enemies():# 적 캐릭터 생성 함수
    
    num_enemies = 5
     
    for _ in range(num_enemies):

        enemy = turtle.Turtle()
        enemy.shape('circle')
        enemy.color('red')
        enemy.penup()
        enemy.speed(0)  # 속도 설정
        
        while True: # 미로의 길인 셀 중 무작위 배치
            ex = random.randint(0, maze_size - 1)
            ey = random.randint(0, maze_size - 1)
            if maze[ey][ex] == 0 and (ex, ey) != (1, 1) and (ex, ey) != (maze_size - 2, maze_size - 1):
                break
        new_enemy_x = -maze_size * 10 + ex * 20 + 10
        new_enemy_y = maze_size * 10 - ey * 20 - 10
        enemy.goto(new_enemy_x, new_enemy_y)
        enemies.append(enemy)
    
    move_enemies()


def move_to_grid(x, y): # 플레이어가 이동할 위치 계산 함수
    new_x = -maze_size * 10 + x * 20 + 10
    new_y = maze_size * 10 - y * 20 - 10
    player.goto(new_x, new_y)
    if (x, y) not in visited_cells:
        visited_cells.add((x, y))
        update_score()


def move(dx, dy): # 플레이어 이동 함수
    if not game_running:
        return

    x, y = player.pos()
    grid_x = int((x + maze_size * 10) // 20)
    grid_y = int((maze_size * 10 - y) // 20)
    new_x, new_y = grid_x + dx, grid_y + dy
    if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] != 1:
        move_to_grid(new_x, new_y)
        check_win()


def check_win(): # 탈출조건 확인 함수
    global game_running
    x, y = player.pos()
    grid_x = int((x + maze_size * 10) // 20)
    grid_y = int((maze_size * 10 - y) // 20)
    if maze[grid_y][grid_x] == 'E':
        game_running = False
        print("미로 탈출 성공!")
        turtle.bye()


def key_ctrl(): # 키보드 이벤트 설정 함수
    screen.onkey(lambda: move(0, -1), "w")
    screen.onkey(lambda: move(0, 1), "s")
    screen.onkey(lambda: move(-1, 0), "a")
    screen.onkey(lambda: move(1, 0), "d")
    screen.onkey(lambda: move(0, -1), "Up")
    screen.onkey(lambda: move(0, 1), "Down")
    screen.onkey(lambda: move(-1, 0), "Left")
    screen.onkey(lambda: move(1, 0), "Right") 

screen.listen()
screen.onkey(start_game, "Return")  # Enter 키로 게임 시작

# 시작 화면 표시
display_text_with_border(0, 0, "Press 'Enter' to Start")

# 게임 실행
turtle.mainloop()
