import tkinter as tk
from tkinter import Canvas, ttk, filedialog, Listbox
from PIL import ImageTk

# 컬러
bg_color = "#004094"
bg_color2 = "#005EB8"
sub_color = "#B9D9EB"

wn = tk.Tk()
wn.title("영상 데이터 오차율 분석")
wn.config(bg = bg_color)

# 화면 크기
s_width = wn.winfo_screenwidth()
s_height = wn.winfo_screenheight()
tk_width = 1080
tk_height = 720
s_pos_x = (s_width - tk_width) / 2
s_pos_y = (s_height - tk_height) / 2
wn.geometry("%dx%d+%d+%d" % (tk_width, tk_height, s_pos_x, s_pos_y))
wn.resizable(False, False)

# 기본 함수, 설정-----------------------------

# frame 구성
def frame(master, row, col, rowmin, colmin):
    frm = ttk.Frame(master)
    frm.rowconfigure(row, minsize = rowmin)
    frm.columnconfigure(col, minsize = colmin)
    return frm

# frame 바꾸기
def change_frm(bf_frm, after_frm):
    bf_frm.grid_remove()
    after_frm.grid()

# 바탕 색
style_frm1 = ttk.Style()
style_frm1.theme_use('alt')
style_frm1.configure("TFrame", background=sub_color)

# 버튼 스타일
style_btn = ttk.Style()
style_btn.theme_use('alt')
style_btn.configure("TButton", background=bg_color, foreground=sub_color, font=("", 20, "bold"))
style_btn.map('TButton', background=[('active', bg_color2)])

# 글씨 스타일
style_lbl1 = ttk.Style()
style_lbl1.theme_use('alt')
style_lbl1.configure("second.TLabel", background=sub_color, foreground=bg_color2, font=("", 30, "bold"))


# 시작 화면----------------------------------

# 시작 화면 frame
frm_first = frame(wn, [0, 1, 2], [0], tk_height / 3, tk_width)

# 구성요소
btn_start = ttk.Button(frm_first, text="Start", style="first.TButton", command=lambda: change_frm(frm_first, frm_main))
btn_info = ttk.Button(frm_first, text="Info", style="first.TButton", command=lambda: change_frm(frm_first, frm_info))
lbl_title = ttk.Label(frm_first, text="Open CV를 활용한 오차계산", style="second.TLabel")

# 구성요소 배치
lbl_title.grid(row = 0, column = 0, ipadx= 0, ipady= 10)
btn_start.grid(row = 1, column = 0, ipadx= 0, ipady= 50)
btn_info.grid(row = 2, column = 0, ipadx= 0, ipady= 50)
frm_first.grid()

# 정보 화면----------------------------------------

# 구성요소
frm_info = frame(wn,[0,1],0,tk_height/2,tk_width)
lbl_info = ttk.Label(frm_info,text = """
프로그램에 대한 정보
""",
style = "second.TLabel")
btn_info_back = ttk.Button(frm_info, text = "Back",command = lambda: change_frm(frm_info, frm_first))

#배치
lbl_info.grid(row =0,column = 0)
btn_info_back.grid(row =1,column = 0)

# 메인 화면--------------------------------------------

# 메인화면 + 메인화면에 속한 frame
frm_main = frame(wn,[0,1,2],0,0,tk_width)

frm_main_lbx = frame(frm_main,0,0,tk_height*(3/7),0)
frm_main_lbx.grid(row = 0,column= 0)

frm_main_chk = frame(frm_main,0,[0,1,2,3],tk_height*(2.3/7),tk_width/4)
frm_main_chk.grid(row = 1,column= 0)

frm_main_btn = frame(frm_main,0,[0,1,2],tk_height*(2/7),tk_width/3)
frm_main_btn.grid(row = 2,column= 0)

# 1) lbx frame 구성요소
lbx_main = tk.Listbox(frm_main_lbx, 
                      width= int(tk_width/13),
                      height = int(tk_height/60),
                      selectmode=tk.MULTIPLE,
                      font= ("",15,"bold"))
scb_main = ttk.Scrollbar(frm_main_lbx,orient="vertical")
scb_main.config(command=lbx_main.yview)
lbx_main.pack(side="left",fill='y')
scb_main.pack(side="right",fill='y')
lbx_main.config(yscrollcommand=scb_main.set)

# 2) chk frame 구성요소
lbl_chk = ttk.Label(frm_main_chk,text="오차 분석 방법: ",style = "second.TLabel",font=("",20,"bold"))
lbl_chk.grid(row = 0,column =0,sticky="e")

error_cal_list = ["MSE","MSA", "RMSE"]
cbx_chk = ttk.Combobox(frm_main_chk,
                       values=error_cal_list,
                       state="readonly",
                       font= ("",15,"bold") )
cbx_chk.set("오차 분석 방법 선택")
cbx_chk.grid(row = 0,column =1,sticky="w")

def Target():
    file_path = filedialog.askopenfilename()
    lbl_chk.config(text=file_path)

btn_chk = ttk.Button(frm_main_chk,text = "Target",command=Target)
btn_chk.grid(row = 0,column=2,ipady=50)
lbl_chk = ttk.Label(frm_main_chk,text = "Taget 이미지 경로",style = "second.TLabel",font=("",15,"bold"),wraplength=250)
lbl_chk.grid(row=0,column=3,sticky="w")

# 3) btn frame 구성요소
# 3-1) btn 커맨드
def data_add(): # 영상데이터 추가 커맨드
    file_path = filedialog.askopenfilenames()
    for path in file_path:
        lbx_main.insert(tk.END,path)

def data_del(): # 영상데이터 삭제 커맨드
    selected_index = lbx_main.curselection()
    for index in reversed(selected_index):
        lbx_main.delete(index)

temp = [] # 임시 데이터
sorted_data=[] # 정렬 데이터

def data_anlz(): # 영상데이터 분석 + 화면 전환 커맨드
    import img2vect as i2v
    import cv2 as cv
    global lbl_chk, lbx_main, cbx_chk
    global sorted_data, image, temp

    error_cal = cbx_chk.get().lower() # 선택한 오차 분석 방법

    # Load and process target image
    target_path = lbl_chk['text'] # target image path
    target_image = i2v.load_binary_image(target_path)
    x, y, w, h, _ = i2v.get_graph_roi(target_image, connectivity=8)
    target_crop = target_image[y : y + h, x : x + w]
    target_w, target_h = target_crop.shape
    target_vec = i2v.image_to_vector(target_crop)

    # Load and process sample images
    sample_path_list = lbx_main.get(0, tk.END) # sample 영상 데이터 위치
    for path in sample_path_list:
        sample_image = i2v.load_binary_image(path)
        x, y, w, h, _ = i2v.get_graph_roi(sample_image, connectivity=8)
        k = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
        sample_crop = cv.resize(sample_image[y : y + h, x : x + w], (target_h, target_w))
        sample_crop = cv.erode(sample_crop, k)
        sample_vec = i2v.image_to_vector(sample_crop)
        error = i2v.calc_error(target_vec, sample_vec, method=error_cal)
        temp.append((path, error))

    sorted_data = sorted(temp, key=lambda x: x[1])
    for data in sorted_data:
        lbx_result.insert(tk.END, data[0])
    
    image = ImageTk.PhotoImage(file=sorted_data[0][0])
    cvs_result.create_image(cvs_result.winfo_width() / 2,
                            cvs_result.winfo_height() / 2,
                            image=image)

    lbl_result.config(text = f"""
계산방법:{cbx_chk.get()}
오차율: {sorted_data[0][1]}
""")
    change_frm(frm_main, frm_result)

# 3-2) 구성요소
btn_main_add = ttk.Button(frm_main_btn,text = "추가",command = data_add)
btn_main_del = ttk.Button(frm_main_btn,text = "삭제",command = data_del)
btn_main_anlz = ttk.Button(frm_main_btn,text = "분석",command = data_anlz)
btn_main_add.grid(row = 0,column = 0,ipady= 30)
btn_main_del.grid(row = 0,column = 1,ipady= 30)
btn_main_anlz.grid(row = 0,column = 2,ipady= 30)

# 결과화면--------------------------------------------------------------
# 결과 화면+속한(canvas,listbox) frame
frm_result = frame(wn,0,[0,1],0,tk_width/2)
frm_result_cvs = frame(frm_result,[0,1],0,tk_height/2,0)
frm_result_lbx = frame(frm_result,[0,1],[0,1,2],tk_height/2,0)
frm_result_cvs.grid(row=0,column=0)
frm_result_lbx.grid(row=0,column=1)

# cvs frame 구성요소
cvs_result = tk.Canvas(frm_result_cvs,height = tk_height/1.8,width = tk_width/2)
lbl_result = ttk.Label(frm_result_cvs,text = "",style = "second.TLabel",font= ("",25,"bold"), width = 400)
cvs_result.grid(row=0,column=0,sticky="ns")
lbl_result.grid(row=1,column=0,sticky="nw")

# lbx frame 구성요소
scb_result = ttk.Scrollbar(frm_result_lbx,orient="vertical")
lbx_result = tk.Listbox(frm_result_lbx, 
                        width= int(tk_width/25),
                        height = int(tk_height/40),
                        font= ("",15,"bold"),
                        yscrollcommand=scb_result.set)
scb_result.config(command=lbx_result.yview)
lbx_result.grid(row=0,column=0,columnspan=2)
scb_result.grid(row=0,column=3,sticky="nsw")
lbx_result.config(yscrollcommand=scb_result.set)

# lbx frame에서 버튼 2개
def result_update():
    global image
    lbl_result.config(text = f"""
계산방법:{cbx_chk.get()}

오차율
            x: {sorted_data[lbx_result.curselection()[0]][1]}%
            y: {sorted_data[lbx_result.curselection()[0]][1]}%
            x,y: {sorted_data[lbx_result.curselection()[0]][1]}%
                       """)
    cvs_result.delete("all")
    image=tk.PhotoImage(file = sorted_data[lbx_result.curselection()[0]][0])
    cvs_result.create_image(cvs_result.winfo_width()/2,
                            cvs_result.winfo_height()/2,
                            image = image)

def return_start():
    cbx_chk.set("오차 분석 방법 선택")
    lbx_main.delete(0,tk.END)
    lbx_result.delete(0,tk.END)
    cvs_result.delete("all")   
    change_frm(frm_result,frm_main)

btn_result_update = ttk.Button(frm_result_lbx,text = "오차율",command = result_update)
btn_result_return = ttk.Button(frm_result_lbx,text = "돌아가기",command = return_start)
btn_result_update.grid(row=1,column=0,ipady= 50)
btn_result_return.grid(row=1,column=1,ipady= 50)

wn.mainloop()
