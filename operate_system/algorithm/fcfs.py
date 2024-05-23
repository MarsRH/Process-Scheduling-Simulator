# from . import Scheduler
from operate_system.__pcb import PCB

class FCFS(object):
    """先到先服务调度算法"""

    def __call__(self, time, time_slices: int, ready_queue: list[PCB]):

        # 队列为空,系统继续运行
        if not ready_queue:
            return 1

        # 获取队首元素
        pcb = ready_queue[0]

        # 纠正进程实际运行时间
        before_io = min(pcb.remain_time, time_slices, pcb.io_time-pcb.ran_time)
        after_io = min(pcb.remain_time, time_slices)
        run_time = before_io if pcb.wait_time else after_io
        # run_time = min(pcb.remain_time, time_slices)

        # 进程运行
        if (pcb.is_running or pcb.is_ready):
            
            pcb.run(time, run_time)
  
        return run_time