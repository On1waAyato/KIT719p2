# Evaluation Report

本报告记录了对职业助手系统的基线与挑战问题测试结果，用于验证路由、RAG 检索以及薪资工具的协同表现。

## Baseline Questions（5）

### B1. 项目经理核心任务（RAG）
1️⃣ **用户问题：** “What are the main tasks of a project manager in the OSCA guide?”
2️⃣ **引用文档位置：** `OSCA_20pages.pdf#chunk1`, `OSCA_20pages.pdf#chunk4`
3️⃣ **手动正确答案：** 该文档指出项目经理需要规划、组织、指导与控制组织内的运营；在 ICT 项目中需编制包含交付物、时间线、资源配置与预算的详细计划，并执行风险管理、技术方案实施与质量管理流程。
4️⃣ **系统输出是否正确：** **Y** – 系统返回了与手动答案一致的要点，并列出了 chunk 引用。

### B2. 澳大利亚项目经理薪资（Tool）
1️⃣ **用户问题：** “What’s the average salary for a project manager in Australia?”
2️⃣ **调用工具结果：** `SalaryTool`（Google Gemini Flash）返回范围：低 120,000 / 中 160,000 / 高 220,000 AUD。
3️⃣ **手动正确答案：** 依据同一工具的快照，澳洲项目经理平均薪资约 160,000 AUD，范围 120,000–220,000 AUD。
4️⃣ **系统输出是否正确：** **Y** – 输出展示了相同的三段式薪资卡片并注明来源为 google-genai。

### B3. 项目经理技能 + 薪资（BOTH）
1️⃣ **用户问题：** “What skills do project managers need and what salary should I expect in Australia?”
2️⃣ **引用文档位置 / 工具：** `OSCA_20pages.pdf#chunk4`；`SalaryTool`（低 90,000 / 中 130,000 / 高 180,000 AUD）。
3️⃣ **手动正确答案：** 需要领导力、项目规划、沟通、团队协作、风险管理与质量保证等技能；薪资范围 90,000–180,000 AUD，平均约 130,000 AUD。
4️⃣ **系统输出是否正确：** **Y** – 路由选择 BOTH，回答中含技能段落（附 chunk 引用）与薪资工具卡片。

### B4. 注册护士职责（RAG）
1️⃣ **用户问题：** “List the typical duties of an enrolled nurse covered by OSCA.”
2️⃣ **引用文档位置：** `OSCA_20pages.pdf#chunk7`
3️⃣ **手动正确答案：** 文档描述护士需提供直接患者护理、给药、监测病情、协助康复，并在多学科团队中协作。
4️⃣ **系统输出是否正确：** **Y** – 返回内容逐项覆盖上述职责并引用 chunk7。

### B5. 澳大利亚护士薪资（Tool）
1️⃣ **用户问题：** “What is the typical salary range for nurses in Australia?”
2️⃣ **调用工具结果：** `SalaryTool` 给出 70,000 / 85,000 / 120,000 AUD。
3️⃣ **手动正确答案：** 工具快照与多渠道公开薪资资料一致，平均约 85,000 AUD。
4️⃣ **系统输出是否正确：** **Y** – 系统呈现相同的范围值并在总结段落中注明工具来源。

## Difficult Questions（3）

### D1. 医疗合规全景（RAG 范围外）
1️⃣ **用户问题：** “What are the regulatory compliance requirements across all healthcare roles in Australia?”
2️⃣ **手动正确答案：** 需要说明常见主题（注册、职业健康安全、隐私等），并强调 OSCA 核心文档只覆盖特定职业，无法提供全面合规指南，建议缩小问题范围。
3️⃣ **系统输出：** 系统给出“未找到相关文档”后仍尝试生成通用段落，缺少明确的范围限制提示。
4️⃣ **失败点分析：** **检索失败 + 覆盖不足。** RAG 只含单一 PDF，路由仍选择 RAG，导致上下文不足且回答未主动声明范围差距。

### D2. 缩写导致路由偏差
1️⃣ **用户问题：** “What skills do PMs need?”
2️⃣ **手动正确答案：** 应先将 “PMs” 解释为 “Project Managers”，再引用 `OSCA_20pages.pdf#chunk4` 说明领导、规划、沟通与风险管理技能。
3️⃣ **系统输出：** Router 将查询判定为 UNKNOWN，仅给出高层次软技能描述，无引用。
4️⃣ **失败点分析：** **路由关键字漏检。** 关键词列表缺少 “PMs” 等缩写，导致未走 RAG 流程；需要在 `router.py` 与 `extract_title()` 中补充同义词。

### D3. 各州薪资细分
1️⃣ **用户问题：** “What’s the average salary for software engineers in each Australian state?”
2️⃣ **手动正确答案：** 工具仅提供全国范围数据，应返回全国平均（如 95,000–140,000 AUD）并说明缺乏州级细分，建议查阅政府数据门户。
3️⃣ **系统输出：** SalaryTool 返回全国范围，系统直接呈现并未解释州级缺失。
4️⃣ **失败点分析：** **工具粒度限制。** 需要在生成提示中加入 fallback 说明或引导用户改用外部数据源。

---

以上结果表明：常规查询在当前语料与工具范围内表现稳定，而对跨领域、缩写及高粒度需求的问题仍需改进路由覆盖与答案模版。
