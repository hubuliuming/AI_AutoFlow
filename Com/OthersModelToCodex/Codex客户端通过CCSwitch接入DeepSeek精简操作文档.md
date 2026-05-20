# Codex 客户端通过 CC Switch 接入 DeepSeek 精简操作文档

## 1. 目标架构

```text
Codex 客户端
    ↓
CC Switch 管理 Codex Provider / Local Routing
    ↓
Moon Bridge 本地 Responses 兼容桥
    ↓
DeepSeek API
```

不要让 Codex 客户端直接填 DeepSeek 官方 API 地址。Codex 需要 OpenAI Responses API，而 DeepSeek 官方接口不能直接作为 Codex Responses Provider 使用；推荐通过 Moon Bridge 转发。

---

## 2. 必要下载与环境

### 2.1 安装 Go

PowerShell 执行：

```powershell
winget install --id GoLang.Go -e
```

安装后关闭 PowerShell，重新打开，检查：

```powershell
go version
```

### 2.2 配置 Go 国内代理

```powershell
go env -w GOPROXY=https://goproxy.cn,direct
go env -w GOSUMDB=sum.golang.google.cn
```

### 2.3 下载 Moon Bridge

```powershell
cd C:\dev
git clone https://github.com/hubuliuming/moon-bridge.git
cd C:\dev\moon-bridge
Copy-Item .\config.example.yml .\config.yml
notepad .\config.yml
```
--- 
原地址：https://github.com/ZhiYi-R/moon-bridge.git

下载的新地址为本人优化过版本

---

### 2.4 安装 CC Switch

优先尝试：

```powershell
winget install -e --id farion1231.CC-Switch
```

如果 winget 找不到，就从 CC Switch 官方 GitHub Releases 下载 Windows 安装包：

```text
https://github.com/farion1231/cc-switch/releases
```

---

## 3. 配置 Moon Bridge

打开：

```text
C:\dev\moon-bridge\config.yml
```

先用最小 DeepSeek 配置，删除示例里多余的 Kimi、visual、其他 provider。

示例：

```yaml
mode: "Transform"

log:
  level: "info"
  format: "text"

server:
  addr: "127.0.0.1:38440"

models:
  deepseek-v4-pro:
    context_window: 1000000
    max_output_tokens: 384000
    display_name: "DeepSeek V4 Pro"
    default_reasoning_level: "high"
    supported_reasoning_levels:
      - effort: "high"
        description: "High reasoning effort"
      - effort: "xhigh"
        description: "Extra high reasoning effort"
    supports_reasoning_summaries: true
    default_reasoning_summary: "auto"
    extensions:
      deepseek_v4:
        enabled: true

providers:
  deepseek:
    base_url: "https://api.deepseek.com/anthropic"
    api_key: "sk-你的DeepSeek密钥"
    protocol: "anthropic"
    version: "2023-06-01"
    offers:
      - model: deepseek-v4-pro

routes:
  moonbridge:
    model: deepseek-v4-pro
    provider: deepseek

defaults:
  model: "moonbridge"
  max_tokens: 8192
```

保存后启动 Moon Bridge：

```powershell
cd C:\dev\moon-bridge
go run ./cmd/moonbridge -config ./config.yml
```

这个窗口不要关闭。

---

## 4. 测试 Moon Bridge 是否正常

另开 PowerShell：

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:38440/v1/models
```

再测试 Responses：

```powershell
$body = @{
  model = "moonbridge"
  input = "请用一句话说明你现在通过 Moon Bridge 工作。"
  max_output_tokens = 100
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
  -Uri http://127.0.0.1:38440/v1/responses `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

能返回内容，说明：

```text
Moon Bridge -> DeepSeek
```

已经通了。

---

## 5. 保护 Codex 客户端默认配置

Codex 客户端会读取用户级配置：

```text
C:\Users\song\.codex\config.toml
```

在修改前备份：

```powershell
cd $HOME\.codex

if (Test-Path ".\config.toml") {
  Copy-Item ".\config.toml" ".\config.toml.bak-$(Get-Date -Format yyyyMMdd-HHmmss)"
}

if (Test-Path ".\models_catalog.json") {
  Copy-Item ".\models_catalog.json" ".\models_catalog.json.bak-$(Get-Date -Format yyyyMMdd-HHmmss)"
}
```

不要手动把 Moon Bridge 生成的极简配置直接覆盖进默认 `.codex`，否则 Codex 客户端可能出现历史加载错误或模型列表异常。

---

## 6. 在 CC Switch 里配置 Codex

打开 CC Switch，进入 Codex 页面。

新增 Provider，填写：

```text
Name:
DeepSeek

Base URL:
http://127.0.0.1:38440/v1

Model:
moonbridge

编写config.tomal内容
重点修改成：

model = "moonbridge"
model_provider = "moonbridge"
model_reasoning_effort = "high"
model_context_window = 1000000
model_auto_compact_token_limit = 900000

[model_providers.moonbridge]
name = "MoonBridge DeepSeek"
base_url = "http://127.0.0.1:38440/v1"
wire_api = "responses"

```

## 7. 启用 CC Switch Local Routing

保存成功config.tomal后 启动
 
---

## 8. 重启 Codex 客户端

不要只关闭窗口，先检查进程：

```powershell
Get-Process | Where-Object { $_.ProcessName -match "codex" } | Select-Object Id,ProcessName,Path
```

强制关闭 Codex 相关进程：

```powershell
Get-Process | Where-Object { $_.ProcessName -match "codex" } | Stop-Process -Force
```

然后重新打开 Codex 客户端。

---

## 9. 验证是否成功

在 Codex 客户端发：

```text
请只回复当前模型名和 provider，不要修改文件。
```

同时看 Moon Bridge 窗口。

成功标志：

```text
POST /v1/responses
```

只要 Moon Bridge 窗口出现这个请求，就说明：

```text
Codex 客户端 -> CC Switch -> Moon Bridge -> DeepSeek
```

已经接通。

---

## 10. 常见问题速查

### 10.1 Codex 只显示 GPT 模型

优先检查：

```text
CC Switch 是否启用了 Codex Local Routing
当前 Provider 是否切到 MoonBridge DeepSeek
Moon Bridge 是否正在运行
Base URL 是否是 http://127.0.0.1:38440/v1
```

### 10.2 Moon Bridge 没有任何请求日志

说明 Codex 客户端没有打到 Moon Bridge。重点检查 CC Switch Local Routing。

### 10.3 Codex 历史加载错误

恢复 `.codex` 备份：

```powershell
cd $HOME\.codex

$latestConfig = Get-ChildItem ".\config.toml.bak-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Copy-Item $latestConfig.FullName ".\config.toml" -Force

if (Get-ChildItem ".\models_catalog.json.bak-*" -ErrorAction SilentlyContinue) {
  $latestCatalog = Get-ChildItem ".\models_catalog.json.bak-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  Copy-Item $latestCatalog.FullName ".\models_catalog.json" -Force
}
```

### 10.4 要不要切 Codex API 登录

不要切。

保持：

```text
Codex = ChatGPT 账号登录
DeepSeek = CC Switch + Moon Bridge 转发
```

Codex 的 API 登录是 OpenAI Platform API Key，不是 DeepSeek Key。

---

## 11. 最终执行顺序

```text
1. 安装 Go
2. 配置 Go 国内代理
3. 下载 Moon Bridge
4. 写入 DeepSeek config.yml
5. 启动 Moon Bridge
6. 测试 /v1/models 和 /v1/responses
7. 安装 CC Switch
8. 备份 C:\Users\song\.codex
9. 在 CC Switch 添加 MoonBridge DeepSeek Provider
10. 启用 Codex Local Routing
11. 重启 Codex 客户端
12. 看 Moon Bridge 是否出现 POST /v1/responses
```

核心原则：

```text
不要直接把 DeepSeek API 填给 Codex
不要手动覆盖默认 .codex
不要切 Codex API 登录
用 CC Switch 管理客户端切换
用 Moon Bridge 做协议转换
```
