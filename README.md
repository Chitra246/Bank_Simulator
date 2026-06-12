[README.md](https://github.com/user-attachments/files/28883880/README.md)
# 🏦 Banking Automation Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey?logo=sqlite) ![Status](https://img.shields.io/badge/Status-Demo%20Project-orange)

A desktop-based **Banking Simulator** application built with **Python** and **Tkinter**, featuring a full GUI, SQLite database integration, OTP-based email verification, CAPTCHA authentication, and role-based access for Admin and Customers.

![Login Screen](screenshot_login.PNG)

---

## 👩‍💻 Author
**M Chitra**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| GUI Framework | Python Tkinter + ttk |
| Database | SQLite3 (`bank.sqlite`) |
| Custom Modules | `Random_Generator.py`, `tables.py`, `mailing.py` |
| Image Handling | Pillow (PIL) |
| Time Utilities | Python `time` module |

---

## 📁 Project Structure

```
Banking_Simulator_Project/
│
├── Main_Project.py        # Core application file (all screens & logic)
├── tables.py              # SQLite table creation module
├── Random_Generator.py    # CAPTCHA, OTP & password generation
├── mailing.py             # Email automation module
├── bank.sqlite            # SQLite database (auto-created on first run)
├── logo.jpg               # Bank logo image for the main screen
└── README.md
```

---

## 🔐 Default Credentials

| Role | Account No. | Password |
|---|---|---|
| Admin | `0` | `admin` |
| Customer | *(auto-assigned on account creation)* | *(auto-generated & emailed to user)* |

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/banking-simulator.git
   cd banking-simulator
   ```

2. **Install dependencies**
   ```bash
   pip install pillow
   ```

3. **Configure email** — Open `mailing.py` and set your SMTP credentials (sender email & app password).

4. **Run the application**
   ```bash
   python Main_Project.py
   ```

> The database (`bank.sqlite`) and all tables are created automatically on first run via `tables.create_tables()`.

---

## 🗺️ Application Flow — Step by Step

---

### 🔑 Step 1 — Main Login Screen

The first screen launched on startup. The live clock updates every second. The user selects a role, enters credentials, solves the CAPTCHA, and clicks Login.

![Login Screen](screenshot_login.PNG)

**Fields:**
- **User Type** — Dropdown to select `Admin` or `Customer`
- **A/C No.** — Account number input
- **Password** — Masked password input
- **CAPTCHA** — Auto-generated code with a 🔄 Refresh button
- **Login / Reset / Forgot Password** — Action buttons

**Login Logic:**
- Validates all fields are filled and CAPTCHA matches
- Admin: checks A/C No. = `0` and Password = `admin`
- Customer: queries `bank.sqlite` — `SELECT * FROM accounts WHERE AC_No=? AND Password=?`

---

### 🔒 Step 2 — Forgot Password Screen

Accessible via the **Forgot Password** button. Allows users to recover their password through OTP verification on their registered email.

![Forgot Password Screen](screenshot_forgot.PNG)

**Flow:**
1. Enter A/C No. and registered Email ID
2. Click **Send OTP** — an OTP is generated via `Random_Generator.forgototp()` and emailed via `mailing.forgototp_mail()`
3. Enter the received OTP in the dialog box
4. On match → password is revealed in a message box
5. On mismatch → error dialog is shown

---

### 🛠️ Step 3 — Admin Panel

Reached after successful admin login. Provides three account management operations via buttons at the top.

![Admin Panel](screenshot_admin.PNG)

#### ➕ New Account
Opens a form to fill customer details — Name, Email ID, Mobile No., Aadhar No.

![New Account Form](screenshot_newaccount.PNG)

On clicking **Open Account**:
- A random password is generated via `Random_Generator.password()`
- Details are inserted into `accounts` table with initial balance = `0`
- Newly assigned A/C No. is fetched via `SELECT MAX(AC_No) FROM accounts`
- Welcome email with credentials is sent via `mailing.openacn_mail()`

#### 👁️ View Account
- Prompts for an A/C No. via dialog box
- Fetches and displays full account details from the database

#### ❌ Close Account
- Prompts for an A/C No. via dialog box
- Sends a closure OTP to the registered email via `mailing.closeotp_mail()`
- On OTP match → `DELETE FROM accounts WHERE AC_No=?` is executed
- On OTP mismatch → error dialog is shown

---

### 👤 Step 4 — Customer Panel

Reached after successful customer login. Five banking operations are available via the left-side buttons.

![Customer Panel](screenshot_customer.PNG)

---

### 💳 Step 5 — Customer Operations

#### Show Details
Displays full account information — Account No., Opening Date, Aadhar No., Mobile No., and current Balance.

![Show Details](screenshot_showdetails.PNG)

#### Update Details
Opens an inner frame to edit Name, Mobile No., and Email ID. Executes an `UPDATE accounts SET ...` query on submission.

#### Deposit
Dialog box prompts for deposit amount. Executes:
```sql
UPDATE accounts SET Balance = Balance + ? WHERE AC_No = ?
```

#### Withdraw
Dialog box prompts for withdrawal amount. Checks for sufficient balance before executing:
```sql
UPDATE accounts SET Balance = Balance - ? WHERE AC_No = ?
```

#### Transfer
1. Prompts for destination A/C No. — validates it exists in the database
2. Prompts for transfer amount — checks sender has sufficient balance
3. On success, deducts from sender and credits to receiver in the same transaction:
```sql
UPDATE accounts SET Balance = Balance - ? WHERE AC_No = ?  -- sender
UPDATE accounts SET Balance = Balance + ? WHERE AC_No = ?  -- receiver
```

---

### 🚪 Step 6 — Logout
Both Admin and Customer screens have a **Logout** button that destroys the current frame and returns to the main login screen.

---

## 🧩 Supporting Modules

### `tables.py`
Sets up the `accounts` table in `bank.sqlite` on first run.

| Column | Type | Description |
|---|---|---|
| AC_No | INTEGER (PK, Auto) | Unique account number |
| Name | TEXT | Account holder name |
| Password | TEXT | Auto-generated password |
| Balance | REAL | Current account balance |
| Mob | TEXT | Mobile number |
| Aadhar | TEXT | Aadhar number |
| Email | TEXT | Registered email ID |
| Open_Date | TEXT | Account opening date & time |

### `Random_Generator.py`
| Function | Purpose |
|---|---|
| `captcha()` | Generates a random CAPTCHA string for login |
| `password()` | Generates a secure random password for new accounts |
| `forgototp()` | Generates OTP for password recovery |
| `closeotp()` | Generates OTP for account closure verification |

### `mailing.py`
| Function | Purpose |
|---|---|
| `openacn_mail(to, text)` | Sends account credentials on new account creation |
| `forgototp_mail(to, text)` | Sends OTP for forgot password flow |
| `closeotp_mail(to, text)` | Sends OTP for account closure verification |

---

## ✨ Key Features

- 🔐 **Role-based access** — Separate flows for Admin and Customer
- 🤖 **CAPTCHA verification** — Prevents automated login attempts
- 📧 **OTP via Email** — Secure verification for password recovery and account closure
- 🔑 **Auto-generated credentials** — Random passwords created and emailed on account opening
- 🕐 **Live clock** — Real-time date and time on the main screen
- 🗄️ **SQLite backend** — Lightweight, file-based database with no external server required
- 💸 **Interbank transfer simulation** — Validates receiver account and updates both balances atomically

---


## 📄 License

This project is for **educational and demo purposes only**.

---

*Demo project by M Chitra*
