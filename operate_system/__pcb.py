from enum import auto,Enum,unique
from dataclasses import dataclass

@unique
class State(Enum):
    """
    定义了进程状态\n
    NONE: 空\n
    READY: 就绪\n
    RUNNING: 运行\n
    WAIT: 阻塞\n
    FINISH: 完成
    """
    NONE = auto()
    READY = auto()
    RUNNING = auto()
    WAIT = auto()
    FINISH = auto()

@dataclass
class PCB(object):
    """
    模拟PCB\n
    用于描述进程的基本情况以及运行变化的过程\n
    进程存在的唯一标志。
    """
    arrive_time: int
    run_time: int
    io_time: int
    wait_time: int
    ran_time: int = -1
    pid: int = -1
    start_time: int = -1
    last_time: int = -1
    end_time: int = -1
    turnaround_time: int = -1
    priority: int = -1
    state: State = State.NONE
    _wait_time: int = 0

    @property
    def remain_time(self):
        """返回进程剩余时间"""
        return self.run_time - self.ran_time

    def ready(self, pid=-1):
        """
        进程就绪,初始化请为其分配PID
        """
        self.state = State.READY

        if pid >= 0 and self.pid < 0:
            self.turnaround_time = 0
            self.ran_time = 0
            self.pid = pid

    def run(self, time: int, run_time: int):
        """
        进程运行指定时间
        """
        self.state = State.RUNNING
        if self.start_time < 0:
            self.start_time = time
        self.ran_time += run_time
        self.last_time = time
        return self.remain_time
    
    def wait(self, ):
        """
        进程阻塞
        """
        self.state = State.WAIT

    def finish(self, time: int):
        """
        进程完成
        """
        self.state = State.FINISH
        self.end_time = time

    def is_arrive(self, time: int):
        """
        进程是否到达
        """
        return time >= self.arrive_time

    def update_turnaround_time(self, time: int):
        """
        更新周转时间
        """
        self.turnaround_time = time - self.arrive_time

    # 判断进程状态的方法
    @property
    def is_none(self):
        return self.state == State.NONE

    @property
    def is_ready(self):
        return self.state == State.READY

    @property
    def is_running(self):
        return self.state == State.RUNNING
    
    @property
    def is_wait(self):
        return self.state == State.WAIT

    @property
    def is_finish(self):
        return self.state == State.FINISH