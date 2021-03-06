# 技术规范 | The Missing Semester 中译组

> 此规范本着简短、到位的观点制订，可以全部阅读，也可以只阅读相关的部分。

- [仓库管理说明](#仓库管理说明)

- [翻译](#翻译)

	- [文本排版](#文本排版)
	
	- [内容排版](#内容排版)

- [校对](#校对)

- [时间轴](#时间轴)

## 仓库管理说明

建立分支（branch）时，用如下格式处理：

`(T/R/L/E)_ch(0,1,2...)_ID`

T 翻译 R 校对 L 时间轴 E 压制

例子：`L_ch5_GNAQ`

	校对时可以改为 R_ch?_翻译ID_校对ID

翻译建立新分支时，从 master 签出（checkout）。

~~校对和轴处理文本时，从对应翻译的分支签出，完毕后提 Pull Request 给**对应分支**。~~ 

时间轴从 master 签出分支，对已经校对完成的内容打轴。

翻译和时间轴完成之后，向 master 提 PR。

文件命名时，使用 `[xxx-xxx]CHN.txt` 处理翻译。

使用 `[xxx-xxx]major/minor.sub` 处理时间轴。

## 翻译

翻译时请勿参照全文机翻。

翻译时如有不确定内容，可以在**行末**使用 `# REVIEW` 的格式请求校对协助完成。

### 文本排版

#### 1. 标点

使用括号包裹内容的时候（无论其中是中英文），均用中文小括号。

枚举内容时看文本长度，酌情使用中文顿号或 / 正斜杠。

除下文情况外，不使用**中文中括号**和**任何**大括号。

- 中括号：标记提示点（见下文）
	
- 大括号：当原文的代码内容含有大括号

说明语气时每行文本结尾只能出现 ！？；（中文） !?;（英文）…… 等这些字符。不出现句号、逗号。说明代码时，无限制。

#### 2. 中、英、代码混排

中、英、数字、代码混排时，中文、英文、数字和代码之间有一个空格。

- 例子 demo `echo demo` 123 `cat` 例子 ipv4 例子 BeautifulSoup4

#### 3. 文本长度

每行文本的**汉字**数量控制在 25 个字以下。**但可据断句安排酌情打破。**

**硬性要求**：打轴时，若出现文本速度（字/秒）超过 16 的情况，将由校对和翻译重新讨论此处的翻译内容，并将速度减少到 16 以下。

### 内容排版

**两行文本之间空一行**

#### 1. 代码高亮的使用

主、副字幕的代码高亮使用 \`\` 触发。请勿嵌套使用代码高亮。

在 `代码 / 文件 / 按键 / 命令名` 等处使用高亮。

普通技术名词、人名等不使用高亮。

#### 2. 注释的使用

主字幕是屏幕下方的字幕，副字幕在屏幕上方，做注释用。如有注释，请在须注释处使用 `[*]` 符号，并紧贴一行写入注释。每行主字幕只允许对应一行副字幕。

例子：

	我知道吗？
	
	我知道[*]
	*实际上我不知道
	
	那也没办法

#### 3. 标记提示点

酌情每间隔 10 - 30 行做提示点。用 【--】 表示，置于行首。

括号内填对应的英文字幕 SRT 格式中的**原始行数**。**不需要严格对齐**（见一个可行的例子）

	822
	it's useful. Another one is apple.
	
	————
	
	建了果园，而且这很管用。
	
	【822】另一个是苹果。
	
## 校对

校对分为润色和技术两类。

润色校对浏览全文，修正不规范的翻译格式、裁短过长的单行文本、修正不通顺的句子。

技术校对针对 REVIRW tag 进行纠正，做出精细准确的调整。

修改量少时，校对可以和翻译讨论措辞，但翻译无权决定校对修改的文本。

大规模的修改：多句（>3）重翻、多句（>5）顺序互换时，**需要和翻译讨论达成共识。**

## 时间轴

使用 Aegisub 3.2.2 打轴。Aegisub 使用方法详见网络。

输出格式为 `.sub` 文件，按**帧**而非**时间**打轴。**输出时帧速率选择 `从视频获得`**

主字幕、副字幕分别打 `major.sub` 和 `minor.sub`，副字幕和相对应的主字幕需要同时出现消失。