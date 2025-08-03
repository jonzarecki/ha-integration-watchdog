# Integration Watchdog

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jzarecki/ha-integration-watchdog)](https://github.com/jzarecki/ha-integration-watchdog/releases)

> **One-click HACS package** that automatically reloads failing integrations or restarts Home Assistant using Watchman + Spook. Zero manual configuration required.

> ⚠️ **CRITICAL DEPENDENCIES**: This blueprint requires **Watchman** and **Spook** integrations to function. Install these first via HACS or the blueprint will fail!

## 🎯 What It Does

This Blueprint automation:

1. **Detects** unavailable/misconfigured entities via the [Watchman integration](https://github.com/dummylabs/thewatchman)
2. **Resolves** each failing entity's `config_entry_id()` at runtime and calls `homeassistant.reload_config_entry` (requires [Spook integration](https://github.com/frenck/spook))
3. **Escalates** to `homeassistant.restart` after N failed reload rounds (default: 3)
4. **Notifies** you via any chosen `notify.*` service before every action

No manual mapping, no Python; everything is declarative YAML so maintenance stays near-zero.

## 🚀 Quick Start

**Just install it!** The automation will guide you through any missing dependencies.

### Installation

#### Option 1: One-Click Import
[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//raw.githubusercontent.com/jzarecki/ha-integration-watchdog/main/blueprints/automation/integration_watchdog_auto.yaml)

#### Option 2: HACS Custom Repository
1. HACS → ⋮ → Custom repositories
2. Repository: `https://github.com/jzarecki/ha-integration-watchdog`
3. Category: `Automation`
4. Add → Install → Restart HA

### Setup Automation

1. **Settings** → **Automations & Scenes** → **Blueprints**
2. Find **"Integration Watchdog (auto)"** → **Create Automation**  
3. Configure:
   - **Notify service**: Your preferred notification (e.g., `notify.mobile_app_your_phone`)
   - Leave other settings as defaults
4. **Save** → The automation will guide you through any missing dependencies via Home Assistant notifications!

## ⚡ How It Works

| Phase | What Happens | Technology |
|-------|-------------|------------|
| **Detection** | Watchman updates `sensor.watchman_issue_count` & `issues` attribute when entities are unavailable/unknown | Watchman |
| **Decision** | Automation triggers after 5 min stable failure → extracts all failing `entity_ids` → converts to unique `entry_ids` | Jinja `config_entry_id` filter |
| **Remediation** | Iterates over `entry_ids` and re-loads each integration; if retries ≥ limit → full HA restart | Spook service + Core restart |
| **Notification** | Pushes a summary before each reload/restart | `notify.*` service |

## ⚙️ How It Works After Setup

Once dependencies are installed, the automation will:

| Scenario | What Happens |
|----------|-------------|
| Entity becomes unavailable | Waits 5 minutes → Reloads integration → Notifies you |
| Multiple entities fail | Reloads all affected integrations → Single summary notification |
| Integration keeps failing | After 3 attempts → Restarts Home Assistant → Notifies you |
| Everything working | Runs quietly in background → No notifications |

## 🚨 Troubleshooting

**The automation should guide you through setup automatically.** If you're still having issues:

### Common Issues

#### Not Getting Setup Messages
- ✅ Setup messages appear as **Home Assistant notifications** (not phone alerts)
- ✅ Check the 🔔 bell icon in your HA interface for persistent notifications
- ✅ Try turning the automation off and on again if stuck

#### Setup Keeps Running Despite Dependencies Installed
- ✅ Make sure both integrations are **configured**, not just installed
- ✅ Check `sensor.watchman_issue_count` exists in Developer Tools → States  
- ✅ Restart Home Assistant after installing Spook
- ✅ Setup checks after each HA restart and every 30 minutes

## 🔮 Future Enhancements

- **Active probes**: Optional script that toggles test entities every X min
- **Supervisor-level reboot**: Call `supervisor.host_reboot` when core restart insufficient
- **Dashboard card**: Mini Lovelace card showing current issue count and last action
- **Python custom component**: Unify logic, expose an "integration_watchdog" sensor

## 🤝 Contributing

Contributions welcome! Please check our [Contributing Guide](CONTRIBUTING.md) for development setup and guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Dependencies

- [Watchman](https://github.com/dummylabs/thewatchman) - Entity monitoring
- [Spook](https://github.com/frenck/spook) - Advanced HA services
- Home Assistant 2024.6.0+ - For Jinja `config_entry_id()` filter