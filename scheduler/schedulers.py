import math

from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        for process in self.processes:
            if process._process_id == cur_event.process_id:
                processtorun = process
        return processtorun

    def dispatcher_func(self, cur_process):
        cur_process._process_state = (ProcessStates.RUNNING)
        while cur_process._process_state == ProcessStates.RUNNING:
            accranfor = cur_process.run_for(cur_process._service_time,self.time)
            if cur_process._remaining_time == 0:
                cur_process._process_state = ProcessStates.TERMINATED
                completedevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_DONE, event_time =  self.time+accranfor)
                return completedevent
        


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        
        process_ready_list = []
        for process in self.processes: 
            if process._process_state == ProcessStates.READY:
                process_ready_list.append(process)
                
                
        for item in range(len(process_ready_list)):
            for proc in range(0, len(process_ready_list) - item - 1):
                if process_ready_list[proc]._service_time > process_ready_list[proc + 1]._service_time:
                    temp = process_ready_list[proc]
                    process_ready_list[proc] = process_ready_list[proc+1]
                    process_ready_list[proc+1] = temp
                    
        
        processtorun = process_ready_list[0]
        return processtorun
        
        

    def dispatcher_func(self, cur_process):
        cur_process._process_state = (ProcessStates.RUNNING)
        while cur_process._process_state == ProcessStates.RUNNING:
            accranfor = cur_process.run_for(cur_process._service_time,self.time)
            if cur_process._remaining_time == 0:
                cur_process._process_state = ProcessStates.TERMINATED
                completedevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_DONE, event_time =  self.time+accranfor)
                return completedevent


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        for process in self.processes:
            if process._process_id == cur_event.process_id:
                processtorun = process
        return processtorun

    def dispatcher_func(self, cur_process):
        cur_process._process_state = (ProcessStates.RUNNING)
        while cur_process._process_state == ProcessStates.RUNNING:
            accranfor = cur_process.run_for(self.quantum,self.time)
            if cur_process._remaining_time == 0:
                cur_process._process_state = ProcessStates.TERMINATED
                completedevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_DONE, event_time =  self.time+accranfor)
                return completedevent
            else:
                cur_process._process_state = ProcessStates.READY
                incompleteevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_REQ, event_time =  self.time+accranfor)
                return incompleteevent


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        
        
        
        process_ready_list = []
        for process in self.processes: 
            if process._process_state == ProcessStates.READY:
                process_ready_list.append(process)
                
                
        for item in range(len(process_ready_list)):
            for proc in range(0, len(process_ready_list) - item - 1):
                if process_ready_list[proc]._remaining_time > process_ready_list[proc + 1]._remaining_time:
                    temp = process_ready_list[proc]
                    process_ready_list[proc] = process_ready_list[proc+1]
                    process_ready_list[proc+1] = temp
        

        processtorun = process_ready_list[0] 
        return processtorun
        

    def dispatcher_func(self, cur_process):
        cur_process._process_state = (ProcessStates.RUNNING)
        nexttime = self.next_event_time()
        while cur_process._process_state == ProcessStates.RUNNING:
                accranfor = cur_process.run_for(nexttime-self.time,self.time)
                if self.context_switch_time > 0.0:
                    if (cur_process._remaining_time+self.context_switch_time) <= (nexttime-(self.time+accranfor)):
                        runagain = cur_process.run_for(cur_process._remaining_time,self.time+accranfor)
                        cur_process._process_state = ProcessStates.TERMINATED
                        completedagainevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_DONE, event_time =  self.time+accranfor+runagain)
                        return completedagainevent
                        break
                    elif cur_process._remaining_time == 0:
                        cur_process._process_state = ProcessStates.TERMINATED
                        completedevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_DONE, event_time =  self.time+accranfor)
                        return completedevent
                        break
                
                    else:
                        cur_process._process_state = ProcessStates.READY
                        incompleteevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_REQ, event_time =  self.time+accranfor)
                        return incompleteevent
                        break
                else:
                    if cur_process._remaining_time == 0:
                        cur_process._process_state = ProcessStates.TERMINATED
                        completedevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_DONE, event_time =  self.time+accranfor)
                        return completedevent
                        break
                
                    else:
                        cur_process._process_state = ProcessStates.READY
                        incompleteevent = Event (process_id = cur_process._process_id, event_type = EventTypes.PROC_CPU_REQ, event_time =  self.time+accranfor)
                        return incompleteevent
                        break

        