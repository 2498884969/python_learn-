# Gitlab安装配置管理

```shell
# 1. 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld
# 2. 关闭SELINUX系统并重启
vi /etc/sysconfig/selinux
...
SELINUX=disable
...
reboot
# 3. 安装依赖包
yum install curl policycoreutils openssh-server openssh-clients postfixs

```

