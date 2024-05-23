# 进程调度模拟器

## 快速开始
直接至 Releases 下载即可使用  
也可以下载源码添加自己想要的算法后自行编译使用  
使用`pip install -r requirements.txt`下载项目依赖  
建议在**venv**虚拟环境中进行二次开发

## 支持算法
- [x] FCFS
- [x] RR
- [x] SJF
- [x] HRRN

## 拓展支持
根据 `src\operate_system\algorithm` 中的其他算法模板编写  
在 **__os.py** 中的 **ALGORITHMS** 中添加新增算法  
在 **ui.py** 中添加对应算法的按钮

## TODO
- [ ] 使拓展更方便
- [ ] 优化UI
- [ ] 修复异步执行IO但是同步显示动画的BUG