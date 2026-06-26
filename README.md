# broker-rules-singbox

每日自动从 [Arthur-vx/broker-rules](https://github.com/Arthur-vx/broker-rules) 抓取规则，转换为 [sing-box](https://sing-box.sagernet.org/) rule-set 格式。

覆盖券商：富途/moomoo、长桥、老虎、嘉信。

## 订阅地址

固定链接：

- JSON（源格式）：`https://github.com/vcdlk/broker-rules-singbox/releases/download/latest/broker.json`
- SRS（编译后）：`https://github.com/vcdlk/broker-rules-singbox/releases/download/latest/broker.srs`

`latest` 适合长期订阅；`v20260625` 这类按日期 tag 只用于锁定历史版本。

## sing-box 配置示例

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "broker",
        "type": "remote",
        "format": "binary",
        "url": "https://github.com/vcdlk/broker-rules-singbox/releases/download/latest/broker.srs",
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

GitHub Actions 每天自动抓取上游 `Broker.list`，生成 `broker.json` 和 `broker.srs`。内容有变化时更新 `latest` release，同时保留一个按日期命名的历史 tag。

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
