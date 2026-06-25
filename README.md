# broker-rules-singbox

每日自动从 [Arthur-vx/broker-rules](https://github.com/Arthur-vx/broker-rules) 抓取规则，转换为 [sing-box](https://sing-box.sagernet.org/) rule-set 格式。

覆盖券商：富途/moomoo、长桥、老虎、嘉信。

## 订阅地址

固定指向最新一次构建（`latest` release）：

- JSON（源格式）：`https://github.com/<your-name>/<this-repo>/releases/download/latest/broker.json`
- SRS（编译后）：`https://github.com/<your-name>/<this-repo>/releases/download/latest/broker.srs`

把 `<your-name>/<this-repo>` 换成你 fork/创建后的实际仓库路径。也可以用按日期的 tag（如 `v20260625`）锁定具体某次构建。

## sing-box 配置示例

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "broker",
        "type": "remote",
        "format": "binary",
        "url": "https://github.com/<your-name>/<this-repo>/releases/download/latest/broker.srs",
        "download_detour": "direct",
        "update_interval": "24h"
      }
    ],
    "rules": [
      { "rule_set": "broker", "outbound": "broker-out" }
    ]
  }
}
```

`format: "source"` + `broker.json` 也可以，性能略低于 `binary`。

## 构建逻辑

`.github/workflows/build.yml`：

1. 每天 17:23 UTC（约北京 01:23）跑一次，也支持手动触发
2. 拉取 `Broker.list` → `convert.py` 解析 `IP-CIDR` / `DOMAIN` / `DOMAIN-SUFFIX` → 生成 `broker.json`
3. 下载官方 sing-box CLI → `sing-box rule-set compile` 生成 `broker.srs`
4. 比对 sha256，与上次 release 一致就跳过发布
5. 否则更新 `latest` 这个浮动 release，并打一个按日期的 tag（如 `v20260625`）做历史归档

## 本地构建

```bash
curl -fsSL https://raw.githubusercontent.com/Arthur-vx/broker-rules/main/Broker.list -o Broker.list
python3 convert.py -i Broker.list -o broker.json
# 需要本地装 sing-box CLI 才能编译 .srs
sing-box rule-set compile --output broker.srs broker.json
```

## 致谢

- 规则源：[Arthur-vx/broker-rules](https://github.com/Arthur-vx/broker-rules) by MsMc
- 格式参考：[MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)
