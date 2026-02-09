# 🤖 AWS Telegram Bot with Groq AI Integration

A production-ready, serverless Telegram bot built on AWS infrastructure with Groq AI integration for natural language conversations. This project demonstrates cloud-native architecture, Infrastructure as Code (IaC) with Terraform, and integration with external APIs.

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [External API Integration](#external-api-integration)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup & Deployment](#setup--deployment)
- [Configuration](#configuration)
- [Bot Commands](#bot-commands)
- [Monitoring & Operations](#monitoring--operations)
- [Security](#security)
- [Terraform Structure](#terraform-structure)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Overview🎯

This project is a **serverless Telegram bot** that demonstrates:

- ✅ **Infrastructure as Code** using Terraform
- ✅ **Serverless architecture** with AWS Lambda
- ✅ **NoSQL database** operations with DynamoDB
- ✅ **Object storage** with S3
- ✅ **External API integration** with Groq AI for natural language processing
- ✅ **Monitoring & alerting** with CloudWatch
- ✅ **Security best practices** with IAM least-privilege policies
- ✅ **Production-grade logging** with structured JSON logs

**Use Cases:**
- Personal assistant bot with AI conversations
- File storage and management system
- Note-taking and organization
- Message history and search
- Analytics and usage statistics

---

## Architecture

```
┌─────────────────┐
│   Telegram API  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API Gateway    │ ◄── Webhook endpoint
│  (REST API)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  AWS Lambda     │─────►│  Groq API    │ External API
│  (Python 3.12)  │      │  (AI Chat)   │
└────────┬────────┘      └──────────────┘
         │
         ├──────────────────┬──────────────────┐
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────┐  ┌──────────────┐
│   DynamoDB      │ │     S3      │  │  CloudWatch  │
│   (NoSQL DB)    │ │  (Storage)  │  │    Logs      │
└─────────────────┘ └─────────────┘  └──────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────────────────────────────────────┐
│         CloudWatch Alarms & Monitoring          │
└─────────────────────────────────────────────────┘
```

### Architecture Components

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **API Gateway** | Webhook receiver | RESTful endpoint, request validation |
| **Lambda** | Bot logic & processing | Python 3.12, 512MB memory, 30s timeout |
| **DynamoDB** | Data persistence | On-demand billing, TTL, GSI |
| **S3** | File storage | Versioning, encryption, lifecycle policies |
| **CloudWatch** | Logging & monitoring | Structured logs, metric filters, alarms |
| **IAM** | Security & permissions | Least-privilege policies, role-based access |
| **Groq API** | AI conversations | Natural language processing, chat history |

---

## Features✨

### 🤖 AI Conversation (Groq Integration)
- Natural language conversations with AI
- Conversation history memory (up to 10 messages)
- Context-aware responses
- Multiple AI model support (llama-3.1-8b-instant, llama-3.1-70b-versatile)

### 💾 Storage System (DynamoDB)
- Key-value storage with `/save` and `/get`
- Advanced notes system with full CRUD operations
- Message history and search
- Personal analytics and statistics

### 📁 File Management (S3)
- Support for multiple file types: photos, documents, videos, audio, voice
- Automatic file metadata extraction
- S3 storage with server-side encryption
- File listing and information retrieval

### 📊 Monitoring & Operations
- Structured JSON logging to CloudWatch
- Custom metric filters for error tracking
- CloudWatch alarms for error rates
- Real-time log analysis

### 🔒 Security Features
- Environment-based secrets management
- IAM least-privilege policies
- S3 encryption at rest
- Request validation and sanitization

---

## External API Integration🌐

### Groq AI API

**Purpose:** Natural language conversation and AI-powered features

**Endpoints Used:**
- `https://api.groq.com/openai/v1/models` - List available models
- `https://api.groq.com/openai/v1/chat/completions` - Chat completions

**Authentication Method:**
- Bearer token authentication via `Authorization: Bearer <API_KEY>`
- API key stored in Lambda environment variables
- **Critical:** User-Agent header required to bypass Cloudflare protection

**Request Format:**
```json
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User message"}
  ],
  "temperature": 0.7,
  "max_tokens": 1024
}
```

**Error Handling:**
- **429 (Rate Limit):** Automatic retry with exponential backoff (3 retries, 1s → 2s → 4s)
- **401 (Auth Failed):** User-friendly error message, logs to CloudWatch
- **400 (Bad Request):** Input validation, truncation of long messages
- **403 (Cloudflare Block):** Fixed by adding User-Agent header
- **Timeout:** 30-second timeout with connection retry logic

**Rate Limiting:**
- In-memory rate limiter: 0.5s minimum interval between requests per user
- Respects Groq's API rate limits
- Graceful degradation on rate limit exceeded

**Failure Handling:**
```python
try:
    response = call_groq_api(messages)
except urllib.error.HTTPError as e:
    if e.code == 429:
        return "⏳ Rate limited. Please try again in a moment."
    elif e.code == 401:
        return "🔒 API authentication failed."
    # ... additional error handling
    logger.error("Groq API HTTP error", http_code=e.code)
```

**Secrets Management:**
- API keys stored as Lambda environment variables
- Never hardcoded in source code
- Accessible via AWS Systems Manager Parameter Store (optional)
- Can be migrated to AWS Secrets Manager for auto-rotation

---

## Prerequisites📦

### Required Tools
- **Terraform** >= 1.0.0 ([Install](https://www.terraform.io/downloads))
- **AWS CLI** >= 2.0 ([Install](https://aws.amazon.com/cli/))
- **Python** >= 3.8 (for local testing)
- **Git** for version control

### AWS Account Requirements
- Active AWS account with admin access
- AWS CLI configured with credentials
- S3 bucket for Terraform remote state (optional but recommended)

### API Keys Required
- **Telegram Bot Token** - Get from [@BotFather](https://t.me/botfather)
- **Groq API Key** - Get from [console.groq.com](https://console.groq.com)

---

## Project Structure📁

```
telegram-bot-aws/
├── terraform/
│   ├── main.tf                 # Main Terraform configuration
│   ├── variables.tf            # Input variables
│   ├── outputs.tf              # Output values
│   └── backend.tf              # Remote state configuration
├── lambda/
│   ├── handler.py              # Main Lambda handler
│   ├── requirements.txt        # Python dependencies
│   └── test_groq_secure.py     # API testing script
├── .gitignore
├── README.md                   # This file
└── LICENSE
```

---

## Setup & Deployment🚀

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/telegram-bot-aws.git
cd telegram-bot-aws
```

### Step 2: Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

### Step 3: Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Save the bot token (looks like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### Step 4: Get Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Navigate to API Keys section
4. Create new API key
5. Save the key (starts with `gsk_`)

### Step 5: Configure Terraform Variables

Create `terraform/terraform.tfvars`:

```hcl
# AWS Configuration
aws_region = "us-east-1"
environment = "production"

# Project Configuration
project_name = "telegram-bot"

# Telegram Configuration
telegram_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"

# Groq AI Configuration
groq_api_key = "YOUR_GROQ_API_KEY"
groq_model = "llama-3.1-8b-instant"

# Bot Configuration
enable_conversation_memory = true
max_conversation_history = 10

# Tags
tags = {
  Project     = "telegram-bot"
  Environment = "production"
  ManagedBy   = "terraform"
}
```

### Step 6: Initialize Terraform

```bash
cd terraform
terraform init
```

### Step 7: Review Plan

```bash
terraform plan
```

Expected output:
- API Gateway REST API
- Lambda Function
- DynamoDB Table
- S3 Bucket
- CloudWatch Log Group
- CloudWatch Alarm
- IAM Roles and Policies

### Step 8: Deploy Infrastructure

```bash
terraform apply
```

Type `yes` when prompted.

⏱️ **Deployment time:** ~2-3 minutes

### Step 9: Set Telegram Webhook

```bash
# Get the API Gateway URL from Terraform outputs
export API_URL=$(terraform output -raw api_gateway_invoke_url)

# Set webhook
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=${API_URL}"

# Verify webhook
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo"
```

### Step 10: Test Your Bot!

Open Telegram and send `/start` to your bot!

---

## Configuration

### Environment Variables (Lambda)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | - | Telegram bot authentication token |
| `DDB_TABLE_NAME` | ✅ | - | DynamoDB table name |
| `S3_BUCKET_NAME` | ✅ | - | S3 bucket for file storage |
| `GROQ_API_KEY` | ✅ | - | Groq API authentication key |
| `GROQ_MODEL` | ❌ | `llama-3.1-8b-instant` | Groq model to use |
| `ENABLE_CONVERSATION_MEMORY` | ❌ | `true` | Enable conversation history |
| `MAX_CONVERSATION_HISTORY` | ❌ | `10` | Max messages in history |

### Terraform Variables

See `terraform/variables.tf` for complete list of configurable options.

**Key Variables:**
- `aws_region` - AWS region for deployment
- `environment` - Environment name (dev/staging/prod)
- `lambda_memory_size` - Lambda memory allocation (MB)
- `lambda_timeout` - Lambda timeout (seconds)
- `dynamodb_billing_mode` - DynamoDB billing (PAY_PER_REQUEST/PROVISIONED)

---

## Bot Commands💬

### 🔹 Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message | `/start` |
| `/hello` | Simple greeting | `/hello` |
| `/help` | Show all commands | `/help` |
| `/menu` | Show command menu | `/menu` |
| `/echo <text>` | Echo back your text | `/echo Hello World` |

### 🤖 AI Conversation (Groq)

| Command | Description | Example |
|---------|-------------|---------|
| `/chat <message>` | Chat with AI | `/chat Tell me a joke` |
| Plain text | Natural conversation | `What's the weather like?` |
| `/clearhistory` | Clear conversation memory | `/clearhistory` |
| `/ask <question>` | Quick AI answer | `/ask What is AWS?` |

### 💾 Storage Commands (DynamoDB)

| Command | Description | Example |
|---------|-------------|---------|
| `/save <key> <value>` | Save key-value pair | `/save name John` |
| `/get <key>` | Retrieve value | `/get name` |
| `/list` | List all saved keys | `/list` |

### 📝 Notes System (CRUD Operations)

| Command | Description | Example |
|---------|-------------|---------|
| `/newnote <title> \| <content>` | Create new note | `/newnote Shopping \| Buy milk` |
| `/readnote <note_id>` | Read specific note | `/readnote abc123` |
| `/updatenote <id> \| <title> \| <content>` | Update note | `/updatenote abc123 \| New Title \| Updated` |
| `/deletenote <note_id>` | Delete note | `/deletenote abc123` |
| `/mynotes` | List all notes | `/mynotes` |

### 📁 File Commands (S3 Storage)

| Action | Description | How to Use |
|--------|-------------|------------|
| Send photo | Upload photo to S3 | Send any image |
| Send document | Upload document to S3 | Send any file |
| Send video | Upload video to S3 | Send video file |
| Send audio | Upload audio to S3 | Send audio file |
| Send voice | Upload voice message | Record voice message |
| `/myfiles` | List uploaded files | `/myfiles` |
| `/fileinfo <file_id>` | Get file details | `/fileinfo xyz789` |

### 📋 Message Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/search <keyword>` | Search messages | `/search meeting` |
| `/latest` | Show latest message | `/latest` |
| `/history` | Show last 5 messages | `/history` |

### 📱 Native Features
| Command | Description | Example |
|---------|-------------|---------|
| `/poll` | Create a poll | `/poll What's your favorite language?` |
| `/location` | Share current location | `/location` |
| `/stickers` | Send sticker menu | `/stickers` |

### 📊 Analytics

| Command | Description | Example |
|---------|-------------|---------|
| `/stats` | Personal usage statistics | `/stats` |

### 🧪 Testing

| Command | Description | Example |
|---------|-------------|---------|
| `/testerror` | Trigger test error for CloudWatch | `/testerror` |

---

## Monitoring & Operations📊

### CloudWatch Logs

**Log Group:** `/aws/lambda/telegram-bot-lambda`

**Log Format:** Structured JSON

```json
{
  "level": "INFO",
  "timestamp": "2025-01-26T10:30:45.123Z",
  "message": "Lambda invocation started",
  "request_id": "abc-123-def",
  "user_id": 12345678,
  "action": "chat"
}
```

### Viewing Logs

**AWS Console:**
1. Navigate to CloudWatch → Log Groups
2. Select `/aws/lambda/telegram-bot-lambda`
3. Click on latest log stream

**AWS CLI:**
```bash
# Tail logs in real-time
aws logs tail /aws/lambda/telegram-bot-lambda --follow

# Search for errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/telegram-bot-lambda \
  --filter-pattern "ERROR"
```

### CloudWatch Alarms

**Error Rate Alarm:**
- **Metric:** ErrorCount from metric filter
- **Threshold:** > 5 errors in 5 minutes
- **Action:** SNS notification (if configured)

**View Alarm Status:**
```bash
aws cloudwatch describe-alarms \
  --alarm-names telegram-bot-lambda-errors
```

### Metric Filters

**Error Detection:**
- Pattern: `{ $.level = "ERROR" }`
- Metric: `ErrorCount`
- Namespace: `TelegramBot`

### Performance Metrics

Monitor in CloudWatch:
- Lambda duration
- Lambda invocations
- Lambda errors
- Lambda concurrent executions
- DynamoDB consumed capacity
- S3 bucket size

---

## Security🔒

### IAM Policies (Least Privilege)

**Lambda Execution Role Permissions:**
- ✅ DynamoDB: `GetItem`, `PutItem`, `Query`, `UpdateItem`, `DeleteItem` (scoped to specific table)
- ✅ S3: `GetObject`, `PutObject`, `DeleteObject`, `ListBucket` (scoped to specific bucket)
- ✅ CloudWatch Logs: `CreateLogGroup`, `CreateLogStream`, `PutLogEvents`
- ❌ No `s3:*` or `dynamodb:*` wildcard permissions

### Secrets Management

1. **Environment Variables** (Current)
   - API keys stored in Lambda environment variables
   - Encrypted at rest by AWS
   - Accessible only to Lambda function

2. **AWS Secrets Manager** (Recommended for Production)
   ```bash
   # Store secret
   aws secretsmanager create-secret \
     --name telegram-bot/groq-api-key \
     --secret-string "gsk_your_key_here"
   
   # Retrieve in Lambda
   secret = boto3.client('secretsmanager').get_secret_value(
       SecretId='telegram-bot/groq-api-key'
   )
   ```

3. **AWS Systems Manager Parameter Store** (Alternative)
   ```bash
   # Store parameter
   aws ssm put-parameter \
     --name /telegram-bot/groq-api-key \
     --value "gsk_your_key_here" \
     --type SecureString
   
   # Retrieve in Lambda
   param = boto3.client('ssm').get_parameter(
       Name='/telegram-bot/groq-api-key',
       WithDecryption=True
   )
   ```

### S3 Encryption

- **Server-side encryption:** AES-256 (SSE-S3)
- **Bucket policy:** Denies unencrypted uploads
- **Versioning:** Enabled for data protection
- **Public access:** Blocked

### Network Security

- ✅ API Gateway with SSL/TLS
- ✅ Lambda in AWS managed VPC
- ✅ DynamoDB and S3 access via AWS PrivateLink
- ❌ No public endpoints except API Gateway

---

## Terraform Structure

### Modules

#### 1. Lambda Module (`modules/lambda`)

**Purpose:** Creates Lambda function with deployment package

**Inputs:**
- `function_name` - Lambda function name
- `handler` - Entry point (e.g., `handler.lambda_handler`)
- `runtime` - Python version
- `memory_size` - Memory allocation
- `timeout` - Execution timeout
- `environment_variables` - Environment variables map
- `iam_role_arn` - IAM role ARN

**Outputs:**
- `function_arn` - Lambda function ARN
- `function_name` - Function name
- `invoke_arn` - Invocation ARN for API Gateway

#### 2. DynamoDB Module (`modules/dynamodb`)

**Purpose:** Creates DynamoDB table with GSI

**Inputs:**
- `table_name` - Table name
- `billing_mode` - PAY_PER_REQUEST or PROVISIONED
- `hash_key` - Partition key name
- `range_key` - Sort key name
- `ttl_enabled` - Enable TTL
- `ttl_attribute_name` - TTL attribute name

**Outputs:**
- `table_name` - DynamoDB table name
- `table_arn` - Table ARN

#### 3. S3 Module (`modules/s3`)

**Purpose:** Creates S3 bucket with security settings

**Inputs:**
- `bucket_name` - Bucket name
- `versioning_enabled` - Enable versioning
- `encryption_algorithm` - SSE algorithm
- `lifecycle_rules` - Lifecycle policies

**Outputs:**
- `bucket_name` - S3 bucket name
- `bucket_arn` - Bucket ARN

#### 4. API Gateway Module (`modules/api_gateway`)

**Purpose:** Creates REST API with Lambda integration

**Inputs:**
- `api_name` - API name
- `lambda_invoke_arn` - Lambda invocation ARN
- `lambda_function_name` - Lambda function name
- `stage_name` - Deployment stage

**Outputs:**
- `api_id` - API Gateway ID
- `api_endpoint` - API endpoint URL
- `deployment_id` - Deployment ID

#### 5. CloudWatch Module (`modules/cloudwatch`)

**Purpose:** Creates log groups, metric filters, and alarms

**Inputs:**
- `log_group_name` - Log group name
- `retention_days` - Log retention period
- `metric_filter_pattern` - Filter pattern
- `alarm_threshold` - Alarm threshold

**Outputs:**
- `log_group_name` - Log group name
- `alarm_arn` - CloudWatch alarm ARN

### Remote State Backend

**File:** `terraform/backend.tf`

```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "telegram-bot/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

**Benefits:**
- ✅ Team collaboration
- ✅ State locking with DynamoDB
- ✅ Encrypted state files
- ✅ State versioning

**Setup:**
```bash
# Create state bucket
aws s3 mb s3://your-terraform-state-bucket

# Create lock table
aws dynamodb create-table \
  --table-name terraform-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

---

## Testing🧪

### Local Testing

**Test Groq API Connection:**
```bash
cd lambda
python3 -m venv venv
source venv/bin/activate
pip install python-dotenv

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# Run test
python test_groq_secure.py
```

**Expected Output:**
```
🔍 Testing Groq API - Listing available models...
✅ Success! Available models:
   - llama-3.1-8b-instant
   - llama-3.1-70b-versatile
   - mixtral-8x7b-32768

🔍 Testing Groq API - Chat completion...
✅ Chat completion successful!
   Response: API test successful.
   Model: llama-3.1-8b-instant
   Tokens used: 52
```

### Unit Tests

```bash
cd tests
pytest test_handler.py -v
```

### Integration Tests

1. **Test Basic Commands:**
   ```
   Send to bot: /start
   Expected: Welcome message
   
   Send to bot: /hello
   Expected: Greeting response
   
   Send to bot: /help
   Expected: Command list
   ```

2. **Test DynamoDB Operations:**
   ```
   Send: /save testkey testvalue
   Expected: ✅ Saved key 'testkey' to DynamoDB.
   
   Send: /get testkey
   Expected: 🔑 testkey = testvalue (from DynamoDB)
   
   Send: /list
   Expected: List showing 'testkey'
   ```

3. **Test Groq AI:**
   ```
   Send: /chat Hello, how are you?
   Expected: AI response
   
   Send: Hi there! (plain text)
   Expected: AI conversation response
   ```

4. **Test File Upload:**
   ```
   Send: Any photo
   Expected: ✅ Photo uploaded to S3!
   
   Send: /myfiles
   Expected: List of uploaded files
   ```

---

## Troubleshooting🔧

### Common Issues

#### 1. Bot Not Responding

**Symptoms:** No response when messaging bot

**Possible Causes:**
- Webhook not set correctly
- Lambda function errors
- API Gateway misconfiguration

**Solutions:**
```bash
# Check webhook status
curl https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo

# Check Lambda logs
aws logs tail /aws/lambda/telegram-bot-lambda --follow

# Verify API Gateway URL
terraform output api_gateway_invoke_url
```

#### 2. Groq API 403 Error

**Symptoms:** Groq API returns `error code: 1010`

**Cause:** Missing User-Agent header (Cloudflare blocks requests without User-Agent)

**Solution:** Ensure handler.py includes:
```python
req.add_header("User-Agent", "python-urllib/groq-api-client")
```

This is already fixed in `handler_fixed.py`

#### 3. DynamoDB Permission Errors

**Symptoms:** `AccessDeniedException` in CloudWatch logs

**Cause:** Lambda IAM role missing DynamoDB permissions

**Solution:**
```bash
# Check IAM policy
aws iam get-role-policy \
  --role-name telegram-bot-lambda-role \
  --policy-name dynamodb-access

# Update Terraform and reapply
terraform apply
```

#### 4. S3 Upload Failures

**Symptoms:** File uploads fail with error message

**Cause:** Lambda role missing S3 permissions or bucket doesn't exist

**Solution:**
```bash
# Verify bucket exists
aws s3 ls s3://your-bucket-name

# Check Lambda has S3 permissions
aws iam get-role-policy \
  --role-name telegram-bot-lambda-role \
  --policy-name s3-access
```

#### 5. Terraform State Lock

**Symptoms:** `Error acquiring the state lock`

**Cause:** Previous Terraform operation didn't complete cleanly

**Solution:**
```bash
# Force unlock (use with caution)
terraform force-unlock <LOCK_ID>

# Or manually delete DynamoDB lock item
aws dynamodb delete-item \
  --table-name terraform-state-lock \
  --key '{"LockID": {"S": "your-state-file-path"}}'
```

### Debug Mode

Enable detailed logging in Lambda:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### CloudWatch Insights Queries

**Find all errors in last hour:**
```
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100
```

**Find slow Lambda executions:**
```
filter @type = "REPORT"
| fields @duration
| filter @duration > 3000
| sort @duration desc
```

---

## Future Enhancements🚀

### Short-term
- [ ] Add support for inline keyboards
- [ ] Implement conversation branching
- [ ] Add user preferences storage
- [ ] Support for more file types
- [ ] Rich text formatting in messages

### Medium-term
- [ ] Multi-language support (i18n)
- [ ] Webhook validation with secret token
- [ ] Rate limiting per user
- [ ] Admin dashboard
- [ ] Scheduled messages/reminders

### Long-term
- [ ] Multi-region deployment
- [ ] Real-time analytics dashboard
- [ ] Machine learning for user preferences
- [ ] Integration with other AI providers
- [ ] Voice message transcription
- [ ] Image recognition and analysis

---

## 📸 Screenshots & Logs

### CloudWatch Alarm
<a href="screenshot/Alarm_Triggered1.png" target="_blank">
  Alarm Triggered
</a>
*Error alarm triggered after detecting test error*

### CloudWatch Logs
<a href="screenshot/Structured_Logs.png" target="_blank">
  Structured Logs
</a>
*CloudWatch log stream showing JSON-formatted logs with consistent fields*

### CloudWatch Dashboard
<a href="screenshot/Dashboard.png" target="_blank">
  Dashboard
</a>
*Complete observability dashboard with all metrics*

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Coding Standards:**
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Include unit tests for new features
- Update README for significant changes

---

## License📄

This project was developed for an MSc Cloud Solutions course and implements a Telegram bot using AWS Lambda, DynamoDB for chat data storage, and Amazon S3.

---
## 🙏 Acknowledgments

- [Telegram Bot API](https://core.telegram.org/bots/api) for bot integration
- [Groq](https://groq.com) for high-performance AI inference
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) for IaC
- [AWS](https://aws.amazon.com) for cloud infrastructure
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for AWS SDK

---

## 📚 Additional Resources

- [Terraform AWS Best Practices](https://www.terraform-best-practices.com/v/aws/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Telegram Bot Development](https://core.telegram.org/bots)
- [Groq API Documentation](https://console.groq.com/docs)

---

## 📞 Support

If you encounter any issues or have questions:

1. Check CloudWatch logs for error details
2. Review alarm history for patterns
3. Consult metric dashboards for performance insights
