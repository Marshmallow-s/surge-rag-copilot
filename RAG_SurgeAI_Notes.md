# 项目① RAG on Surge AI — 执行笔记

> 目标定位:**AI Engineer**(不是 FDE)。
> 这是 AI Engineer 转型路径上的第一个项目。完整层级 + 路径见 `AI_Engineer_Learning_Path.md`;这份是项目①的独立动手笔记,self-contained,动手时开这一份。

---

## 0. 一句话项目定义

爬 Surge AI 的公开 docs + 技术 blog,建一个「关于 Surge 的 RLHF / data labeling 做法」的问答系统。用户问一个问题(如「Surge 怎么做 red teaming」),系统检索相关文档片段,LLM 基于片段给出有依据、可溯源的答案。

**它在 AI stack 里是 RAG 模式**,市场 #1 in-demand(35.9% 的 JD 提它),补的是我 portfolio 的真空。

---

## 1. 这个项目要练什么(对照能力层级)

> 层级定义见主文档。这里只列项目①实际会碰到的格子。

- **L1 LLM 基础**:API call · structured output · prompt(Step 1, 3)
- **L2 RAG**:ingestion · chunking · search/retrieval(Step 2, 3)── 项目主攻
- **L0a 学一次概念**:Docker 基础 + cloud 最浅层(Step 6)── 第一次学,永久复用
- **L0b 套一遍的壳**:evaluation · testing · CI/CD · deploy · observability(Step 4, 5, 6)

**机制**:L0 不前置单独学,在项目里需要它的那一步才触发。做 RAG 做到「要 deploy 了」才去学 Docker,学了立刻用上。

---

## 2. 为什么 domain 选 Surge AI(已锁定)

**决策标准(我自己定的):** 「哪家在 data feeding / 数据这一层能教我更多 + 文档多不多、透不透明」。不是「跟我 eval harness 连不连贯」。

**为什么 Surge 而非 Labelbox:**
- **data feeding 知识密度更高**:Surge 是 RLHF 执行引擎,深度嵌进 frontier 模型研发循环(给 Anthropic 做 RLHF、red teaming、model evaluation);Labelbox 偏平台/流程管控。我想深挖「数据怎么喂给模型训练」,Surge 教我的更前沿。
- **文档透明度过关(关键 gate,已验证)**:三类能爬的真原料 ──
  1. GitHub `surge-documentation`(API 静态文档,RAG 最干净的原料)
  2. 大量 RLHF / red teaming / 模型评估深度 blog(既是 RAG 原料、又是我要学的 data feeding 知识本身)
  3. GitHub 公开 safety / toxicity 数据集
- **量够大**:docs + blog 合起来塞不进单次 context → 撑得住「为什么需要 RAG 而非 long-context」这个 trade-off 论证。

**知情接受的代价:** Surge 没有 warm contact(Labelbox 有 Gandharv)。但 warm contact 属于「面试挂回」这条独立轴,不是我这次降权的「主题连贯」。这个项目首要目的是「学到 data feeding 真知识」,挂回用别的线补(Mercor 有 Harwinder)。

---

## 3. Step-by-step(动手主体)

> 每步标:**爬哪格 · Claude Code 帮我做 · 我自己必须懂**。
> 最后一列是底线 ── 那些是项目灵魂,不能外包给 AI,否则面试一问就穿。

### Step 0 — 建 repo 骨架(半天)
- **动作**:本地建文件夹 + 空 README + `git init` → push 到 GitHub 建公开 repo。
- **爬哪格**:无,纯起步。
- **Claude Code 做**:`.gitignore`、目录结构(data / ingestion / retrieval / app / eval)、空 README 模板。
- **我必须懂**:目录为什么这么分。
- **产出**:能 push 的空骨架。

### Step 1 — L1:调通一个 LLM API(半天-1 天)
- **动作**:最小脚本发一个 request 给 LLM,拿回 structured output(JSON)。
- **爬哪格**:**L1**。
- **Claude Code 做**:调用样板、API key 处理、解析返回。
- **我必须懂**:一次 API 调用概念上发生什么(我发了什么、模型返回什么、token 是什么、为什么要 structured output)。**项目第一个动作,卡这后面全卡。**
- **产出**:能稳定调通一次 LLM、拿回结构化结果。
- **注**:eval harness 调过 LLM 生成 SQL,这步大概率快。

### Step 2 — L2 上半:ingestion(爬 + 切片)(2-3 天)
- **动作**:① 爬 Surge docs + blog 存本地;② 长文档切 chunk。
- **爬哪格**:**L2**(ingestion + chunking)。「RAG 难在搜索」的源头,数据进得干不干净决定一切。
- **Claude Code 做**:爬虫、chunking 逻辑(按段落/token 数切)。
- **我必须懂**:① 为什么切片(不能整篇塞);② chunk 切多大、重不重叠,怎么影响检索质量(**deep-dive 必问的 trade-off,不能外包**);③ 爬下来脏不脏(空页、导航噪声)── **validation 主场,别浪费**。
- **产出**:干净的、切好片的 Surge 文档 chunk。

### Step 3 — L2 下半:search + 检索(2-3 天)
- **动作**:① chunk 建可搜索索引(vector search,或先用简单 text search);② 给问题搜出最相关 chunk;③ chunk + 问题拼 prompt,调 LLM(复用 Step 1)生成答案。
- **爬哪格**:**L2**(search/retrieval)+ 串 L1。
- **Claude Code 做**:embedding + 向量检索、prompt 拼接。
- **我必须懂**:① vector search 在做什么(文本变向量、按相似度搜)── 概念层,不用懂数学;② 检索出的 chunk 相不相关(**validation 主场**);③ 为什么比「整库塞 context」好(成本/速度/可溯源)。
- **产出**:能跑通的 RAG ── 问问题 → 搜文档 → 出有依据的答案。**到这 MVP 核心完成,项目「能用」了。**

### Step 4 — L0b:evaluation(2-3 天)
- **动作**:建小 golden set(15-20 个「问题 + 期望答案要点」),跑 RAG,LLM-as-judge 打分(相不相关、有没有依据、有没有幻觉)。
- **触发**:**L0b evaluation**。source:「没有 eval 的 RAG 是不完整的项目」。把项目从玩具抬成合格。
- **Claude Code 做**:judge 调用、打分汇总。
- **我必须懂**:① 怎么定义「一个答案算好」(评分标准我设计,**项目灵魂,不能外包**);② 看判分对不对(validation 主场)。
- **产出**:scorecard ──「我的 RAG 在 X 类问题准确率 Y%」。**相对只搭 prototype 的人的差异化。**
- **注**:golden set / LLM-as-judge 我做 eval harness 时熟,套到 RAG 上会快。

### Step 5 — L0b:test + CI/CD(1-2 天)
- **动作**:写几个 pytest(ingestion 没崩、检索返回非空、关键问题答案含预期要点)→ 让 Claude 包成 GitHub Actions。
- **触发**:**L0b testing + CI/CD**。source:「有 test 后包成 Actions 是 5 分钟的事」。
- **Claude Code 做**:test 样板、`.github/workflows` yaml。
- **我必须懂**:每个 test 测什么、为什么(test 是我 UAT/validation 本能换语法)。
- **产出**:repo 上绿色 CI badge,每次 push 自动跑测试。

### Step 6 — L0a + L0b:deploy + observability(2-3 天)
- **动作**:① Streamlit 包能点的界面(输入问题 → 看答案 + 来源 chunk);② 接 Logfire 看每次调用 cost/latency;③ deploy 上线拿 link。可选:deploy 跑 GCP,顺便认识云。
- **触发**:**L0a(Docker 基础 + cloud 最浅层)+ L0b(Streamlit deploy + Logfire)**。第一次完整学 L0a,永久复用。
- **Claude Code 做**:Streamlit app、Logfire 配置、Dockerfile、deploy 步骤。
- **我必须懂**:① Docker 在做什么(把项目打包成到处能跑的盒子)── 概念层,不深;② deploy 后跑在哪;③ Logfire 里 cost/latency 怎么读。
- **产出**:**一个能点的 demo link**(source 说这是 gold)+ 监控面板。

### Step 7 — README(1 天,最重要)
- **动作**:写给两类读者(peer reviewer + 没时间的 HM)。
- **触发**:无新能力,但 source 眼里**最重要的文件**。
- **Claude Code 做**:初稿。**我必须大改** ── AI 生成的 README 一眼能认出来、混废话。
- **我必须自己写**:① 解什么真问题、为什么需要 RAG 而非 long-context(trade-off 是我思考的证明);② 直接链到关键部分(prompts / 检索逻辑 / eval scorecard);③ 放 demo link、CI badge、架构图或截图。
- **产出**:5 分钟能扫懂的 README。

---

## 4. 时间预算与 MVP 边界

- **总时长**:~2 周(L1/eval 有底子可能更快;L0a 第一次学可能拖一点,正常)。
- **MVP 边界**:**Step 0-4 跑通 = 能用的 RAG;Step 5-7 = 抬成「HM 会停下」的合格项目。** Step 1-7 全做完 = 项目①完成。
- **别过度工程**:不上 K8s、不上多模型、不追生产级规模。source 明说个人项目搞生产级基建是 over-engineering、显得 forced。

---

## 5. 防自己踩的坑(这个项目专属)

- **chunking 和检索质量的 trade-off 必须我自己懂** ── deep-dive 必问、最能体现 judgment,不能 vibe coding 到说不清。
- **validation 本能是隐藏王牌** ── 数据脏不脏、chunk 对不对、检索准不准、judge 判得对不对,全是我 ZS 主场。别只当「调 API 的人」,要当「判断这套 pipeline 对不对的人」。
- **demo link > 一切花哨** ── 时间不够时先保 demo link + README,后保其他。
- **每段 AI 生成代码停下来问「这在做什么」** ── 面试要能 steer + review,「一次就成功」会被质疑。
- **commit history 没人看** ── 别设计 commit 节奏,精力放 README + demo link。

---

## 6. 完成后接什么

- 项目① 做完,**L0a 永久会了、L0b 套过一遍**,项目②(brand-visibility agent,L3)只需爬 L3 + 复用 L0,负担小很多。
- 项目② 可用同一 domain 思路(测 Surge 或 Profound 在 LLM 里的可见度)让叙事连贯,但**数据源不同、各做各的完整项目**,别一份数据硬撑两个。

---

## 7. 待定 / 开工前要拍的小决定

- **Step 1 用哪个 API**:OpenAI 还是 Claude?(看手上有哪个 key / 想用哪个)
- **检索先简单还是直接 vector**:可以 Step 3 先用简单 text search 跑通,再升级 vector(降低第一次的复杂度)。
- **要不要 deploy 上 GCP**:Step 6 可选,想认识云就上,想快就先 Streamlit Cloud。