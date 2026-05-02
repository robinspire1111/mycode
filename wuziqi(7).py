import tkinter as tk
from tkinter import messagebox, font
import numpy as np
import threading
import time
import random
import math

# ---------- 音频引擎 ----------
SOUND_ENABLED = False
try:
    import sounddevice as sd
    SOUND_ENABLED = True
    AUDIO_BACKEND = "sd"
except ImportError:
    try:
        import winsound
        SOUND_ENABLED = True
        AUDIO_BACKEND = "winsound"
    except ImportError:
        SOUND_ENABLED = False
        AUDIO_BACKEND = None

class SoundPlayer:
    @staticmethod
    def play(freq, duration=0.12, volume=0.4):
        if not SOUND_ENABLED:
            return
        try:
            if AUDIO_BACKEND == "sd":
                def _play():
                    sr = 44100
                    t = np.linspace(0, duration, int(sr * duration))
                    envelope = 1 - np.linspace(0, 0.8, len(t))
                    wave = volume * envelope * np.sin(2 * np.pi * freq * t)
                    sd.play(wave, sr)
                    sd.wait()
                threading.Thread(target=_play, daemon=True).start()
            elif AUDIO_BACKEND == "winsound":
                winsound.Beep(int(freq), int(duration * 1000))
        except:
            pass

    @staticmethod
    def place(is_ai):
        if is_ai:
            SoundPlayer.play(880, 0.1, 0.5)
            SoundPlayer.play(1100, 0.08, 0.3)
        else:
            SoundPlayer.play(440, 0.12, 0.5)
            SoundPlayer.play(660, 0.1, 0.3)

    @staticmethod
    def win():
        for f in [523, 659, 784, 1046]:
            SoundPlayer.play(f, 0.15, 0.5)
            time.sleep(0.05)

    @staticmethod
    def error():
        SoundPlayer.play(220, 0.2, 0.4)

    @staticmethod
    def undo():
        SoundPlayer.play(660, 0.1, 0.3)

    @staticmethod
    def hint():
        SoundPlayer.play(880, 0.05, 0.2)
        SoundPlayer.play(1046, 0.05, 0.2)

    @staticmethod
    def button_hover():
        SoundPlayer.play(880, 0.03, 0.1)

    @staticmethod
    def combo():
        SoundPlayer.play(1046, 0.1, 0.6)

# ---------- 游戏配置 ----------
BOARD_SIZE = 15
DEFAULT_CELL_SIZE = 36
DEFAULT_PADDING = 45
DEFAULT_WIDTH = DEFAULT_PADDING * 2 + DEFAULT_CELL_SIZE * (BOARD_SIZE - 1)
DEFAULT_HEIGHT = DEFAULT_WIDTH
DEFAULT_WINDOW_WIDTH = DEFAULT_WIDTH + 260
DEFAULT_WINDOW_HEIGHT = DEFAULT_HEIGHT + 80

BG_MAIN = "#2c3e50"
BG_PANEL = "#ecf0f1"
BG_BOARD = "#DEB887"
LINE_COLOR = "#5D3A1A"
STAR_COLOR = "#C97E3A"

DIFFICULTY = {
    "easy": {"depth": 1, "defense_weight": 0.6, "random_rate": 0.3, "name": "简单"},
    "medium": {"depth": 2, "defense_weight": 0.9, "random_rate": 0.1, "name": "中等"},
    "hard": {"depth": 3, "defense_weight": 1.0, "random_rate": 0.0, "name": "困难"}
}

# ---------- 主菜单 ----------
class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        self.root.configure(bg=BG_MAIN)

        self.canvas = tk.Canvas(self.root, bg=BG_MAIN, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.draw_gradient_bg()

        title_font = font.Font(family="华文楷书", size=48, weight="bold")
        self.canvas.create_text(400, 150, text="五子棋", font=title_font, fill="#F7D44A", anchor="center")

        btn_font = font.Font(family="微软雅黑", size=16, weight="bold")
        btn_width = 200
        btn_height = 50
        cx = 400

        self.create_rounded_btn(cx - btn_width//2, 260, btn_width, btn_height, "#27ae60", "简单", lambda: self.start_game("easy"))
        self.create_rounded_btn(cx - btn_width//2, 340, btn_width, btn_height, "#f39c12", "中等", lambda: self.start_game("medium"))
        self.create_rounded_btn(cx - btn_width//2, 420, btn_width, btn_height, "#e74c3c", "困难", lambda: self.start_game("hard"))

        self.canvas.create_text(400, 550, text="人机对战 · 深度启发式AI", fill="#BDC3C7", font=("微软雅黑", 10))

    def draw_gradient_bg(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if w < 10:
            w, h = 800, 600
        for i in range(0, h, 2):
            ratio = i / h
            color = self.interpolate(BG_MAIN, "#1a2632", ratio)
            self.canvas.create_rectangle(0, i, w, i+2, fill=color, outline="")

    def interpolate(self, c1, c2, t):
        c1 = tuple(int(c1[i:i+2],16) for i in (1,3,5))
        c2 = tuple(int(c2[i:i+2],16) for i in (1,3,5))
        r = int(c1[0] + (c2[0]-c1[0])*t)
        g = int(c1[1] + (c2[1]-c1[1])*t)
        b = int(c1[2] + (c2[2]-c1[2])*t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def create_rounded_btn(self, x, y, w, h, color, text, cmd):
        r = 15
        points = [x+r, y, x+w-r, y, x+w, y, x+w, y+r, x+w, y+h-r, x+w, y+h, x+w-r, y+h, x+r, y+h, x, y+h, x, y+h-r, x, y+r, x, y]
        btn = self.canvas.create_polygon(points, smooth=True, fill=color, outline="white", width=2)
        txt = self.canvas.create_text(x+w/2, y+h/2, text=text, font=("微软雅黑",16,"bold"), fill="white", anchor="center")
        def click(e): cmd()
        self.canvas.tag_bind(btn, "<Button-1>", click)
        self.canvas.tag_bind(txt, "<Button-1>", click)
        def on_enter(e): 
            self.canvas.itemconfig(btn, fill=self.lighten(color))
            SoundPlayer.button_hover()
        def on_leave(e): self.canvas.itemconfig(btn, fill=color)
        self.canvas.tag_bind(btn, "<Enter>", on_enter)
        self.canvas.tag_bind(txt, "<Enter>", on_enter)
        self.canvas.tag_bind(btn, "<Leave>", on_leave)
        self.canvas.tag_bind(txt, "<Leave>", on_leave)
        return btn

    def lighten(self, color):
        c = tuple(int(color[i:i+2],16) for i in (1,3,5))
        c = tuple(min(255, int(v*1.2)) for v in c)
        return f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}"

    def start_game(self, diff):
        self.root.destroy()
        new_root = tk.Tk()
        GomokuGame(new_root, diff)
        new_root.mainloop()

# ---------- 游戏主类 ----------
class GomokuGame:
    def __init__(self, root, difficulty="medium"):
        self.root = root
        self.root.title(f"五子棋 - {DIFFICULTY[difficulty]['name']}难度")
        self.root.configure(bg=BG_PANEL)
        self.root.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        self.root.minsize(700, 700)

        self.cell_size = DEFAULT_CELL_SIZE
        self.padding = DEFAULT_PADDING
        self.board_width = self.padding*2 + self.cell_size*(BOARD_SIZE-1)
        self.board_height = self.board_width

        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int8)
        self.current_turn = 1
        self.game_over = False
        self.last_move = None
        self.hover_pos = None
        self.ai_thinking = False
        self.difficulty = difficulty
        self.depth = DIFFICULTY[difficulty]["depth"]
        self.defense_weight = DIFFICULTY[difficulty]["defense_weight"]
        self.random_rate = DIFFICULTY[difficulty]["random_rate"]
        self.move_history = []
        self.player_score = 0
        self.ai_score = 0
        self.combo_count = 0
        self.flash_after = None  # 用于存储闪烁定时器

        self.create_widgets()
        self.bind_events()
        self.reset_game()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg=BG_PANEL)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas_frame = tk.Frame(self.main_frame, bg="#C7A47B", relief=tk.RAISED, bd=3)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg=BG_BOARD, highlightthickness=0,
                                cursor="cross", width=self.board_width, height=self.board_height)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.right_frame = tk.Frame(self.main_frame, bg=BG_PANEL, width=240)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15,0))
        self.right_frame.pack_propagate(False)

        diff_label = tk.Label(self.right_frame, text=f"难度: {DIFFICULTY[self.difficulty]['name']}",
                              font=("微软雅黑",12,"bold"), bg=BG_PANEL, fg="#e67e22")
        diff_label.pack(pady=(0,10))

        self.score_frame = tk.Frame(self.right_frame, bg=BG_PANEL)
        self.score_frame.pack(pady=10)
        self.player_score_label = tk.Label(self.score_frame, text="玩家: 0", font=("微软雅黑",10), bg=BG_PANEL, fg="#2c3e50")
        self.player_score_label.pack(side=tk.LEFT, padx=5)
        self.ai_score_label = tk.Label(self.score_frame, text="AI: 0", font=("微软雅黑",10), bg=BG_PANEL, fg="#e67e22")
        self.ai_score_label.pack(side=tk.LEFT, padx=5)

        self.status_var = tk.StringVar()
        self.status_var.set("玩家回合")
        status = tk.Label(self.right_frame, textvariable=self.status_var,
                          font=("微软雅黑",14,"bold"), bg=BG_PANEL, fg="#2c3e50")
        status.pack(pady=5)

        self.turn_canvas = tk.Canvas(self.right_frame, width=60, height=60, bg=BG_PANEL, highlightthickness=0)
        self.turn_canvas.pack(pady=5)

        btn_base = {"font":("微软雅黑",11),"fg":"white","bd":0,"padx":20,"pady":8,"cursor":"hand2"}
        tk.Button(self.right_frame, text="🔄 新游戏", command=self.reset_game,
                  bg="#3498db", activebackground="#2980b9", **btn_base).pack(pady=5)
        tk.Button(self.right_frame, text="↩️ 悔棋", command=self.undo_move,
                  bg="#f1c40f", activebackground="#e67e22", **btn_base).pack(pady=5)
        tk.Button(self.right_frame, text="💡 提示", command=self.show_hint,
                  bg="#9b59b6", activebackground="#8e44ad", **btn_base).pack(pady=5)
        tk.Button(self.right_frame, text="🏠 主菜单", command=self.back_to_menu,
                  bg="#95a5a6", activebackground="#7f8c8d", **btn_base).pack(pady=5)

        self.combo_label = tk.Label(self.right_frame, text="", font=("微软雅黑",9), bg=BG_PANEL, fg="#e67e22")
        self.combo_label.pack(pady=5)

        info = tk.Label(self.right_frame, text="五子连珠获胜\n鼠标点击交叉点落子",
                        font=("微软雅黑",9), bg=BG_PANEL, fg="#7f8c8d", justify=tk.LEFT)
        info.pack(side=tk.BOTTOM, pady=20)

        self.draw_board()
        self.draw_pieces()

    def bind_events(self):
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Leave>", self.on_mouse_leave)
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        w, h = event.width, event.height
        board_side = min(w, h) - 20
        self.cell_size = board_side / (BOARD_SIZE - 1)
        self.padding = self.cell_size
        self.board_width = self.padding*2 + self.cell_size*(BOARD_SIZE-1)
        self.board_height = self.board_width
        self.redraw_all()

    def redraw_all(self):
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        self.canvas.delete("board")
        for i in range(BOARD_SIZE):
            start = self.padding
            end = self.padding + self.cell_size*(BOARD_SIZE-1)
            y = self.padding + i*self.cell_size
            self.canvas.create_line(start, y, end, y, fill=LINE_COLOR, width=2, tags="board")
            self.canvas.create_line(y, start, y, end, fill=LINE_COLOR, width=2, tags="board")
        stars = [(3,3),(11,3),(7,7),(3,11),(11,11)]
        r = max(3, int(self.cell_size*0.12))
        for x,y in stars:
            cx = self.padding + x*self.cell_size
            cy = self.padding + y*self.cell_size
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=STAR_COLOR, outline=STAR_COLOR, tags="board")

    def draw_pieces(self):
        self.canvas.delete("piece")
        self.canvas.delete("marker")
        self.canvas.delete("hover")
        self.piece_radius = max(6, int(self.cell_size*0.42))

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 1:
                    self._draw_piece(i, j, "#2c3e50", "#4a627a")
                elif self.board[i][j] == 2:
                    self._draw_piece(i, j, "#e67e22", "#f39c12")

        if self.last_move:
            x,y = self.last_move
            cx = self.padding + x*self.cell_size
            cy = self.padding + y*self.cell_size
            r = self.piece_radius + 6
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline="#ffaa44", width=3, tags="marker")

        if self.hover_pos and not self.game_over and self.current_turn==1:
            x,y = self.hover_pos
            if self.board[x][y]==0:
                cx = self.padding + x*self.cell_size
                cy = self.padding + y*self.cell_size
                r = self.piece_radius-2
                self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#88ff88", outline="#44aa44", width=2, tags="hover", stipple="gray50")

    def _draw_piece(self, x, y, dark_color, light_color):
        cx = self.padding + x*self.cell_size
        cy = self.padding + y*self.cell_size
        r = self.piece_radius
        # 阴影
        self.canvas.create_oval(cx-r+2, cy-r+2, cx+r+2, cy+r+2, fill="#a0a0a0", outline="", tags="piece")
        # 主体
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=dark_color, outline="white", width=1.5, tags="piece")
        # 径向渐变模拟
        steps = 5
        for i in range(1, steps):
            ratio = i / steps
            rad = r - i * (r//steps)
            if rad < 2: continue
            alpha = 1 - ratio * 0.8
            color = self._blend(dark_color, light_color, alpha)
            self.canvas.create_oval(cx-rad, cy-rad, cx+rad, cy+rad, outline=color, width=1, tags="piece")
        # 高光
        hr = r//3
        self.canvas.create_oval(cx-hr, cy-hr, cx+hr//2, cy+hr//2, fill="white", outline="", tags="piece")

    def _blend(self, c1, c2, t):
        c1 = tuple(int(c1[i:i+2],16) for i in (1,3,5))
        c2 = tuple(int(c2[i:i+2],16) for i in (1,3,5))
        r = int(c1[0] + (c2[0]-c1[0])*t)
        g = int(c1[1] + (c2[1]-c1[1])*t)
        b = int(c1[2] + (c2[2]-c1[2])*t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def on_mouse_move(self, event):
        if self.game_over or self.current_turn!=1 or self.ai_thinking:
            return
        pos = self._get_board_pos(event.x, event.y)
        if pos:
            x,y = pos
            if self.board[x][y]==0:
                self.hover_pos = (x,y)
            else:
                self.hover_pos = None
        else:
            self.hover_pos = None
        self.draw_pieces()

    def on_mouse_leave(self, event):
        self.hover_pos = None
        self.draw_pieces()

    def on_click(self, event):
        if self.game_over or self.current_turn!=1 or self.ai_thinking:
            return
        pos = self._get_board_pos(event.x, event.y)
        if pos:
            x,y = pos
            if self.board[x][y]==0:
                self.make_move(x,y)

    def _get_board_pos(self, mx, my):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cx = self.padding + i*self.cell_size
                cy = self.padding + j*self.cell_size
                # 使用更精确的阈值
                if abs(mx-cx) <= self.cell_size*0.45 and abs(my-cy) <= self.cell_size*0.45:
                    return (i,j)
        return None

    def make_move(self, x, y, is_ai=False):
        if self.board[x][y]!=0 or self.game_over:
            return False

        player = 2 if is_ai else 1
        self.board[x][y] = player
        self.move_history.append((x,y,player))
        self.last_move = (x,y)
        SoundPlayer.place(is_ai)
        self.draw_pieces()
        self._add_fancy_effect(x, y, is_ai)

        combo = self._check_combo(x, y)
        if combo >= 4:
            self.combo_count += 1
            self.combo_label.config(text=f"连珠警告! {combo}连!")
            SoundPlayer.combo()
            self.root.after(1500, lambda: self.combo_label.config(text=""))

        win = self._check_win(x, y)
        if win:
            self.game_over = True
            if is_ai:
                self.ai_score += 1
                self.ai_score_label.config(text=f"AI: {self.ai_score}")
            else:
                self.player_score += 1
                self.player_score_label.config(text=f"玩家: {self.player_score}")
            self.status_var.set(f"🏆 {'AI' if is_ai else '玩家'}胜利！")
            SoundPlayer.win()
            self._victory_effect(x, y, is_ai)
            messagebox.showinfo("游戏结束", f"{'AI' if is_ai else '玩家'}胜利！")
            return True

        if np.count_nonzero(self.board) == BOARD_SIZE*BOARD_SIZE:
            self.game_over = True
            self.status_var.set("平局！")
            messagebox.showinfo("游戏结束", "平局！")
            return True

        self.current_turn = 1 if is_ai else 2
        self.update_turn_indicator()

        if not self.game_over:
            if self.current_turn == 1:
                self.status_var.set("玩家回合")
            else:
                self.status_var.set("AI思考中...")
                self.root.after(200, self.ai_move)
        return True

    def _add_fancy_effect(self, x, y, is_ai):
        cx = self.padding + x*self.cell_size
        cy = self.padding + y*self.cell_size
        # 扩散圆环
        rings = []
        for i in range(3):
            ring = self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, outline="gold", width=2, tags="effect")
            rings.append(ring)
            self.root.after(i*50, lambda r=ring, step=i: self._expand_ring(r, step))
        # 粒子效果
        particles = []
        for _ in range(12):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(2, 6)
            color = "#ffaa44" if is_ai else "#88aaff"
            part = self.canvas.create_oval(cx-2, cy-2, cx+2, cy+2, fill=color, outline="", tags="effect")
            particles.append((part, angle, speed, cx, cy))
        def animate():
            still_alive = False
            for i, (part, angle, speed, ox, oy) in enumerate(particles):
                if self.canvas.find_withtag(part):
                    still_alive = True
                    coords = self.canvas.coords(part)
                    if coords:
                        x1,y1,x2,y2 = coords
                        cx_new = (x1+x2)/2
                        cy_new = (y1+y2)/2
                        dx = math.cos(angle) * speed
                        dy = math.sin(angle) * speed
                        self.canvas.move(part, dx, dy)
                        w = (x2-x1)
                        if w > 1:
                            self.canvas.coords(part, cx_new+dx-w*0.05, cy_new+dy-w*0.05,
                                               cx_new+dx+w*0.05, cy_new+dy+w*0.05)
                        else:
                            self.canvas.delete(part)
                    else:
                        self.canvas.delete(part)
            if still_alive:
                self.root.after(30, animate)
        animate()

    def _expand_ring(self, ring, step):
        for i in range(1, 5):
            def expand(r):
                coords = self.canvas.coords(r)
                if coords:
                    x1,y1,x2,y2 = coords
                    cx = (x1+x2)/2
                    cy = (y1+y2)/2
                    new_r = (x2-x1)/2 + 4
                    self.canvas.coords(r, cx-new_r, cy-new_r, cx+new_r, cy+new_r)
            self.root.after(i*30, lambda r=ring: expand(r))
        self.root.after(300, lambda: self.canvas.delete(ring))

    def _victory_effect(self, x, y, is_ai):
        # 闪烁棋盘，最后恢复原色
        original_bg = BG_BOARD
        for i in range(3):
            self.root.after(150*i, lambda: self.canvas.config(bg="#ffd966"))
            self.root.after(150*(i+1), lambda: self.canvas.config(bg=original_bg))
        # 棋子跳动效果
        cx = self.padding + x*self.cell_size
        cy = self.padding + y*self.cell_size
        r = self.piece_radius
        def bounce():
            self.canvas.move("piece", 0, -3)
            self.root.after(50, lambda: self.canvas.move("piece", 0, 3))
        self.root.after(100, bounce)

    def _check_combo(self, x, y):
        player = self.board[x][y]
        if player == 0:
            return 0
        dirs = [(1,0),(0,1),(1,1),(1,-1)]
        max_len = 0
        for dx,dy in dirs:
            cnt = 1
            for step in range(1,6):
                nx, ny = x+dx*step, y+dy*step
                if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and self.board[nx][ny]==player:
                    cnt+=1
                else:
                    break
            for step in range(1,6):
                nx, ny = x-dx*step, y-dy*step
                if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and self.board[nx][ny]==player:
                    cnt+=1
                else:
                    break
            max_len = max(max_len, cnt)
        return max_len

    def _check_win(self, x, y):
        player = self.board[x][y]
        if player==0: return False
        dirs = [(1,0),(0,1),(1,1),(1,-1)]
        for dx,dy in dirs:
            cnt = 1
            for step in range(1,6):
                nx, ny = x+dx*step, y+dy*step
                if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and self.board[nx][ny]==player:
                    cnt+=1
                else:
                    break
            for step in range(1,6):
                nx, ny = x-dx*step, y-dy*step
                if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE and self.board[nx][ny]==player:
                    cnt+=1
                else:
                    break
            if cnt>=5:
                return True
        return False

    def update_turn_indicator(self):
        self.turn_canvas.delete("all")
        if self.game_over:
            return
        if self.current_turn == 1:
            self.turn_canvas.create_oval(10,10,50,50, fill="#2c3e50", outline="white")
            self.turn_canvas.create_text(30,30, text="👤", fill="white", font=("Arial",20))
        else:
            self.turn_canvas.create_oval(10,10,50,50, fill="#e67e22", outline="white")
            self.turn_canvas.create_text(30,30, text="🤖", fill="white", font=("Arial",20))

    def ai_move(self):
        if self.game_over or self.current_turn!=2 or self.ai_thinking:
            return
        self.ai_thinking = True
        self.status_var.set("AI思考中...")
        def compute():
            time.sleep(0.2)
            move = self._get_best_move()
            self.root.after(0, lambda: self._execute_ai_move(move))
        threading.Thread(target=compute, daemon=True).start()

    def _execute_ai_move(self, move):
        self.ai_thinking = False
        if move and not self.game_over and self.current_turn==2:
            x,y = move
            self.make_move(x,y, is_ai=True)

    def _get_best_move(self):
        if self.difficulty == "easy" and random.random() < self.random_rate:
            empties = [(i,j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j]==0]
            if empties:
                return random.choice(empties)

        best_score = -1
        best_move = None
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j]==0:
                    score = self._evaluate_position(i,j)
                    if score > best_score:
                        best_score = score
                        best_move = (i,j)
        return best_move

    def _evaluate_position(self, x, y):
        attack = self._evaluate_direction(x,y,2)
        defense = self._evaluate_direction(x,y,1) * self.defense_weight
        center = (BOARD_SIZE//2 - abs(x-BOARD_SIZE//2)) + (BOARD_SIZE//2 - abs(y-BOARD_SIZE//2))
        center_bonus = center * 2.5
        return attack + defense + center_bonus

    def _evaluate_direction(self, x, y, player):
        dirs = [(1,0),(0,1),(1,1),(1,-1)]
        total = 0
        for dx,dy in dirs:
            count = 1
            left_open, right_open = 0,0
            for step in range(1,6):
                nx, ny = x+dx*step, y+dy*step
                if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE:
                    if self.board[nx][ny]==player:
                        count+=1
                    else:
                        if self.board[nx][ny]==0:
                            right_open+=1
                        break
                else:
                    break
            for step in range(1,6):
                nx, ny = x-dx*step, y-dy*step
                if 0<=nx<BOARD_SIZE and 0<=ny<BOARD_SIZE:
                    if self.board[nx][ny]==player:
                        count+=1
                    else:
                        if self.board[nx][ny]==0:
                            left_open+=1
                        break
                else:
                    break
            total += self._score_pattern(count, left_open+right_open)
        return total

    def _score_pattern(self, length, openings):
        if length>=5:
            return 100000
        elif length==4:
            return 30000 if openings>=1 else 1000
        elif length==3:
            if openings>=2:
                return 5000
            elif openings>=1:
                return 300
            else:
                return 50
        elif length==2:
            if openings>=2:
                return 200
            elif openings>=1:
                return 20
            else:
                return 5
        else:
            return 1

    def undo_move(self):
        if self.game_over:
            SoundPlayer.error()
            return
        if len(self.move_history) == 0:
            SoundPlayer.error()
            return
        last = self.move_history.pop()
        x, y, _ = last
        self.board[x][y] = 0
        if self.move_history:
            last_x, last_y, _ = self.move_history[-1]
            self.last_move = (last_x, last_y)
        else:
            self.last_move = None
        self.current_turn = 1
        self.status_var.set("玩家回合")
        self.draw_pieces()
        SoundPlayer.undo()
        self.ai_thinking = False
        self.update_turn_indicator()

    def show_hint(self):
        if self.game_over or self.current_turn!=1 or self.ai_thinking:
            SoundPlayer.error()
            return
        SoundPlayer.hint()
        best = self._get_best_move()
        if best:
            x,y = best
            cx = self.padding + x*self.cell_size
            cy = self.padding + y*self.cell_size
            r = self.piece_radius + 6
            hint_id = self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline="cyan", width=3, tags="hint")
            def clear():
                self.canvas.delete(hint_id)
            self.root.after(1500, clear)

    def reset_game(self):
        self.board.fill(0)
        self.move_history.clear()
        self.current_turn = 1
        self.game_over = False
        self.last_move = None
        self.hover_pos = None
        self.ai_thinking = False
        self.status_var.set("玩家回合")
        self.combo_count = 0
        self.combo_label.config(text="")
        self.update_turn_indicator()
        # 恢复棋盘颜色
        self.canvas.config(bg=BG_BOARD)
        self.draw_board()
        self.draw_pieces()

    def back_to_menu(self):
        if not self.game_over:
            if messagebox.askyesno("返回主菜单", "确定返回吗？当前进度将丢失。"):
                self.root.destroy()
                root = tk.Tk()
                MainMenu(root)
                root.mainloop()
        else:
            self.root.destroy()
            root = tk.Tk()
            MainMenu(root)
            root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()