<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [学习笔记](#学习笔记)
  - [一、Scrapy并行参数优化原理](#一scrapy并行参数优化原理)
  - [二、进程的创建](#二进程的创建)
  - [三、多进程调试](#三多进程调试)
  - [四、基于队列的进程间通信](#四基于队列的进程间通信)
  - [线程](#线程)

<!-- /code_chunk_output -->

# 学习笔记

## 一、Scrapy并行参数优化原理

1. 相较于单独使用`requests`库，scrapy拥有更快的速度，这是由scrapy内核使用了异步并行原理，调节`settings.py`内部参数，即可控制爬虫速度

    ```python {.line-numbers}
    # 并发请求数量 根据本机性能和目标网站性能进行调节
    CONCURRENT_REQUESTS = 32
    # 请求间隔 避免被目标网站识别为爬虫
    DOWNLOAD_DELAY = 3
    # 设置针对单个域名或Ip并发请求的最大数量
    CONCURRENT_REQUESTS_PER_DOMAIN = 16
    CONCURRENT_REQUESTS_PER_IP = 16
    ```

2. scrapy引擎：twisted异步IO Web框架——运行于单个进程中
   - 相较于同步编程，异步编程首先定义完整算法流程，再异步执行算法

## 二、进程的创建

1. 进程的父子关系，可以使用`os.fork()/multiprocessing.Process()`，前者比较底层，后者是一个更高级封装。

    ```python {.line-numbers}
    # 下列代码的输出:
    # >> 123456789
    # >> 123466789
    os.fork()
    print("123456789")

    # 基于返回值判断父/子进程，0表示子进程
    res = os.fork()
    ```

2. 使用`multiprocessing.Process()`创建进程：

    ```python {.line-numbers}
    def foo(name):
        print("hello {name}!")

    if __name__ == '__main__':
        proce = Process(target=f, args=("Trump",))
        proce.start()
        # 父进程等待子进程结束后结束，强制终止或超时返回None
        # 进程无法和自身进行合并，否则会造成死锁
        proce.join(timeout=None)
    ```

## 三、多进程调试

1. `os`模块相关函数：

    ```python {.line-numbers}
    # 获取父进程ID
    os.getppid()
    # 获取当前进程ID
    os.getpid()
    # 检查所有当前进程中活动的子进程
    p: list = multiprocessing.active_children()
    # 获取cpu内核数量
    num: int = multiprocessing.cpu_count()

    proce = Process(target=f, args=("Trump",))
    # 子进程名字，默认Process-i
    proce.name
    # 子进程ID
    proce.pid
    ```

2. 使用面向对象创建进程

    ```python {.line-numbers}
    class NewProcess(Process): #继承Process类创建一个新类
    def __init__(self,num):
        self.num = num
        super().__init__()

    def run(self):  #重写Process类中的run方法.
        while True:
            print(f'我是进程 {self.num} , 我的pid是: {os.getpid()}')
            time.sleep(1)

    for i in range(2):
        p = NewProcess(i)
        p.start()
    # 当不给Process指定target时，会默认调用Process类里的run()方法。
    # 这和指定target效果是一样的，只是将函数封装进类之后便于理解和调用。
    ```

## 四、基于队列的进程间通信

1. 进程间变量共享的方式：队列、管道、共享内存，为了解决资源抢占问题，引入了锁机制；
2. 使用队列进行进程间通信，主要利用block机制：

    ```python {.line-numbers}
    def write(q):
        print("启动Write子进程：%s" % os.getpid())
        for i in ["A", "B", "C", "D"]:
            q.put(i)  # 写入队列
            time.sleep(1)
        print("结束Write子进程：%s" % os.getpid())

    def read(q):
        print("启动Read子进程：%s" % os.getpid())
        while True:  # 阻塞，等待获取write的值
            value = q.get(True)
            print(value)
        print("结束Read子进程：%s" % os.getpid())  # 不会执行

    if __name__ == "__main__":
        # 父进程创建队列，并传递给子进程
        q = Queue()
        pw = Process(target=write, args=(q,))
        pr = Process(target=read, args=(q,))
        pw.start()
        pr.start()

        pw.join()
        # pr进程是一个死循环，无法等待其结束，只能强行结束
        # （写进程结束了，所以读进程也可以结束了）
        pr.terminate()
        print("父进程结束")
    ```

3. 队列的底层即为管道，通过一些封装使得进程更加安全，管道一般是双工的

    ```python {.line-numbers}
    from multiprocessing import Process, Pipe
    def f(conn):
        conn.send([42, None, 'hello'])
        conn.close()

    if __name__ == '__main__':
        parent_conn, child_conn = Pipe()
        p = Process(target=f, args=(child_conn,))
        p.start()
        print(parent_conn.recv())   # prints "[42, None, 'hello']"
        p.join()
    # 返回的两个连接对象 Pipe() 表示管道的两端。
    # 每个连接对象都有 send() 和 recv() 方法（相互之间的）。
    # 请注意，如果两个进程（或线程）同时尝试读取或写入管道的 同一 端，
    # 则管道中的数据可能会损坏。当然，同时使用管道的不同端的进程不存在损坏的风险。
    ```

4. 共享内存模拟C语言的内存操作，使得其效率更高：

    ```python {.line-numbers}
    from multiprocessing import Process, Value, Array

    def f(n, a):
        n.value = 3.1415927
        for i in a:
            a[i] = -a[i]

    if __name__ == '__main__':
        num = Value('d', 0.0)
        arr = Array('i', range(10))

        p = Process(target=f, args=(num, arr))
        p.start()
        p.join()

        print(num.value)
        print(arr[:])
    ```

5. 锁机制：

    ```python {.line-numbers}
    def job(v, num, l):
        l.acquire() # 锁住
        for _ in range(5):
            time.sleep(0.1) 
            v.value += num # 获取共享内存
            print(v.value, end="|")
        l.release() # 释放

    def multicore():
        l = mp.Lock() # 定义一个进程锁
        v = mp.Value('i', 0) # 定义共享内存
        # 进程锁的信息传入各个进程中
        p1 = mp.Process(target=job, args=(v,1,l)) 
        p2 = mp.Process(target=job, args=(v,3,l)) 
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    ```

6. 进程池：当进程的数量远远超过CPU内核数量时，就需要使用进程池对进程进行管理：

    ```python {.line-numbers}
    # 创建多个进程，表示可以同时执行的进程数量。默认大小是CPU的核心数
    p = Pool(4)
    for i in range(10):
        # 创建进程，放入进程池统一管理
        p.apply_async(run, args=(i,))
    # 如果我们用的是进程池，在调用join()之前必须要先close()，
    # 并且在close()之后不能再继续往进程池添加新的进程
    p.close()
    # 进程池对象调用join，会等待进程池中所有的子进程结束完毕再去结束父进程
    p.join()
    print("父进程结束。")
    p.terminate()
    ```

## 线程

1. 进程调度消耗资源较大，而线程则相反。另外一个进程中可以进行多个线程，同一进程中的内存共享更加方便；
2. 阻塞/非阻塞描述发送端的状态，同步和异步描述接收端的状态；
3. python在一个物理核心上运行，为了提高其运行效率，需要使用多线程和多进程相结合的方式；
4. 为了使进程的切换更加轻量级且增加认为的控制，则需要使用协程；
5. 线程的创建类似进程，可以采用函数的方式或面向对象的方式；
6. 线程池：
    - `from multiprocessing.dumpy import Pool`
    - `from concurrent.futures import ThreadPoolExecutor`
    - 避免死锁，如互相等待对方输出结果
7. 多线程与GIL锁
    - 每个进程只有一个GIL锁
    - 获取到GIL锁方可使用CPU
    - CPython解释器并不是真正意义上的多线程描述与伪并发
    - 多线程使用IO密集型应用
