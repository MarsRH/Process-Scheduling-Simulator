from operate_system.__pcb import PCB

class HRRN(object):
    """高响应比调度算法"""

    def __call__(self, time, time_slices: int, ready_queue: list[PCB]):

        # 队列为空,系统继续运行
        if not ready_queue:
            return 1

        # 计算优先级
        for each in ready_queue:
            each.priority = ((time-each.last_time)+(each.run_time-each._wait_time))/(each.run_time-each._wait_time)
        ready_queue.sort(key=lambda pcb: pcb.priority, reverse=True)
        pcb = ready_queue[0]

        # 纠正进程实际运行时间
        before_io = min(pcb.remain_time, pcb.io_time-pcb.ran_time)
        after_io = pcb.remain_time
        run_time = before_io if pcb.wait_time else after_io

        # 进程运行
        if (pcb.is_running or pcb.is_ready):
            
            pcb.run(time, run_time)
  
        return run_time