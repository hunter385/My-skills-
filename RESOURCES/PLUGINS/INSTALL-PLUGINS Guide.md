# Installing Your CoWork OS Plugins

CoWork OS plugins install from the Better Creating marketplace. The marketplace always has the latest plugins available for your system.

**One thing first:** plugins require a paid Claude plan — Pro, Max, Team, or Enterprise. If you're on the free plan, you'll need to upgrade before you can install.

There are three ways to install them.

---

## Option 1: Install from the Better Creating Marketplace (recommended)

This is the easiest way for most people.

1. Open a CoWork session in the Claude desktop app
2. Click **Customise** (the sliders icon in the bottom-left of the sidebar)
3. Go to **Plugins**
4. Click the **+** button next to "Personal plugins"
5. Hover over **Create plugin**, then select **Add marketplace** from the submenu (yes, "Add marketplace" lives inside "Create plugin" — that's just where Anthropic put it, you're in the right place)
6. Enter: `bettercreating/cowork-os-plugins`
7. Click **Sync**
8. You'll see a safety notice — this is normal (see below). Click **Sync** to confirm
9. Now click **Browse plugins** and go to the **Personal** tab
10. You'll see both plugins listed under Better Creating — click the **+** on each one to install

That's it — your plugins are now ready to use.

---

## Option 2: Install from the Claude Code tab (desktop app)

If you're using the Claude Code tab inside the Claude desktop app, the process is exactly the same as Option 1. Open **Customise → Plugins**, follow steps 4–10 above, and you're done. Same marketplace address (`bettercreating/cowork-os-plugins`), same plugins, same outcome.

This is different from Option 3, which uses Claude Code in your terminal.

---

## Option 3: Install from the Terminal (Claude Code)

Prefer the terminal? You can install the Better Creating marketplace and its plugins entirely from inside a Claude Code session. The result is identical to the desktop methods — same plugins, same updates, same everything. Use this option if you live in the terminal anyway, or if the desktop install isn't behaving for some reason.

You don't need to be a developer to do this. You just need Claude Code installed, and you need to be able to type a few commands.

---

### Before you start

Open Claude Code in your terminal as you normally would. You should see the chat prompt where you'd usually type your message to Claude. The commands below are typed into that prompt — they start with a forward slash (`/`), which tells Claude Code you're running a built-in command rather than chatting.

---

### Step 1 — Add the Better Creating marketplace

In the Claude Code prompt, type:

```
/plugin marketplace add bettercreating/cowork-os-plugins
```

Press Enter. Claude Code will fetch the marketplace and show you a safety notice (the same warning you'd see in the desktop app — it appears for every non-Anthropic marketplace and isn't specific to CoWork OS). Confirm when prompted.

Once it's added, Claude Code will tell you the marketplace was added successfully.

---

### Step 2 — Install the plugins

Still in the Claude Code prompt, install each plugin one at a time:

```
/plugin install personal-assistant@better-creating
```

```
/plugin install specialist-sub-agent-builder@better-creating
```

Each one should confirm with a success message and tell you what skills and commands the plugin has activated.

---

### Step 3 — Check it worked

Type:

```
/plugin
```

You should see both plugins listed as installed. Their slash commands (`/briefing`, `/eod`, `/tasks`, and so on) are now available — try one to confirm it fires.

That's it — you're set up.

---

### A note on `@better-creating`

The bit after the `@` is the marketplace's internal name (set in its manifest), not the GitHub repo path. So even though you added the marketplace using `bettercreating/cowork-os-plugins`, you install plugins from it using `@better-creating`. Don't worry about why — just type it as written above.

---

## About the Safety Warning

Whichever option you use, when you add the marketplace or install a plugin, you'll see a warning from Anthropic saying they can't guarantee the safety of third-party plugins. This appears for every plugin that isn't in Anthropic's official marketplace — it's not specific to CoWork OS. The plugins included here were built by Simon at Better Creating and only contain text-based instructions and connections to your own tools. Nothing risky. Just click confirm and you're good to go.

---

## Keeping plugins up to date

When Better Creating ships a new version of a plugin, or adds a new one to the marketplace, here's how to get it.

**Desktop (Cowork or Claude Code tab):** Open Customise → Plugins. Find the Better Creating marketplace and click **Sync** to refresh it. New plugins will appear in the Personal tab — click the **+** to install. Updated versions of plugins you already have pull in automatically once the marketplace is synced.

**Terminal:** Re-run `/plugin marketplace add bettercreating/cowork-os-plugins` to refresh the marketplace listing. Any new plugins are then installable with `/plugin install <plugin-name>@better-creating`. Updated versions of plugins you already have refresh automatically.

---

## Troubleshooting

**Desktop install issues**

*"Add marketplace" doesn't appear when I click +*
You need to hover over **Create plugin** first — the menu expands to show "Add marketplace" inside it. Yes, this is a slightly weird UI choice from Anthropic.

*The marketplace doesn't appear after I click Sync*
Check the address you typed: `bettercreating/cowork-os-plugins`. Watch for typos and the hyphen. If it's correct, close and reopen the Claude desktop app — the marketplace should appear after a restart.

*Plugins don't show in the Personal tab*
After adding the marketplace, click **Browse plugins** and switch to the **Personal** tab. If they're still not there, close and reopen the Claude desktop app.

*Plugin installs but slash commands don't work*
Close and reopen the Claude desktop app. Skills and commands register on startup.

**Terminal install issues**

*"Marketplace not found"*
Double-check the address: `bettercreating/cowork-os-plugins`. Watch for typos and the hyphen.

*"Plugin not found in marketplace"*
The plugin name needs the `@better-creating` suffix. Without it, Claude Code doesn't know which marketplace to look in.

*Slash commands don't appear after install*
Quit Claude Code (Ctrl+C or close the terminal) and reopen it. The commands register on startup.

**Still stuck?**
Email Simon and Liza at notion@bettercreating.com — include the exact step you were on and any error message you saw.
