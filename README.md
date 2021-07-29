# [MaixPy3 Scripts](https://github.com/sipeed/MaixPy3_scripts)

====


Scripts for [MaixPy3](https://github.com/sipeed/MaixPy3) ~ have a good time~

Doc of MaixPy3: [maixpy3.sipeed.com](https://maixpy3.sipeed.com)

## Directory Structure

| directory | description |
| --------- | ----------- |
| application | Some complex applications |
| basic | basic MaixPy3 usage |
| x86 | x86 test code |
| hardware | MaixPy3 API usage demo |
| machine_vision | demo for vision related, including machine vision and AI processing related |


-------------------------------

运行在 [MaixPy3](https://github.com/sipeed/MaixPy3) 上的脚本，玩得开心～

MaixPy 文档: [maixpy3.sipeed.com](https://maixpy3.sipeed.com)

另外，国内也可以在[gitee](https://gitee.com/Sipeed/maixpy3_scripts)上查看，会实时同步, 对脚本有疑问请到[github](https://github.com/sipeed/MaixPy3_scripts/issues)搜索问题或者提问， MaixPy 固件相关问题请到[MaixPy issue](https://github.com/sipeed/MaixPy3_scripts/issues)提问



## 目录结构

| 目录 | 描述 |
| --------- | ----------- |
| application | 一些在v831上使用的python3包 |
| basic | 基本的 maixpy3 使用 |
| x86 | 在x86机器上测试 |
| hardware | MaixPy3 API 使用例程 |
| machine_vision | 视觉处理相关,包括机器视觉以及AI处理 |

在使用basic中的脚本时,请首先安装好application里面的 "MaixPy3" 包.  
basic脚本中所依赖的资源文件集中在application/res中,先复制到v831上再运行!



## 开发使用说明
请自行具备 Python 代码开发基础，最好能有 linux C/C++ 开发基础，在下述地址获取开发文档。
- https://wiki.sipeed.com/soft/maixpy3/zh/

- https://wiki.sipeed.com/soft/maixpy3/zh/install/maixii_m2dock/verify.html

- https://wiki.sipeed.com/soft/maixpy3/zh/install/others/develop.html

请先熟读文档学习基础的开发，学会烧录系统和链接板子运行程序，基础使用的问题可以在网上/群里/社区里通过搜索和交流解决。

在确保进入了 Linux 系统，启动了 Python3 后进入开发阶段，此时开发分两个层次，底层 C/C++ 开发，上层 Python 开发，请根据需求查收。

- C/C++ 交叉编译链 https://api.dl.sipeed.com/shareURL/MaixII/SDK/Toolchain
- Python3 交叉编译链 https://github.com/sipeed/MaixPy3/releases/tag/20210613

开发代码以下述最新内容或仓库代码为准：

- https://github.com/sipeed/maixpy3

- https://github.com/sipeed/libmaix

- https://github.com/sipeed/MaixPy3_scripts

libamix 用途是提供给 V831/V833 的底层驱动库，适合有开发经验的开发者。

maixpy3 用途是通用的 Python3 库，提供了许多 steam 需要的模块功能，涵盖 摄像头/屏幕/I2C/SPI 等外设驱动，AI 检测、分类、识别等模块，传统视觉 OPENCV 等功能接口。

MaixPy3_scripts 存放着 Sipeed 对 STEAM 教育环境下的进行的功能开发。

请根据如下顺序进行验证与开发。

- 确定系统 Python3 可用。

- 确定可以直接安装 MaixPy3 包使用。

- 确定开发结果在 SD 卡上，并将其 DD 导出，用于量产复现。



