import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from operate_system.__os import PC

import time
from enum import auto,Enum,unique

# 窗口大小
WINDOW_WIDTH = int(800)
WINDOW_HEIGHT = int(550)

# 进度条处位置偏移
OFFSET_LEFT = int(70)
OFFSET_TOP = int(5)
OFFSET_BOTTOM = int(55)
OFFSET_TEXT = int(35)
RITIO = int(5)
SPAN = int(10)

algorithms = [("FCFS",0),("RR",1),("SJF",2),("HRRN",3)]

@unique
class state(Enum):
    """
    定义页面运行状态
    """

    INIT = auto()
    CREATED = auto()
    RUNNING = auto()
    PAUSING = auto()
    FINISH = auto()

class UI(object):
    """
    界面类
    """
    
    def __init__(self) -> None:
        
        # 获取根页面
        self.root = ttk.Window(title="操作系统课程设计", resizable=(False,False))

        # 设置窗口居中
        self.root.geometry(self.__window_center())
        # self.root.place_window_center()

        # 算法变量
        self.algorithm = ttk.IntVar()

        # 进程数量变量
        self.process_num = ttk.StringVar(value="4")

        # 时间片变量
        self.time_slices = ttk.StringVar(value="1")

        # 初始化界面元素
        self.__init_window()

    def __init_window(self) -> None:
        """初始化页面元素"""

        # 第一个块
        frame1 = ttk.Frame(self.root, relief=SUNKEN, bootstyle=SECONDARY)
        frame1.pack(fill="x", ipady=5, padx=10)

        # 文字标签
        ttk.Label(frame1, text="调度算法", padding=10, bootstyle="inverse-secondary").grid(sticky=W, row=0, pady=10)

        # 算法选择单选框
        self.algorithm_selector:list[ttk.Radiobutton] = []
        self.algorithm_selector.append(ttk.Radiobutton(frame1, text=algorithms[0][0], variable=self.algorithm, 
                                                    bootstyle="primary-outline-toolbutton", value=algorithms[0][1], width=10))
        self.algorithm_selector.append(ttk.Radiobutton(frame1, text=algorithms[1][0], variable=self.algorithm, 
                                                    bootstyle="primary-outline-toolbutton", value=algorithms[1][1], width=10))
        self.algorithm_selector.append(ttk.Radiobutton(frame1, text=algorithms[2][0], variable=self.algorithm, 
                                                    bootstyle="primary-outline-toolbutton", value=algorithms[2][1], width=10))
        self.algorithm_selector.append(ttk.Radiobutton(frame1, text=algorithms[3][0], variable=self.algorithm, 
                                                    bootstyle="primary-outline-toolbutton", value=algorithms[3][1], width=10))

        for each in self.algorithm_selector:
            index = self.algorithm_selector.index(each)
            # each.configure(command=self.algorithm_click_event)
            each.grid(column=index, row=1, padx=10)
            
        # 文字标签
        ttk.Label(frame1, text="进程个数", padding=10, bootstyle="inverse-secondary").grid(sticky=W, column=4, row=0, pady=10)
        # 进程输入框
        self.entry_process_num = ttk.Entry(frame1, exportselection=False, textvariable=self.process_num, width=5)
        self.entry_process_num.grid(column=5, row=0, pady=10)

        # 文字标签
        ttk.Label(frame1, text="时间片大小", padding=10, bootstyle="inverse-secondary").grid(sticky=W, column=4, row=1)
        # 时间片输入框
        self.entry_time_slices = ttk.Entry(frame1, exportselection=False, textvariable=self.time_slices, width=5)
        self.entry_time_slices.grid(column=5, row=1)

        # 第二个块
        frame2 = ttk.Frame(self.root, relief=SUNKEN, bootstyle=SECONDARY)
        frame2.pack(fill="x", ipady=5, padx=10)

        # 五个功能按钮
        self.button_create = ttk.Button(frame2, text="创建进程", command=self.create,
                                        bootstyle="primary-outline-toolbutton", width=10)
        self.button_create.grid(column=0, row=0, padx=10, pady=10)

        self.button_run = ttk.Button(frame2, text="开始运行", command=self.run, state=DISABLED,
                                     bootstyle="primary-outline-toolbutton", width=10)
        self.button_run.grid(column=1, row=0, padx=10, pady=10)

        self.button_reset = ttk.Button(frame2, text="重新开始", command=self.restart, state=DISABLED,
                                       bootstyle="primary-outline-toolbutton", width=10)
        self.button_reset.grid(column=2, row=0, padx=10, pady=10)

        self.button_pause = ttk.Button(frame2, text="暂停", command=self.pause, state=DISABLED,
                                       bootstyle="primary-outline-toolbutton", width=10)
        self.button_pause.grid(column=3, row=0, padx=10, pady=10)

        self.button_exit = ttk.Button(frame2, text="退出", command=self.close_window,
                                      bootstyle="primary-outline-toolbutton", width=10)
        self.button_exit.grid(column=4, row=0, padx=10, pady=10)

        # 第三个块
        frame3 = ttk.Frame(self.root, relief=SUNKEN, bootstyle=SECONDARY)
        frame3.pack(fill="x", ipady=5, padx=10)

        # CPU状态
        ttk.Label(frame3, text="CPU", padding=10, bootstyle="inverse-secondary").grid(sticky=W, column=4,row=0)
        self.cpu_state = ttk.Label(frame3, text="free", bootstyle="inverse-success")
        self.cpu_state.grid(column=5,row=0)

        # IO状态
        ttk.Label(frame3, text="IO", padding=10, bootstyle="inverse-secondary").grid(sticky=W, column=4,row=1)
        self.io_state = ttk.Label(frame3, text="free", bootstyle="inverse-success")
        self.io_state.grid(column=5,row=1)

        # 两个图例
        ttk.Label(frame3, text="CPU计算", background="aqua", anchor=CENTER, width=10,
                  bootstyle="inverse").grid(padx=60, column=6, row=0)
        ttk.Label(frame3, text="I/O操作", background="wheat", anchor=CENTER, width=10,
                  bootstyle="inverse").grid(padx=60, column=6, row=1)

        # 就绪队列
        self.ready_queue_lable = ttk.Label(frame3, text="就绪队列[]", bootstyle="inverse-secondary")
        self.ready_queue_lable.grid(sticky=W, column=7, row=0)

        # 等待队列
        self.wait_queue_lable = ttk.Label(frame3, text="等待队列[]", bootstyle="inverse-secondary")
        self.wait_queue_lable.grid(sticky=W, column=7, row=1)

        # 平均周转时间
        self.average_tuturnaround_time = ttk.Label(frame3, bootstyle="inverse-secondary")
        self.average_tuturnaround_time.grid(sticky=W, padx=200, column=8, row=0)

        # 平均带权周转时间
        self.double_ztime = ttk.Label(frame3, bootstyle="inverse-secondary")
        self.double_ztime.grid(sticky=W, padx=200, column=8, row=1)

        # 第四个块
        frame4 = ttk.Frame(self.root, relief=SUNKEN, bootstyle=SECONDARY)
        frame4.pack(ipady=5, padx=10)

        # 滚动条
        scrollbar = ttk.Scrollbar(frame4)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 画布
        self.canvas = ttk.Canvas(frame4, width = WINDOW_WIDTH-40, height=250, bg = "white")
        self.canvas.pack(fill=Y, expand=True, padx=10, pady=5)
        self.canvas.pack()
        
        # 滚动条配置
        scrollbar.configure(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 800))

        # 绑定鼠标滚动事件
        def scroll_event(event):
            number = int(-event.delta / 120)
            self.canvas.yview_scroll(number, 'units')

        self.canvas.bind("<MouseWheel>", scroll_event)

    
    def main_loop(self) -> None:
        """进程模拟主循环"""

        # 暂停运行
        if (self.state == state.PAUSING or self.state == state.INIT):
            return
        if (not app.is_finish()):
            app.step()
            self.update_page()
            self.root.after(10,self.main_loop)
        else:
            self.state = state.FINISH
            self.update_button()
            self.average_tuturnaround_time.configure(text="平均周转时间："+app.average_turnaround_time)
            self.double_ztime.config(text="平均带权周转时间："+app.double_ztime)
            # 调试使用
            # for each in app.pcb_list:
            #     print(each)
        
    def __window_center(self) -> str:
        """窗口居中"""
        screenwidth = self.root.winfo_screenwidth()  # 屏幕宽
        screenheight = self.root.winfo_screenheight()  # 屏幕高

        size = '%dx%d+%d+%d' % (WINDOW_WIDTH,
                                WINDOW_HEIGHT,
                                (screenwidth - WINDOW_WIDTH) / 2,
                                (screenheight - WINDOW_HEIGHT) / 2)
        
        return size
    
    def open_window(self) -> None:
        """启动界面"""

        self.state = state.INIT
        self.root.mainloop()
    
    def close_window(self) -> None:
        """关闭窗口"""

        self.root.quit()
        self.root.destroy()

    def init_canvas(self) -> None:
        """初始化画板"""

        # 进程标号
        index = 0

        # 进度条数组 TODO
        self.progress_bar = []
        self.process_text = []
        
        # 位置偏移变量
        top = OFFSET_TOP
        bottom = OFFSET_BOTTOM
        space = SPAN + OFFSET_BOTTOM -OFFSET_TOP

        # 分割线
        self.canvas.create_line(OFFSET_LEFT, 0, OFFSET_LEFT, 800, fill="darkgray", dash=1)

        for each in app.pcb_list:
            
            # 计算进度条位置
            left = each.arrive_time * RITIO + OFFSET_LEFT
            right = (each.arrive_time + each.run_time) * RITIO + OFFSET_LEFT
            io_left = (each.io_time + each.arrive_time) * RITIO + OFFSET_LEFT
            io_right = each.wait_time * RITIO + io_left

            # 绘制文字、进度条
            self.canvas.create_text(OFFSET_TEXT, top+25, text=f"进程{index}", font=("黑体", 12), fill="dimgray")
            self.canvas.create_rectangle(left, top, right+1, bottom, fill="aqua", outline = "blue", width = 1)
            self.canvas.create_rectangle(io_left, top, io_right+1, bottom, fill="wheat", outline = "blue", width = 1)
            self.progress_bar.append(self.canvas.create_rectangle(left+1, top+1, left+1,
                                                                  bottom, outline = "", width = 0, fill = "palegreen"))

            top += space
            bottom += space
            index += 1

    def create(self) -> None:
        """创建进程"""

        # 获取app
        global app
        app = PC(PC.createPcb(int(self.process_num.get())), self.algorithm.get(), int(self.time_slices.get()))
        self.init_canvas()

        # 更新按钮状态
        self.state = state.CREATED
        self.update_button()

        # 调试使用
        # for each in app.pcb_list:
        #     print(each)

    def run(self) -> None:
        """开始运行"""
        
        self.state = state.RUNNING
        self.update_button()
        self.main_loop()

    def restart(self) -> None:
        """重新开始"""
        
        app.reset()
        self.canvas.delete(ALL)
        self.average_tuturnaround_time.configure(text="")
        self.double_ztime.configure(text="")
        self.state = state.INIT
        self.update_button()

    def pause(self) -> None:
        """暂停"""

        self.state = state.PAUSING
        self.update_button()

    def update_page(self) -> None:
        """更新页面"""

        # 更新系统状态
        if(app.ready_queue):
            self.cpu_state.configure(text="busy", bootstyle="inverse-danger")
            text = str([each.pid for each in app.ready_queue[1:]])
            self.ready_queue_lable.configure(text="就绪队列"+text)
        else:
            self.cpu_state.configure(text="free", bootstyle="inverse-success")

        if(app.wait_queue):
            self.io_state.configure(text="busy", bootstyle="inverse-danger")
            text = str([each.pid for each in app.wait_queue[1:]])
            self.wait_queue_lable.configure(text="等待队列"+text)
        else:
            self.io_state.configure(text="free", bootstyle="inverse-success")

        self.root.update()

        loop = len(app.pcb_list)
        while(loop):

            loop = len(app.pcb_list)

            for each, process in zip(self.progress_bar, app.pcb_list):
                tmp = self.canvas.coords(each)
                tmp1 = (process.ran_time + process.arrive_time) * RITIO + OFFSET_LEFT + 1
                if (process.ran_time >= 0 and tmp[2] != tmp1):
                    tmp[2] += 1
                    self.canvas.coords(each, tmp[0], tmp[1], tmp[2], tmp[3])
                else:
                    loop -= 1
            self.root.after(int(self.time_slices.get())*3)
            self.root.update()
        
    def update_button(self) -> None:
        """更新各按钮状态"""

        def change_algorithm_state(state):
            for each in self.algorithm_selector:
                each.configure(state=state)
            self.algorithm_selector[self.algorithm.get()].configure(state=NORMAL)

        def change_button_state(state_create, state_run, state_reset, state_pause):
            self.button_create.configure(state=state_create)
            self.button_run.configure(state=state_run)
            self.button_reset.configure(state=state_reset)
            self.button_pause.configure(state=state_pause)


        match self.state:
            case state.INIT:
                change_button_state(NORMAL,DISABLED,DISABLED,DISABLED)
                change_algorithm_state(NORMAL)

            case state.CREATED:
                change_button_state(DISABLED,NORMAL,NORMAL,DISABLED)

            case state.RUNNING:
                change_button_state(DISABLED,DISABLED,NORMAL,NORMAL)
                change_algorithm_state(DISABLED)

            case state.PAUSING:
                change_button_state(DISABLED,NORMAL,NORMAL,DISABLED)

            case state.FINISH:
                change_button_state(DISABLED,DISABLED,NORMAL,DISABLED)

    # def algorithm_click_event(self):
    #     """更新右上角输入框"""

    #     if self.algorithm.get() == 1:
    #         self.entry_time_slices.configure(state=DISABLED)
    #     else:
    #         self.entry_time_slices.configure(state=NORMAL)