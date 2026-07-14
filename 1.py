import tkinter as tk
from tkinter import messagebox

class MacPerfectRoomCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Premium Calculator & Hybrid Memo")
        self.root.geometry("820x560") 
        self.root.resizable(False, False)
        
        # 핑크 & 딥 벨벳 색상 설계
        self.COLOR_BG = "#1A1618"        
        self.COLOR_DISPLAY = "#000000"   
        self.COLOR_TEXT = "#FFFFFF"      
        self.COLOR_NUM_BG = "#D4A5B8"    
        self.COLOR_OP_BG = "#FF69B4"     
        self.COLOR_FN_BG = "#FBC5D8"     
        self.COLOR_DARK_TEXT = "#222222" 
        self.COLOR_MEMO_BG = "#2D2629"   
        
        self.root.configure(bg=self.COLOR_BG)
        
        # 계산기 변수
        self.current_value = ""
        self.expression = ""
        
        # 메모장 작동 제어 변수
        self.last_x, self.last_y = None, None
        self.draw_color = "#FF69B4"      
        
        self.create_layouts()
        
    def create_layouts(self):
        # 전체 화면 좌/우 분할
        self.left_frame = tk.Frame(self.root, bg=self.COLOR_BG, width=360, height=560)
        self.left_frame.pack(side="left", fill="both", padx=(10, 5), pady=10)
        self.left_frame.pack_propagate(False)
        
        self.right_frame = tk.Frame(self.root, bg=self.COLOR_BG, width=440, height=560)
        self.right_frame.pack(side="right", fill="both", padx=(5, 10), pady=10)
        self.right_frame.pack_propagate(False)
        
        # =========================================================================
        # [좌측 구역] 프리미엄 핑크 계산기
        # =========================================================================
        self.display_frame = tk.Frame(self.left_frame, bg=self.COLOR_DISPLAY, height=120)
        self.display_frame.pack(expand=True, fill="both", pady=(0, 10))
        self.display_frame.pack_propagate(False)
        
        self.sub_label = tk.Label(self.display_frame, text="", anchor="e", bg=self.COLOR_DISPLAY, fg="#FFB6C1", font=("Helvetica", 13))
        self.sub_label.pack(fill="x", padx=15, pady=(15, 0))
        
        self.main_label = tk.Label(self.display_frame, text="0", anchor="e", bg=self.COLOR_DISPLAY, fg=self.COLOR_TEXT, font=("Helvetica", 36, "bold"))
        self.main_label.pack(fill="x", padx=15, pady=(5, 10))
        
        self.btn_frame = tk.Frame(self.left_frame, bg=self.COLOR_BG)
        self.btn_frame.pack(expand=True, fill="both")
        
        for i in range(5): self.btn_frame.rowconfigure(i, weight=1)
        for j in range(4): self.btn_frame.columnconfigure(j, weight=1)
            
        buttons = [
            ('C', 0, 0, self.COLOR_FN_BG, 'fn'), ('⌫', 0, 1, self.COLOR_FN_BG, 'fn'), ('%', 0, 2, self.COLOR_FN_BG, 'fn'), ('/', 0, 3, self.COLOR_OP_BG, 'op'),
            ('7', 1, 0, self.COLOR_NUM_BG, 'num'), ('8', 1, 1, self.COLOR_NUM_BG, 'num'), ('9', 1, 2, self.COLOR_NUM_BG, 'num'), ('*', 1, 3, self.COLOR_OP_BG, 'op'),
            ('4', 2, 0, self.COLOR_NUM_BG, 'num'), ('5', 2, 1, self.COLOR_NUM_BG, 'num'), ('6', 2, 2, self.COLOR_NUM_BG, 'num'), ('-', 2, 3, self.COLOR_OP_BG, 'op'),
            ('1', 3, 0, self.COLOR_NUM_BG, 'num'), ('2', 3, 1, self.COLOR_NUM_BG, 'num'), ('3', 3, 2, self.COLOR_NUM_BG, 'num'), ('+', 3, 3, self.COLOR_OP_BG, 'op'),
            ('0', 4, 0, self.COLOR_NUM_BG, 'num'), ('.', 4, 1, self.COLOR_NUM_BG, 'num'), ('=', 4, 2, self.COLOR_OP_BG, 'eq')
        ]
        
        for text, row, col, bg, btype in buttons:
            colspan = 1
            if text == '=': colspan = 2
            fg_color = self.COLOR_DARK_TEXT if btype in ['fn', 'num'] else self.COLOR_TEXT
            
            btn = tk.Label(self.btn_frame, text=text, bg=bg, fg=fg_color, font=("Helvetica", 18, "bold"), relief="flat", cursor="hand2")
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)
            btn.bind("<Button-1>", lambda e, t=text: self.on_button_click(t))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#FFF0F5"))
            btn.bind("<Leave>", lambda e, b=btn, orig_bg=bg: b.config(bg=orig_bg))

        # =========================================================================
        # [우측 구역] 완전 독립형 룸 전환식 하이브리드 메모장
        # =========================================================================
        self.memo_ctrl = tk.Frame(self.right_frame, bg=self.COLOR_BG, height=40)
        self.memo_ctrl.pack(fill="x", pady=(0, 5))
        
        # 모드 전환 상단 버튼 조립
        self.btn_mode_text = tk.Label(self.memo_ctrl, text="⌨️ 글씨 쓰기", bg="#FF69B4", fg=self.COLOR_TEXT, font=("Helvetica", 11, "bold"), padx=12, pady=5, cursor="hand2")
        self.btn_mode_text.pack(side="left", padx=2)
        self.btn_mode_text.bind("<Button-1>", lambda e: self.show_text_room())
        
        self.btn_mode_draw = tk.Label(self.memo_ctrl, text="✍️ 핑크 낙서", bg="#444444", fg=self.COLOR_TEXT, font=("Helvetica", 11, "bold"), padx=12, pady=5, cursor="hand2")
        self.btn_mode_draw.pack(side="left", padx=2)
        self.btn_mode_draw.bind("<Button-1>", lambda e: self.show_draw_room())
        
        self.clear_btn = tk.Label(self.memo_ctrl, text="🗑️ 싹 지우기", bg=self.COLOR_FN_BG, fg=self.COLOR_DARK_TEXT, font=("Helvetica", 11, "bold"), padx=12, pady=5, cursor="hand2")
        self.clear_btn.pack(side="right", padx=2)
        self.clear_btn.bind("<Button-1>", lambda e: self.clear_memo())

        # 하단 작업대 컨테이너 확보
        self.work_space = tk.Frame(self.right_frame, bg=self.COLOR_MEMO_BG)
        self.work_space.pack(expand=True, fill="both")

        # 방 1: 순수 텍스트 타이핑창 (기본 배치)
        self.text_area = tk.Text(self.work_space, bg=self.COLOR_MEMO_BG, fg=self.COLOR_TEXT, insertbackground=self.COLOR_TEXT, font=("Helvetica", 14), bd=0, highlightthickness=0, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        
        # 방 2: 순수 그림판 도화지 (대기 상태)
        self.canvas = tk.Canvas(self.work_space, bg=self.COLOR_MEMO_BG, highlightthickness=0, cursor="pencil")
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.catch_touch_and_draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    # 방 교체 제어 시스템 (오류 수정)
    def show_text_room(self):
        self.canvas.pack_forget() 
        self.text_area.pack(expand=True, fill="both") 
        self.btn_mode_text.config(bg="#FF69B4")
        self.btn_mode_draw.config(bg="#444444")

    def show_draw_room(self):
        self.text_area.pack_forget() 
        self.canvas.pack(expand=True, fill="both") 
        self.btn_mode_text.config(bg="#444444")
        self.btn_mode_draw.config(bg="#FF69B4")

    # 계산기 엔진 로직
    def on_button_click(self, char):
        if char == 'C':
            self.current_value, self.expression = "", ""
            self.main_label.config(text="0"); self.sub_label.config(text="")
        elif char == '⌫':
            self.current_value = self.current_value[:-1]
            self.main_label.config(text=self.current_value if self.current_value else "0")
        elif char in ['+', '-', '*', '/', '%']:
            if self.current_value:
                self.expression += self.current_value + " " + char + " "
                self.sub_label.config(text=self.expression); self.current_value = ""
        elif char == '=':
            if self.current_value: self.expression += self.current_value
            try:
                expr = self.expression.replace('%', '/100')
                result = eval(expr)
                if isinstance(result, float) and result.is_integer(): result = int(result)
                elif isinstance(result, float): result = round(result, 6)
                self.main_label.config(text=str(result)); self.sub_label.config(text=self.expression + " =")
                self.current_value = str(result); self.expression = ""
            except Exception:
                messagebox.showerror("오류", "수식이 올바르지 않습니다."); self.on_button_click('C')
        else:
            if char == '.' and '.' in self.current_value: return
            self.current_value += char; self.main_label.config(text=self.current_value)

    # 그림판 도화지 드로잉 엔진
    def start_drawing(self, event):
        self.last_x, self.last_y = event.x, event.y

    def catch_touch_and_draw(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.draw_color, width=3, capstyle="round", smooth=True)
            self.last_x, self.last_y = event.x, event.y

    def stop_drawing(self, event):
        self.last_x, self.last_y = None, None

    def clear_memo(self):
        self.text_area.delete("1.0", tk.END)
        self.canvas.delete("all")
        self.show_text_room() 

if __name__ == "__main__":
    root = tk.Tk()
    # 상단 클래스명과 완벽하게 일치하도록 수정 완료
    app = MacPerfectRoomCalculator(root)
    root.mainloop()