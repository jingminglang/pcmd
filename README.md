# pcmd

A simple python code  execute shell command by parallel way.


# Example
```
    root]$cat host.txt
    172.17.148.55
    172.17.148.56
    172.17.23.151
    172.17.23.152
    root]$ ./pcmd.py host.txt "date"
    Enter username: root
    Enter password: 
    172.17.23.152
    2016年 01月 04日 星期一 11:29:12 CST
    
    172.17.23.151
    2016年 01月 04日 星期一 11:29:12 CST
    
    172.17.148.55
    2016年 01月 04日 星期一 11:29:12 CST
    
    172.17.148.56
    2016年 01月 04日 星期一 11:29:12 CST
    
    成功的数:4
    失败的数:0
```
