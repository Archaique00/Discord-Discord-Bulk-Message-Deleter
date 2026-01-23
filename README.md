# 🗑️ Discord Bulk Message Deleter

Automatically delete all your Discord messages on selected servers and private conversations.

## ✨ Features

- ✅ **Bulk message deletion** (servers + DMs)
- 📊 **Two modes**: Automatic (batch) or Verification mode
- 💾 **JSON backup** of scraped messages
- 🎯 **Selective deletion** (choose specific servers/DMs)
- 🛡️ **Whitelist/Exclusion system** (protect important servers/DMs)
- 📈 **Detailed statistics** and success rate
- ⚡ **Automatic rate limit handling**
- 🔄 **Smart retry** on network errors
- 🎨 **Colorful terminal interface**

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- `requests` library

```bash
pip install requests
```

### Installation

1. Download `discord_bulk_deleter.py`
2. Create a `token.txt` file in the same directory
3. Add your Discord token to `token.txt`

---

## 🔑 Getting Your Discord Token

### Method 1: Web Browser (discord.com)

1. Open Discord in your browser: https://discord.com/app
2. Press **F12** to open Developer Tools
3. Go to the **Console** tab
4. Paste this code and press Enter:

```javascript
(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
```

5. Your token appears in quotes
6. Copy it (without quotes) and paste into `token.txt`

### Method 2: Desktop App

1. Open Discord Desktop
2. Press **Ctrl+Shift+I** (Windows/Linux) or **Cmd+Option+I** (Mac)
3. Go to the **Console** tab
4. Follow steps 4-6 from Method 1

---

## 📖 Usage Guide

### Step 1: Launch the script

```bash
python discord_bulk_deleter.py
```

If `token.txt` doesn't exist, the script will offer to create it.

### Step 2: Choose deletion scope

```
1. Servers
2. Messages privés (MPs)
3. Les deux
```

### Step 3: Select deletion mode

- **Automatic (batch)** - Delete everything without confirmation
- **Verification** - Preview 5 messages and confirm with "YES" or "skip"

### Step 4: Backup option

Choose whether to keep or delete JSON files after deletion.

### Step 5: Select targets

- Enter numbers: `1,3,5` for specific servers/DMs
- Enter `all` to process everything

### Step 6: Review statistics

At the end, you'll see:
- Total messages scraped
- Total messages deleted
- Success rate
- Number of servers/DMs processed

---

## ⚠️ Security Warnings

> [!CAUTION]
> - **NEVER share your Discord token with anyone**
> - Your token = full access to your Discord account
> - If compromised, change your Discord password immediately
> - This script runs locally - no data is sent to third parties

### Best Practices

- Keep your `token.txt` file private
- Add `token.txt` to `.gitignore` if using version control
- Use this tool responsibly
- Rate limits are handled automatically to avoid API abuse

### Legal Notice

> [!WARNING]
> This tool is for personal use only. By using it, you acknowledge:
> - You're responsible for compliance with Discord's Terms of Service
> - Bulk deletion may violate Discord's policies
> - Use at your own risk

---

## 🐛 Troubleshooting

### Token Invalid or Expired
- Verify you copied the complete token
- Check for extra spaces or quotes
- Token must be at least 50 characters
- Try regenerating by logging out and back in

### Rate Limit Errors
- The script handles rate limits automatically
- If persistent, increase `DELAY_BETWEEN_DELETIONS` in the code (default: 1.5s)

### Permission Errors
- Some channels may not be accessible with your permissions
- The script will skip inaccessible content and continue

### Network Errors
- Script includes automatic retry logic (3 attempts)
- Check your internet connection
- Discord API may be temporarily unavailable

---

## 📊 Output Files

| Filename Format | Contents |
|----------------|----------|
| `messages_LocationName_YYYYMMDD_HHMMSS.json` | Message ID, content, timestamp, attachments, channel info |

**Note**: JSON files are automatically deleted if you choose not to save backups.

---

## ⚙️ Configuration

You can modify these settings at the top of the script:

```python
TOKEN_FILE = "token.txt"              # Token file name
DELAY_BETWEEN_DELETIONS = 1.5         # Seconds between each deletion
DELAY_BETWEEN_REQUESTS = 2.0          # Seconds between API requests
REQ_TIMEOUT = 10                      # HTTP request timeout
MAX_RETRIES = 3                       # Maximum retry attempts
```

---

## ❓ FAQ

<details>
<summary><b>Q: Will I get banned for using this tool?</b></summary>
<br>
A: Using self-bots and automation tools violates Discord's ToS. Use at your own risk.
</details>

<details>
<summary><b>Q: How fast can I delete messages?</b></summary>
<br>
A: Rate limits apply. The script uses 1.5s delay between deletions by default.
</details>

<details>
<summary><b>Q: Can I recover deleted messages?</b></summary>
<br>
A: No. Enable JSON backup if you want to keep a record before deletion.
</details>

<details>
<summary><b>Q: Does this work on mobile?</b></summary>
<br>
A: No, this is a Python script for desktop use only.
</details>

<details>
<summary><b>Q: Can I select specific channels within a server?</b></summary>
<br>
A: Currently, the script deletes all your messages from selected servers/DMs. Channel-specific deletion is not yet implemented.
</details>

<details>
<summary><b>Q: What happens if the script crashes mid-deletion?</b></summary>
<br>
A: Simply re-run the script. It will re-scrape messages and continue. Already deleted messages won't appear in the new scrape.
</details>

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues first
- Provide error logs and steps to reproduce

---

## 📝 License

This project is provided as-is for educational purposes. Use responsibly.

---

**⚡ Remember: With great power comes great responsibility. Use this tool wisely!**
