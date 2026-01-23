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
4. (Optional) Create a `whitelist.txt` file to exclude servers/DMs

---

## 🛡️ Whitelist / Exclusion System

### What is it?

The whitelist allows you to protect specific servers or DMs from deletion. Any server or conversation whose ID is in the whitelist will be **completely excluded** from the deletion process.

### How to Set Up the Whitelist

#### Step 1: Enable Discord Developer Mode

1. Open Discord (web or desktop)
2. Go to **Settings** (⚙️ icon)
3. Go to **Advanced** (or **App Settings → Advanced**)
4. Enable **Developer Mode** (toggle ON)

#### Step 2: Get Server/DM IDs

**For a Server:**
1. Right-click on the server icon (left sidebar)
2. Click **"Copy Server ID"** (or **"Copy ID"**)
3. The ID is now in your clipboard

**For a DM/Conversation:**
1. Right-click on the conversation name
2. Click **"Copy Channel ID"** (or **"Copy ID"**)
3. The ID is now in your clipboard

#### Step 3: Create the Whitelist File

1. In the same folder as `discord_bulk_deleter.py`, create a new file named **`whitelist.txt`**
2. Paste the IDs you want to exclude (one per line)
3. You can add comments with `#`

**Example `whitelist.txt`:**

```txt
# My important servers
123456789012345678
987654321098765432

# Family group chat
111222333444555666

# Work-related DMs
777888999000111222
555666777888999000

# Friend's server - don't touch!
444555666777888999
```

#### Step 4: Run the Script

When you run the script, it will automatically:
- Load the whitelist
- Display how many IDs are excluded
- Remove whitelisted servers/DMs from the selection list

### Features

- ✅ **Automatic exclusion**: Whitelisted servers/DMs don't even appear in the selection list
- ✅ **Comment support**: Lines starting with `#` are ignored
- ✅ **Empty lines ignored**: You can organize your whitelist with blank lines
- ✅ **Statistics**: Shows how many items were excluded
- ✅ **Optional**: If the file doesn't exist, the script works normally without exclusions
- ✅ **Safe**: IDs in whitelist are 100% protected from deletion

### Example Output

When the script runs with a whitelist:

```
✓ Token loaded from 'token.txt'
✓ Whitelist loaded: 5 ID(s) excluded
ℹ Excluded IDs: 123456789012345678, 987654321098765432, 111222333444555666...

ℹ Retrieving server list...
⚠ 2 server(s) excluded by whitelist
✓ 8 server(s) found:

  [1] Gaming Server (ID: 123...)
  [2] Study Group (ID: 456...)
  [3] Music Community (ID: 789...)
  ...
```

### Common Use Cases

- 🏢 **Work servers** - Keep professional communications safe
- 👨‍👩‍👧‍👦 **Family/friend groups** - Protect personal conversations
- 📚 **Important communities** - Preserve membership in key servers
- 💼 **Business contacts** - Don't delete client communications
- 🎮 **Main gaming servers** - Keep your clan/guild intact

### Tips

- Start by adding your most important servers to the whitelist
- Run the script once to see the list - you can always cancel and add more IDs
- Keep a backup copy of your `whitelist.txt` file
- You can enable/disable the whitelist by renaming the file (e.g., `whitelist.txt.bak`)

---

## 🔑 Getting Your Discord Token

### Method 1: Web Browser (discord.com)

1. Open Discord in your browser: https://discord.com/app
2. Press **F12** to open Developer Tools
3. Go to the **Console** tab
4. Paste this code and press Enter:

```javascript
window.webpackChunkdiscord_app.push([
    [Symbol()], {}, req => {
        if (!req.c) return;
        for (let m of Object.values(req.c)) {
            if (!m.exports || m.exports === window) continue;
            if (m.exports?.getToken) return console.log('"' + m.exports.getToken() + '"');
            for (let ex in m.exports) {
                if (m.exports?.[ex]?.getToken && m.exports[ex][Symbol.toStringTag] !== 'IntlMessagesProxy') {
                    return console.log('"' + m.exports.getToken() + '"');
                }
            }
        }
    },
]);
window.webpackChunkdiscord_app.pop();
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
WHITELIST_FILE = "whitelist.txt"      # Whitelist file name
DELAY_BETWEEN_DELETIONS = 1.5         # Seconds between each deletion
DELAY_BETWEEN_REQUESTS = 2.0          # Seconds between API requests
REQ_TIMEOUT = 10                      # HTTP request timeout
MAX_RETRIES = 3                       # Maximum retry attempts
```

### File Structure

```
your_folder/
├── discord_bulk_deleter.py
├── token.txt              # Your Discord token (required)
├── whitelist.txt          # IDs to exclude (optional)
└── messages_*.json        # Backup files (generated if enabled)
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
A: Currently, the script deletes all your messages from selected servers/DMs. Channel-specific deletion is not yet implemented. However, you can use the whitelist to exclude entire servers.
</details>

<details>
<summary><b>Q: How do I protect certain servers from deletion?</b></summary>
<br>
A: Create a `whitelist.txt` file with the server/DM IDs you want to exclude. See the Whitelist section above for details.
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
