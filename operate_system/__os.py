from operate_system.__pcb import PCB

from operate_system.algorithm.fcfs import FCFS
from operate_system.algorithm.rr import RR
from operate_system.algorithm.sjf import SJF
from operate_system.algorithm.hrrn import HRRN
from operate_system.algorithm.inout import IO

from copy import deepcopy
from random import randint

# 最早到达时间
MIN_ARRIVE_TIME = int(0)

# 最晚到达时间
MAX_ARRIVE_TIME = int(20)

# 最小运行时间
MIN_RUN_TIME = int(50)

# 最大运行时间
MAX_RUN_TIME = int(100)

# 最小阻塞时间
MIN_WAIT_TIME = int(3)

ALGORITHMS = [FCFS, RR, SJF, HRRN]

class PC(object):
    """
    模拟PC类
    """

    pid: int = 0
    time: int = 0
    time_slices: int = 0
    pcb_list: list[PCB] = []
    ready_queue: list[PCB] = []
    wait_queue: list[PCB] = []
    finish = False
    # io = IO()
    # cpu = CPU()
    
    def __init__(self, pcb_list: list[PCB], algorithm_num: int, time_slices: int) -> None:
        """
        初始化
        """
        self.pcb_list = deepcopy(pcb_list)
        # self.pcb_list = pcb_list
        self.pcb_list.sort(key=lambda pcb: pcb.arrive_time)
        self.algorithm = ALGORITHMS[algorithm_num]()
        self.time_slices = time_slices
        self.io = IO()

    def is_finish(self) -> bool:
        """
        判断是否完成
        """
        return self.finish == True

    def createPcb(num: int) -> list[PCB]:
        """
        创建PCB\n
        num: PCB数量
        """
        # 自定义PCB部分
        # if len(args):
        #     for each in args:
        #         arrive_time = each.arrive_time
        #         run_time = each.arrive_time
        #         io_time = each.io_time
        #         wait_time = each.wait_time
        #         self.pcb.append(PCB(arrive_time, run_time, io_time, wait_time))
        pcb_list = []
       
        for i in range(num):
            arrive_time = randint(MIN_ARRIVE_TIME, MAX_ARRIVE_TIME)
            run_time = randint(MIN_RUN_TIME, MAX_RUN_TIME)
            wait_time = randint(MIN_WAIT_TIME, run_time-MIN_RUN_TIME+MIN_WAIT_TIME)
            io_time = randint(1,run_time-wait_time)
            pcb_list.append(PCB(arrive_time,run_time,io_time,wait_time))
            pcb_list[i]._wait_time = wait_time
        
        return pcb_list
    
    def reset(self) -> None:
        """
        重置
        """
        # TODO
        self.time = 0
        self.ready_queue.clear()
        self.wait_queue.clear()
        # self.finish = True
        self.pcb_list.clear()

    def step(self) -> (int, int|None, list):
        """
        单步执行
        """
        run_time = self.time_slices

        finish = len(self.pcb_list)
        
        for pcb in self.pcb_list:

            # 将刚到达的进程加入到就绪队列
            if (pcb.is_none and pcb.is_arrive(self.time)):
                pcb.ready(self.pid)
                self.pid += 1
                self.ready_queue.append(pcb)

            # 调用io，进程进入阻塞队列
            if (pcb.io_time == pcb.ran_time and not pcb.is_wait):
                pcb.wait()
                self.wait_queue.append(pcb)
                self.ready_queue.remove(pcb)

            # 更新周转时间
            if not pcb.is_finish:
                pcb.update_turnaround_time(self.time)
                if (pcb.run_time == pcb.ran_time):
                    self.ready_queue.remove(pcb) if pcb.is_running or pcb.is_ready else None
                    self.wait_queue.remove(pcb) if pcb.is_wait else None
                    pcb.finish(self.time)
            else:
                finish -= 1

        # 执行调度算法
        run_time = self.algorithm(self.time, self.time_slices, self.ready_queue)
       
        # io操作
        self.io(run_time, self.wait_queue, self.ready_queue)

        # 调试使用
        # print(f"[{self.time}]pcb_list:")
        # for each in self.pcb_list:
        #     print(f"{each}")
        # print("\n")


        # 判断结束
        self.finish = False if finish else True

        # 时间流逝
        self.time += run_time

        return run_time
    
    @property
    def average_turnaround_time(self):
        time = 0
        for each in self.pcb_list:
            time += each.turnaround_time
        return str(time/len(self.pcb_list))
    
    @property
    def double_ztime(self):
        time = 0
        for each in self.pcb_list:
            time += each.turnaround_time/(each.run_time-each._wait_time)
        return "{:.2f}".format(time/len(self.pcb_list))