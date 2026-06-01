## Option 3: Install from the Terminal (Claude Code)

Prefer the terminal? You can install the Better Creating marketplace and its plugins entirely from inside a Claude Code session. The result is identical to the desktop method — same plugins, same updates, same everything. Use this option if you live in the terminal anyway, or if the desktop install isn't behaving for some reason.

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

Press Enter. Claude Code will fetch the marketplace and show you a safety notice (this is the same warning you'd see in the desktop app — it appears for every non-Anthropic marketplace and isn't specific to CoWork OS). Confirm when prompted.

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

That's it — you're set up. Your plugins will pull updates automatically from the marketplace, the same as the desktop method.

---

### A note on `@better-creating`

The bit after the `@` is the marketplace's internal name (set in its manifest), not the GitHub repo path. So even though you added the marketplace using `bettercreating/cowork-os-plugins`, you install plugins from it using `@better-creating`. Don't worry about why — just type it as written above.

---

### Troubleshooting

**"Marketplace not found"**
Double-check the address: `bettercreating/cowork-os-plugins`. Watch for typos and the hyphen.

**"Plugin not found in marketplace"**
The plugin name needs the `@better-creating` suffix. Without it, Claude Code doesn't know which marketplace to look in.

**Slash commands don't appear after install**
Quit Claude Code (Ctrl+C or close the terminal) and reopen it. The commands register on startup.

**Still stuck?**
Email Simon at notion@bettercreating.com — include the exact command you ran and the error message you saw.
