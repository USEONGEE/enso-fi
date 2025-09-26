# Lending Protocol Monitor Bot

This project provides a **Telegram bot** that continuously monitors **APYs (Annual Percentage Yields)** across multiple lending protocols.  
When significant rate changes are detected, the bot immediately sends alerts to users, allowing them to react quickly with actions such as moving, reinforcing, or closing positions.

The bot relies on a **Python SDK adaptation of Enso’s TypeScript SDK** (in progress). For now, it uses HTTP calls as a fallback until the SDK is finalized.

---

## ✨ Features

- **Telegram Bot Interface**  
  Users interact via commands and buttons (`/start`, wallet management, lending info, etc.).

- **Account Management**  
  Create, activate, retrieve, and delete accounts. Data is stored in MongoDB.

- **Lending Portfolio Monitoring**  
  - Fetch wallet balances and token metadata from Enso.  
  - Compare market lending rates from Hyperlend.  
  - Match assets against the best available APY.

- **Background Tasks**  
  Periodic jobs and Kafka consumers for event-driven updates.

- **Alert System**  
  Instant Telegram notifications when significant APY fluctuations occur.

---

## 🏗️ Architecture Overview

```text
User (Telegram)
   ↓
front/ (Telegram UI & flow handlers)
   ├─ start, wallet, lend commands
   └─ utils (session, error handling, UI helpers)
        ↓
backend/
   ├─ account/ (business logic + repository + Kafka integration)
   ├─ lend/ (portfolio monitoring and APY matching)
   ├─ abi/, constants/, utils/ (on-chain/Web3 utilities)
   └─ background_task/ (periodic tasks & consumers)
        ↓
External Services
   ├─ MongoDB (account storage)
   └─ Enso API (balances, token info)
```

## 📂 Repository Structure
```text
front/                  # Telegram command handlers & utils
backend/
 ├─ account/            # Account services and repository
 ├─ lend/               # Lending service logic
 ├─ abi/                # Smart contract ABIs
 ├─ constants/          # Constants and configs
 ├─ utils/              # Helper functions (web3, etc.)
```

## 🔧 Tech Stack
- Python 3.10+
- MongoDB (account persistence)
- Telegram Bot API
- Enso SDK (Python port in progress)
- Hyperlend API
- Kafka (for event-driven flows, optional)

# NOTE
- The Enso SDK integration is currently mocked via HTTP requests.
- Once the Python SDK is finalized, the dependency will be swapped seamlessly.
- This project is designed for monitoring and alerting only; it does not execute on-chain transactions.
- Currently, the project depends on a private internal GitHub repository (for internal utilities).
Therefore, it cannot be executed by the public as-is.
If you wish to run the project, please contact shdbtjd8@gmail.com
