# 开源软件许可合规检测实践：Apache Commons Lang + ScanCode Toolkit

班级 f250117 ｜ 学号 f25011506 ｜ 姓名 雷施佳

《开源创新思维》平时作业一。选取 Apache 社区开源项目 **Apache Commons Lang 3.21.0**，使用
**ScanCode Toolkit 32.5.0** 进行许可证合规扫描，并给出检测报告与逐项分析。

## 目录结构

```
├── f250117-f25011506-雷施佳-作业1.docx   # 作业报告（封面 + 正文 5 页 + 评价表）
├── f250117-f25011506-雷施佳-作业1.pdf    # 同上，PDF 版
├── scan/
│   ├── scan.json                 # ScanCode 原始扫描结果（1.8 MB）
│   ├── scan_report.html          # ScanCode 生成的 HTML 报告（可直接浏览器打开）
│   └── scan.log                  # 扫描运行日志
├── scripts/
│   ├── analyze.py                # 统计脚本：许可证表达式分布、检出率、得分分布
│   └── chart.py                  # 生成图 1「按文件类型的许可证检出率」
└── report/
    └── fig1_detection_rate.png   # 图 1
```

## 环境与复现步骤

Windows 11 + Python 3.11.9：

```bash
python -m venv .venv-scancode
.venv-scancode\Scripts\python.exe -m pip install scancode-toolkit==32.5.0 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
# 若报 pluggy 相关 ValueError，需降级：
.venv-scancode\Scripts\python.exe -m pip install pluggy==0.13.1 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple
```

获取源码包并扫描：

```bash
# commons-lang3-3.21.0-src.tar.gz 取自 https://mirrors.tuna.tsinghua.edu.cn/apache/commons/lang/source/
tar -xzf commons-lang3-3.21.0-src.tar.gz

.venv-scancode\Scripts\scancode.exe -clpi \
    --json-pp scan.json --html scan_report.html \
    --processes 4 --timeout 120 commons-lang3-3.21.0-src
```

统计与作图：

```bash
python scripts/analyze.py scan/scan.json
python scripts/chart.py
```

## 关键结果

| 指标 | 数值 |
| --- | --- |
| 扫描规模 | 706 个文件、71 个目录、10.04 MB |
| 耗时 | 157.22 s（4 进程并行），错误 0 |
| 检出 Apache-2.0 | 692 个文件（98.02%） |
| 未检出 | 11 个（1.56%），均为图像 / 字节码 / 测试数据 |
| 多重表达式 | 4 个，其中 2 处为 CLA 措辞误报 |
| 版权命中 | 仅 2 处（ASF 源码头不含 Copyright 行，版权集中声明于 NOTICE.txt） |

**结论**：commons-lang3 3.21.0 许可证维度洁净，无 GPL/AGPL/LGPL 等强著佐权成分，可安全作为依赖引入；
再分发时须履行 Apache-2.0 的四项义务（附 LICENSE、保留 NOTICE、标注修改、注意专利终止条款）。

## 安装过程中遇到的四个问题

1. pip 直连 pypi.org 报 `SSL: UNEXPECTED_EOF_WHILE_READING` → 改用清华镜像 + `--trusted-host`。
2. 安装末尾 `OSError: [WinError 5] 拒绝访问`（`.dist-info\INSTALLER`）→ 杀毒软件瞬时占用，
   重执行 `pip install --no-deps scancode-toolkit==32.5.0` 补齐。
3. `ValueError: did not find any 'pre_scan' hooks` → pip 装了 pluggy 1.x，与 plugincode 不兼容，
   降级 `pluggy==0.13.1` 解决。
4. 首次运行需装载许可证知识库（3.02 s）；单进程约 8 分钟，`--processes 4` 后降至 153 s。

## 文件校验（SHA-256）

下载后可用 `sha256sum <文件>` 核对，确认与本次提交的版本一致：

| 文件 | SHA-256 |
| --- | --- |
| `f250117-f25011506-雷施佳-作业1.docx` | `e1f078b8c0e9f9c935ed512a96dba1150bdedb3152b33034103769a90c39df01` |
| `f250117-f25011506-雷施佳-作业1.pdf` | `86b1073639bef965c15ca5fbb306b7f839ff77865ccb289df5bca5e85cd634bb` |
| `scan/scan.json` | `628d3176183011c3cc578835f631a3b5a150ba12aed80c4cd3155ea894a620e2` |
| `scan/scan_report.html` | `178ea83860d5fa804ee809a0e172e1ef6a6f396cf4dfa153c1dec3aaf8c323e7` |
