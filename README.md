# Integration Watchdog

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jzarecki/ha-integration-watchdog)](https://github.com/jzarecki/ha-integration-watchdog/releases)

Automatically reloads failing integrations or restarts Home Assistant when they can't be fixed.

**Requirements**: [Watchman](https://github.com/dummylabs/thewatchman) and [Spook](https://github.com/frenck/spook) integrations must be installed first.

## 🎯 What It Does

- Detects failing integrations using Watchman
- Tries to reload broken integrations using Spook
- Restarts Home Assistant after 3 failed attempts
- Sends notifications before each action

## 📦 Installation

[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//raw.githubusercontent.com/jzarecki/ha-integration-watchdog/main/blueprints/automation/integration_watchdog_auto.yaml)

Or install via HACS:
1. HACS → Custom repositories → Add `https://github.com/jzarecki/ha-integration-watchdog`
2. Category: `Automation` → Install

## ⚙️ Setup

1. Go to **Settings** → **Automations & Scenes** → **Blueprints**
2. Find **"Integration Watchdog (auto)"** → **Create Automation**
3. Set your notification service (e.g., `notify.mobile_app_your_phone`)
4. Save

## ⚡ How It Works

1. Watchman detects failing entities and updates `sensor.watchman_issue_count`
2. After 5 minutes of stable failure, the automation triggers
3. It tries to reload each affected integration using Spook
4. If an integration fails 3 times, Home Assistant restarts
5. You get notified before each action

## 🚨 Troubleshooting

- Check Home Assistant notifications (🔔 bell icon) for setup messages
- Make sure Watchman and Spook are configured, not just installed
- Verify `sensor.watchman_issue_count` exists in Developer Tools → States
- Restart Home Assistant after installing Spook

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Dependencies

- [Watchman](https://github.com/dummylabs/thewatchman)
- [Spook](https://github.com/frenck/spook)
- Home Assistant 2024.6.0+