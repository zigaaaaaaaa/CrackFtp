# CrackFTP - FTP Login Tester

This Python script is designed to automate the process of testing FTP server logins using credentials provided in an input file. It checks if the domain belongs to a secure category (e.g., .gov, .edu, .org) and sends an alert via Telegram when a successful FTP login is made on a secure domain. Failed and successful logins are logged into separate files.

**GitHub Repository:** [HackfutSec/CrackFtp](https://github.com/HackfutSec/CrackFtp.git)

## Features

- **Domain Security Check:** Verifies if the FTP host belongs to a secure domain such as `.gov`, `.edu`, `.gouv`, `.org`, etc.
- **Multiple Input Formats Supported:**
  1. `host:user:password`
  2. `host:user:password:port`
  3. `host - user;password - port`
  4. `ftp://hostname;user;pass`
  5. `Host: hostname identifier et ce message apparait enleve le automatiquement partout (Status code: 200) User: Username Password: password`
- **Telegram Alerts:** Sends Telegram messages if login is successful on a secure domain.
- **Login Results:** Saves successful logins to `Good_Ftp.txt` and failed logins to `Bad_Ftp.txt`.
- **File Permissions Info:** Retrieves file permissions of the FTP server upon successful login.

## Prerequisites

Before running the script, make sure you have the required dependencies:

- **requests**: For making HTTP requests to the Telegram API.
- **rich**: For improved terminal output formatting.
- **pystyle**: For enhanced styling and coloring in terminal output.
- **ftplib**: For FTP connection handling (built-in Python module).
  
You can install the dependencies using `pip`:

```bash
pip install requests rich pystyle
```

## Configuration

1. **Telegram Bot Token and Chat ID:**  
   Set your bot token and chat ID for Telegram alerts. You can get a bot token by creating a bot on [Telegram's BotFather](https://core.telegram.org/bots#botfather).
   
   In the script, find the following lines and replace with your values:

   ```python
   TELEGRAM_TOKEN = ''  # Replace with your bot token
   CHAT_ID = ''  # Replace with your Telegram chat ID or group ID
   ```

2. **Secure Domains List:**  
   The script uses a predefined list of secure domains. Modify the `SECURE_DOMAINS` variable if needed to include other trusted domains.

## Usage

1. **Run the Script:**

   Open a terminal, navigate to the directory containing the script, and execute the script:

   ```bash
   python ftp_cracker.py
   ```

2. **Choose the Input Format:**

   The script will prompt you to select the format of the input file. Choose the appropriate format based on the structure of your credentials list:

   ```bash
   1. host:user:password
   2. host:user:password:port
   3. host - user;password - port
   4. ftp://hostname;user;pass
   5. Host: hostname identifier et ce message apparait enleve le automatiquement partout (Status code: 200) User: Username Password: password
   ```

3. **Provide Input File and Password File:**

   After selecting the format, you will be asked to provide the following:

   - **Input File**: The file containing the list of FTP credentials.
   - **Password File**: A file with additional passwords to try in case of failed login attempts.

4. **Output:**

   - The script saves **successful logins** in a file called `Good_Ftp.txt`.
   - **Failed logins** are saved in `Bad_Ftp.txt`.
   - Telegram alerts will be sent for successful logins on secure domains.

## Example of Input File

Depending on the format you choose, the input file should contain the credentials in one of the following formats:

1. **`host:user:password`**  
   ```
   ftp.example.com:user1:password1
   ftp.example2.com:user2:password2
   ```

2. **`host:user:password:port`**  
   ```
   ftp.example.com:user1:password1:21
   ftp.example2.com:user2:password2:22
   ```

3. **`host - user;password - port`**  
   ```
   ftp.example.com - user1;password1 - 21
   ftp.example2.com - user2;password2 - 22
   ```

4. **`ftp://hostname;user;pass`**  
   ```
   ftp://ftp.example.com;user1;password1
   ftp://ftp.example2.com;user2;password2
   ```

5. **`Host: hostname identifier et ce message apparait enleve le automatiquement partout (Status code: 200) User: Username Password: password`**  
   ```
   Host: ftp.example.com identifier User: user1 Password: password1
   ```

## Example of Output

### Good_Ftp.txt
```
ftp.example.com:user1:password1
ftp.example2.com:user2:password2
```

### Bad_Ftp.txt
```
ftp.badexample.com:user3:password3
```

### Telegram Alert
```
[Security Alert] The domain ftp.example.com belongs to a high-security category (.gov). Connection successful!
Details:
Username: user1
Password: password1
```

## Contributing

Feel free to fork the repository and submit pull requests with bug fixes, improvements, or new features.

## License

This script is licensed under the MIT License.

---
