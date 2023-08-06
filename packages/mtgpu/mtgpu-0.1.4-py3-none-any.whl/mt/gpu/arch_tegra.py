'''Module specific to Nvidia Tegra/Jetson arch.'''


import subprocess as _sp
import psutil as _pu


arch2gpu = {
    'arm64-tk1': 'NVIDIA Jetson TK1',
    'arm64-tx1': 'NVIDIA Jetson TX1',
    'arm64-tx2': 'NVIDIA Jetson TX2',
    'arm64-j43': 'NVIDIA Jetson TX2'
    }


def get_mem_info_impl(arch):
    res = {}

    mem_info = _pu.virtual_memory()
    res['cpu_mem_free'] = mem_info.free
    res['cpu_mem_used'] = mem_info.used
    res['cpu_mem_total'] = mem_info.total
    res['cpu_mem_shared_with_gpu'] = True

    gpu = {}
    gpu['mem_free'] = res['cpu_mem_free']
    gpu['mem_used'] = res['cpu_mem_used']
    gpu['mem_total'] = res['cpu_mem_total']
    gpu['name'] = arch2gpu.get(arch, 'Unknown')
    
    res['gpus'] = [gpu]
    
    return res
