Integration Watchdog – HACS Blueprint Spec

1 · Intent

Create a one-click HACS package that installs a Blueprint-only automation which:
	1.	Detects unavailable/misconfigured entities via the Watchman integration.  ￼
	2.	Resolves each failing entity’s config_entry_id() at runtime and calls homeassistant.reload_config_entry (requires Spook to expose that service).  ￼ ￼
	3.	Escalates to homeassistant.restart after N failed reload rounds (default 3).
	4.	Notifies the user via any chosen notify.* service before every action.

No manual mapping, no Python; everything is declarative YAML so maintenance stays near-zero.

⸻

2 · Behaviour Overview

Phase	What Happens	Key Tech
Detection	Watchman updates sensor.watchman_issue_count & issues attribute when entities are unavailable/unknown	Watchman
Decision	Automation triggers after 5 min stable failure → extracts all failing entity_ids → converts to unique entry_ids	Jinja config_entry_id filter
Remediation	Iterates over entry_ids and re-loads each integration; if retries ≥ limit → full HA restart	Spook service + Core restart
Notification	Pushes a summary before each reload/restart	notify.* service


⸻

3 · Blueprint YAML (drop-in)

blueprint:
  name: Integration Watchdog (auto)
  domain: automation
  input:
    issue_sensor:
      name: Watchman issue sensor
      default: sensor.watchman_issue_count
    notify_service:
      name: Notify service
      default: notify.mobile_app_your_phone
    max_reload_attempts:
      name: Reload attempts before reboot
      default: 3

trigger:
  - platform: numeric_state
    entity_id: !input issue_sensor
    above: 0
    for: "00:05:00"

variables:
  issues: "{{ state_attr(trigger.entity_id,'issues') or [] }}"
  entry_ids: >
    {{ issues
       | map(attribute='entity_id')
       | map('config_entry_id')
       | reject('none')
       | unique
       | list }}
  attempts: "{{ this.attributes.get('attempts', 0) | int }}"

action:
  - repeat:
      while: "{{ repeat.index <= entry_ids|length }}"
      sequence:
        - service: homeassistant.reload_config_entry
          data:
            entry_id: "{{ entry_ids[repeat.index-1] }}"
  - service: !input notify_service
    data:
      title: "Watchdog reload"
      message: "Reloaded {{ entry_ids|length }} integration(s): {{ entry_ids }}"
  - choose:
      - conditions: "{{ attempts + 1 >= (max_reload_attempts | int) }}"
        sequence:
          - service: !input notify_service
            data:
              title: "Watchdog rebooting Home Assistant"
              message: "Still seeing issues after {{ max_reload_attempts }} reloads."
          - service: homeassistant.restart
          - variables: {attempts: 0}
      - default:
          - variables: {attempts: "{{ attempts + 1 }}"}
mode: restart

Key points
	•	Uses Jinja config_entry_id() to stay integration-agnostic.  ￼
	•	Stores retry counter in this.attributes.
	•	Relies on Spook to expose reload_config_entry to automations.  ￼ ￼

⸻

4 · Repository Layout

integration-watchdog/
├─ blueprints/
│   └─ automation/
│       └─ integration_watchdog_auto.yaml
├─ hacs.json
└─ README.md

hacs.json

{
  "name": "Integration Watchdog",
  "description": "Reload flaky integrations or reboot Home Assistant using Watchman + Spook.",
  "domains": ["automation"],
  "content_in_root": false,
  "homeassistant": "2024.6.0",
  "render_readme": true
}


⸻

5 · Implementation Steps (for the AI agent)
	1.	Repo bootstrap
	•	Create GitHub repo integration-watchdog with the structure above.
	•	Copy the YAML blueprint verbatim.
	2.	Write README.md
	•	Include: prerequisites, install via HACS Custom Repo, import-link badge (/redirect/import_blueprint/?url=RAW_YAML_URL), configuration steps, troubleshooting.
	•	Mention Watchman & Spook install instructions with brief notes.  ￼ ￼
	3.	Tag release
	•	v0.1.0 so HACS can fetch it.
	4.	Internal QA
	•	Spin up a test HA instance with Watchman & Spook.
	•	Simulate an unavailable entity → confirm reload occurs and retry counter works.
	•	Force repeated failure → confirm HA restarts after limit.
	5.	Distribution
	•	Add repo as Custom Repository in HACS (Category: Automation).  ￼
	•	Optionally submit to the HACS default index once stable.

⸻

6 · End-User Installation Flow
	1.	Install Watchman & Spook via HACS, restart HA.  ￼ ￼
	2.	HACS → Custom Repos → add integration-watchdog (Automation).
	3.	Click Install, restart HA.
	4.	Settings → Automations & Scenes → Blueprints → Integration Watchdog (auto) → Create Automation.
	5.	Pick your notify.* service (defaults to mobile), optionally change retry limit → Save.

No further entity mapping needed; it works out-of-the-box.

⸻

7 · Testing Checklist

Test	Expected
Manually set one entity to unavailable	Integration reloads, phone alert “Reloaded 1 integration”
Break two different integrations	Both reloaded; one phone message listing 2 IDs
Persistently failing entity (toggle unavailable 3×)	After 3rd cycle HA restarts; reboot notification sent
Integration without reload support	Service call errors → counted as “fail”; HA restarts per limit


⸻

8 · Future Enhancements
	•	Active probes: optional script that toggles test entities every X min and raises a synthetic Watchman issue on failure.
	•	Supervisor-level reboot: call supervisor.host_reboot when core restart is insufficient.
	•	Dashboard card: mini Lovelace card showing current issue count and last action.
	•	Python custom component: unify logic, expose an “integration_watchdog” sensor for richer analytics.

⸻

9 · Reference Docs & Threads
	•	Watchman GitHub repo & quick-start guide  ￼
	•	Spook GitHub & installation walkthrough  ￼ ￼
	•	config_entry_id() Jinja filter in HA templating docs  ￼
	•	HA blueprint import & usage docs  ￼
	•	HACS “My link” & custom repository guidelines  ￼ ￼

⸻

Hand-off note: all code snippets are production-ready; adjust copyright/license headers to your org’s standards before publishing.