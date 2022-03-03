该实验来源于电赛训练题，主要由K210和STM32F103C8T6构成，可实现人体温度检测，身份识别以及口罩识别。


## 一、各种链接
官方文档: [maixpy.sipeed.com](maixpy.sipeed.com)

例程： [github.com/sipeed/MaixPy_scripts](github.com/sipeed/MaixPy_scripts)

硬件资料（原理图等）: [dl.sipeed.com/MAIX/HDK](dl.sipeed.com/MAIX/HDK)

固件源码: [github.com/sipeed/MaixPy](github.com/sipeed/MaixPy)






## 实验器材
> -	 MCU：K210，STM32F103C8T6
> -	 屏幕：2.4寸
> -	 测温模块： GY - 906

## STM32
STM32负责温度测量以及温度的监控。

## K210


开发文档:
[wiki.sipeed](https://wiki.sipeed.com/soft/maixpy/zh/index.html)

K210负责身份识别以及口罩识别。

### MemoryError: Out of normal MicroPython Heap Memory!

k210 有 6MiB 通用内存， 需要用到内存的有固件(K210 是一次性将所有代码加载到内存的….)，一些功能所需比如摄像头缓冲区等，还有存放模型, 另外有 2MiB 给 KPU 专用的内存(如果使用 KPU 的话)

打印剩余内存:
```python
import gc
print(gc.mem_free())
```
GC 的总内存大小可以通过下面的代码来设置， GC 的大了， 系统的就小了，如果模型大这里就不要设置太大了。 

```python 
from Maix import utils
import machine
old = utils.gc_heap_size()
print(old)
new = 512*1024
utils.gc_heap_size(new)
machine.reset() #重启
```



开发过程中可能由于空间不足无法放下足够的模型，可以通过减小堆栈大小。utils.gc_heap_size(1024*256)




### 身份识别


### 口罩识别



后续可完全删除STM32F103C8T6部分，单K210可完美实现原功能。