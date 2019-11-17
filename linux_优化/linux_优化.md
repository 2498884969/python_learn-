## 1.CPU性能

### 1.1 平均负载的理解

```shell
# 1. 获取CPU核数 
grep 'model name' /proc/cpuinfo | wc -l
# 2. 安装 stress 和 sysstat包
yum install stress sysstat -y
# 3. 使用源码安装sysstat
https://github.com/sysstat/sysstat/releases
./configure
./make && make install
```

- 实验一(CPU)

```shell
# 1. 模拟CPU使用100%
stress --cpu 1 --timeout 600
# 2. -d 参数表示高亮显示变化的区域
watch -d uptime
# 3. -P ALL 表示监控所有 CPU，后面数字 5 表示间隔 5 秒后输出一组数据
mpstat -P ALL 5
# 4. 间隔 5 秒后输出一组数据（查看是哪个进程占比高）
pidstat -u 5 1
```

- 实验二(I/O 密集型进程)

```shell
# 模拟 I/O 压力
stress -i 1 --timeout 600
# 2.CPU 负载
watch -d uptime
# 显示所有 CPU 的指标，并在间隔 5 秒输出一组数据
mpstat -P ALL 5 1
#间隔 5 秒后输出一组数据，-u 表示 CPU 指标
pidstat -u 5 1
```

- 实验三(大量进程场景)

```shell
# 1.模拟的是 4 个进程：
stress -c 4 --timeout 600
# 2.
 uptime
# 3. pidstat -u 5 3
```

### 1.2 上下文切换

```shell
用户内核
进程
线程
中断

# 每隔 5 秒输出 1 组数据
$ vmstat 5
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 7005360  91564 818900    0    0     0     0   25   33  0  0 100  0  0
cs（context switch）是每秒上下文切换的次数。
in（interrupt）则是每秒中断的次数。
r（Running or Runnable）是就绪队列的长度，也就是正在运行和等待 CPU 的进程数。
b（Blocked）则是处于不可中断睡眠状态的进程数。
# 每隔 5 秒输出 1 组数据
$ pidstat -w 5 
08:18:26      UID       PID   cswch/s nvcswch/s  Command
08:18:31        0         1      0.20      0.00  systemd
08:18:31        0         8      5.40      0.00  rcu_sched

所谓自愿上下文切换，是指进程无法获取所需资源，导致的上下文切换。比如说， I/O、内存等系统资源不足时，就会发生自愿上下文切换。
而非自愿上下文切换，则是指进程由于时间片已到等原因，被系统强制调度，进而发生的上下文切换。比如说，大量进程都在争抢 CPU 时，就容易发生非自愿上下文切换。
```

实验

```shell

```

