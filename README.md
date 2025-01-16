# ServiBots - $1 Microservices Marketplace 🚀

Welcome to **ServiBots**, the **digital marketplace** where developers can offer **microservices** for a **fixed price of $1 per session**. Customers can browse and instantly access these **developer-built services**, paying securely through **Stripe** or **PayPal**.

---

## 📌 Key Features
- **💻 Developer-Powered Microservices** – Independent developers publish their microservices on the platform.
- **💲 $1 Per Use** – Every microservice session costs exactly **$1**.
- **🔄 Subscription Model** *(Optional)* – Scale customer usage with subscription plans.
- **🔒 Secure Payments** – Powered by **Stripe Connect** & **PayPal Payouts**.
- **💸 Automated Payouts** – Developers receive payments directly to their **Stripe Express** or **PayPal accounts**.
- **📊 Developer Dashboard** – View transaction history, balance, and payout status.

---

## 🛠 Tech Stack
- **Backend**: AWS **Lambda** (Serverless), **Python**, PostgreSQL (**RDS**)
- **Payments**: **Stripe Connect**, **PayPal Payouts**
- **Infrastructure**: **AWS API Gateway**, **Serverless Framework**
- **Logging & Monitoring**: AWS **CloudWatch**
- **Security**: **SSM Parameter Store** for API keys & secrets

---

## 📜 How It Works
### For Customers
1. **Browse microservices** – Select a service from available bots.
2. **Pay $1 per session** – Secure checkout via **Stripe** or **PayPal**.
3. **Receive output instantly** – The bot runs and provides results.
4. **(Optional) Subscribe** – Access services at scale via **subscriptions**.

### For Developers
1. **Create an account** – Register on ServiBots.
2. **Publish a microservice** – Provide a **service URL**.
3. **Earn from every transaction** – Each session costs **$1**.
4. **Get paid via PayPal or Stripe** – Withdraw balance anytime.

---

## 🔑 Payments & Payouts
### Customers
✔ Pay **$1 per session** securely.  
✔ Transactions are handled via **Stripe** & **PayPal**.

### Developers
✔ **85% of each transaction** goes to the developer.  
✔ **15% platform fee** deducted from each session.  
✔ Withdraw funds via:
   - **Stripe Express** (for instant payouts)
   - **PayPal** (for manual withdrawals)
✔ View **balance, history, and failed payouts**.

---

## 🚀 API Endpoints
### Bot Orders
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/bot/order/create` | `POST` | Create a new bot order |
| `/bot/order/initialize` | `POST` | Mark an order as received |
| `/bot/order/complete` | `POST` | Mark an order as completed |

### Transactions
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/transaction/create` | `POST` | Create a new transaction |
| `/transaction/history` | `GET` | Retrieve transaction history |
| `/transaction/balance` | `GET` | Get developer balance |

### Payouts
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/payout/create` | `POST` | Request a payout |
| `/payout/status` | `GET` | Check payout status |
| `/payout/retry` | `POST` | Retry failed payouts |

---

## 🔄 Webhooks
ServiBots listens for **real-time updates** from Stripe & PayPal:
- **Stripe** → Payment confirmations, chargebacks.
- **PayPal** → Payout success, disputes, failed transfers.

---

## ⚡ Developer Setup
### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
