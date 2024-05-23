from operate_system.__pcb import PCB

class IO(object):
    """模拟IO操作"""
    
    def __call__(self, run_time: int, wait_queue: list[PCB], ready_queue: list[PCB]):

        pid = []
        # 等待队列不为空,剩余运行时间不为零则继续
        while(wait_queue and run_time):
            # 获取队首元素
            pcb = wait_queue[0]
            pid.append(pcb.pid)

            # 计算进程是否能在时间片内完成IO操作
            run_time_slices = min(run_time, pcb.wait_time)
            run_time -= run_time_slices

            # 进程使用IO
            run(run_time_slices, pcb)

            # 检测进程是否就绪
            if (not pcb.wait_time):
                pcb.ready()
                wait_queue.pop(0)
                ready_queue.append(pcb)

        return

def run(run_time: int, pcb: PCB):
    """模拟运行修改进程时间"""

    pcb.ran_time += run_time
    pcb.wait_time -= run_time