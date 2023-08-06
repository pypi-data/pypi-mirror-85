import os
import json
import soco_device.GPUtil as GPUtil


class DeviceCheck(object):
    def __init__(self):
        """ Log model gpu usage, save into a file, and auto choose
            available device (gpu/cpu) for the next time.

        Example:
            dc = DeviceCheck()
            device_name = dc.get_device_by_model(model_name_or_path)
            device = torch.device(device_name)
            
            dc.log_start()
            # inference model for one time here
            dc.log_end()
            dc.save(model_name_or_path)
        
        """
        self.local_dir = 'resources'
        self.save_name = 'config.json'
        self.current_device = None
        self.current_device_ids = None
        self.model_memory_map = dict()
        self.log_map = dict()

        
    def get_device(self, max_load=1, max_mem=1, n_gpu=1):
        """ Get available gpu devices
        """
        device_id = GPUtil.getAvailable(order='memory', limit=n_gpu, maxLoad=max_load, maxMemory=max_mem)
        return(self._check_and_return(device_id, n_gpu))


    def get_device_by_model(self, model_id, n_gpu=1):
        """ Get first available gpu with largest available memory by model name,
            if not found return first gpu with largest available memory by default
        """
        model_path = self._get_valid_path(model_id)
        model_name = os.path.join(model_path, self.save_name)
        if model_id not in self.model_memory_map:
            if os.path.exists(model_name):  
                data = json.load(open(model_name))
                if 'memory_needed' in data:
                    print('Load memory info from json')
                    self.model_memory_map[model_id] = data['memory_needed']
                else:
                    return self.get_device(n_gpu=n_gpu)
            else:
                return self.get_device(n_gpu=n_gpu)

        all_device = GPUtil.getGPUs()
        device_id = [(i.id, i.memoryUsed) for i in all_device if i.memoryFree >= self.model_memory_map[model_id]]
        # sort by memory used ascendingly, and only extract the gpu id
        device_id = [i[0] for i in sorted(device_id, key=lambda x: x[1])] if len(device_id) > 0 else device_id
        print('GPU: {} Memory needed: {} '.format(device_id, self.model_memory_map[model_id]))
        return(self._check_and_return(device_id, n_gpu))


    def log_start(self):
        if self.current_device != 'cuda':
            return
        all_device = GPUtil.getGPUs()
        id_to_mem_st_map = {i.id: i.memoryUsed for i in all_device}
        self.log_map['start'] = sum([id_to_mem_st_map[i] for i in self.current_device_ids])
        print(self.log_map)


    def log_end(self):
        if 'start' not in self.log_map:
            print('Warning: did not find a log_start. Skip logging gpu usage.')
            return
        if self.current_device != 'cuda':
            return
        all_device = GPUtil.getGPUs()
        id_to_mem_ed_map = {i.id: i.memoryUsed for i in all_device}
        self.log_map['end'] = sum([id_to_mem_ed_map[i] for i in self.current_device_ids])
        print(self.log_map)


    def save(self, model_id, save_max=True):
        if 'start' not in self.log_map or 'end' not in self.log_map:
            print('Warning: did not find a complete log. Skip logging gpu usage.')
            return
        model_path = self._get_valid_path(model_id)
        if not os.path.exists(model_path):
            os.makedirs(model_path, exist_ok=True)
        memory_needed = self.log_map['end'] - self.log_map['start']
        if memory_needed < 0:
            print('Warning: memory change is negative. Set to 0.')
            memory_needed = 0
        model_name = os.path.join(model_path, self.save_name)
        
        if not os.path.exists(model_name):
            json.dump({'model':model_path, 'memory_needed':memory_needed}, open(model_name, 'w'))
        else:
            # only overwrite the config when the memory usage is higher than the record
            data = json.load(open(model_name))
            if 'memory_needed' not in data or not save_max or memory_needed > data['memory_needed']:
                data['memory_needed'] = memory_needed
                json.dump(data, open(model_name, 'w'))
            else:
                print('Did not update since {}mb (current) <= {}mb (recorded)'.format(memory_needed, data['memory_needed']))
                return

        print('{} needs {} mb gpu memory.'.format(model_path, memory_needed))
        print('Saved into {}'.format(model_name))


    def _get_valid_path(self, model_id):
        if self.local_dir in model_id:
            return model_id
        return os.path.join(self.local_dir, model_id)


    def _check_and_return(self, device_ids, n_gpu):
        """
        Return:
            current_divice(str): 'cpu' or 'cuda'
            device_ids(list): a list of none, one or more integers indicating available gpu ids

        """ 
        # ids must be sorted ascendingly to feed in pytorch nn.DataParallel
        device_ids = sorted(device_ids)[:n_gpu]
        self.current_device_ids = device_ids
        
        if len(device_ids) == 0:
            current_device = 'cpu'
        else:
            current_device = 'cuda'

        self.current_device = current_device
        
        if len(device_ids) < n_gpu:
            print('Warning: asked for {} gpus but only have {} available'.format(n_gpu, len(device_ids)))

        return current_device, device_ids
