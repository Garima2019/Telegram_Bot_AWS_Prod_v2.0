# 🧪 Bot Testing Commands - Complete Guide

## Quick Test Sequence for Live Demo

This is a **5-minute demo script** that covers all major features for your Task 10 presentation.

---

## 🎬 DEMO SCRIPT (Follow This Order)

### 1️⃣ Basic Setup & Welcome (30 seconds)

```
/start
```
**Expected:** Welcome message with bot introduction

```
/help
```
**Expected:** Complete command list with AI status

---

### 2️⃣ AI Conversation - Groq Integration (1 minute)

**Test natural conversation:**
```
Hello! Can you introduce yourself?
```
**Expected:** AI responds with natural conversation

**Test /chat command:**
```
/chat What are the main AWS services?
```
**Expected:** AI provides detailed response about AWS services

**Test conversation memory:**
```
/chat What did I just ask you about?
```
**Expected:** AI remembers previous question about AWS

**Clear history:**
```
/clearhistory
```
**Expected:** "🧹 Conversation history cleared!"

---

### 3️⃣ DynamoDB Operations - CRUD Demo (1.5 minutes)

**A. Simple Key-Value Storage:**

```
/save project aws-telegram-bot
```
**Expected:** ✅ Saved key 'project' to DynamoDB

```
/save course cloud-computing
```
**Expected:** ✅ Saved key 'course' to DynamoDB

```
/get project
```
**Expected:** 🔑 project = aws-telegram-bot (from DynamoDB)

```
/list
```
**Expected:** List showing both keys (project, course)

**B. Notes System (Full CRUD):**

**CREATE:**
```
/newnote AWS Lambda | Lambda is a serverless compute service that runs code in response to events
```
**Expected:** ✅ Note created! Note ID: abc123xyz...
**IMPORTANT:** Copy the note_id from the response!

**READ:**
```
/readnote <paste_note_id_here>
```
**Expected:** Shows note title, content, created date

**LIST:**
```
/mynotes
```
**Expected:** List of all your notes with IDs

**UPDATE:**
```
/updatenote <paste_note_id_here> | AWS Lambda Functions | Lambda runs serverless code with automatic scaling
```
**Expected:** ✅ Note updated successfully!

**VERIFY UPDATE:**
```
/readnote <paste_note_id_here>
```
**Expected:** Shows updated title and content

**DELETE:**
```
/deletenote <paste_note_id_here>
```
**Expected:** ✅ Note deleted successfully!

---

### 4️⃣ S3 File Upload & Retrieval (1 minute)

**Upload different file types:**

1. **Send a photo** (any image)
   - **Expected:** ✅ Photo uploaded to S3! File ID: xyz789...

2. **Send a document** (PDF, Word doc, etc.)
   - **Expected:** ✅ Document uploaded to S3! File ID: abc456...

**List files:**
```
/myfiles
```
**Expected:** List of uploaded files with:
- Filename
- File type
- Size in KB
- Upload date
- File ID

**Get file details:**
```
/fileinfo <paste_file_id_here>
```
**Expected:** Detailed file information including S3 key

---

### 5️⃣ Message Search & History (30 seconds)

```
/history
```
**Expected:** Last 5 messages from DynamoDB

```
/search lambda
```
**Expected:** Messages containing "lambda"

```
/latest
```
**Expected:** Most recent message

---

### 6️⃣ Analytics & Statistics (30 seconds)

```
/stats
```
**Expected:** Personal usage statistics:
- Total messages
- Files uploaded
- Notes created
- Storage used

---

### 7️⃣ CloudWatch Test (30 seconds)

```
/testerror
```
**Expected:** ✅ Test error logged successfully!
**Action:** Switch to AWS Console → CloudWatch → Logs
**Show:** Error entry with stack trace in logs

---

## 📊 What to Show in AWS Console

### During Demo, Have These Tabs Open:

1. **CloudWatch Logs** (`/aws/lambda/telegram-bot-lambda`)
   - Show real-time log streaming
   - Point out structured JSON logs
   - Filter for "ERROR" after /testerror

2. **CloudWatch Alarms**
   - Show `telegram-bot-lambda-errors` alarm
   - Explain threshold (>5 errors in 5 minutes)

3. **DynamoDB Console**
   - Show table items being created/updated
   - Show GSI (if configured)
   - Show capacity metrics

4. **S3 Console**
   - Show uploaded files in bucket
   - Show folder structure (user_id/file_type/)
   - Show encryption enabled

5. **Lambda Console**
   - Show function configuration
   - Show environment variables (blur sensitive values)
   - Show execution time metrics

---

## 🎯 Extended Testing (If Time Permits)

### Advanced AI Features

**Summarization:**
```
/summarize
```
**Expected:** AI-generated summary of your notes

**Quick Question:**
```
/ask What is DynamoDB?
```
**Expected:** Concise AI answer (without conversation history)

---

### Advanced File Operations

**Send voice message** (record and send)
**Expected:** Voice message uploaded and transcription (if implemented)

**Send video** (any video file)
**Expected:** Video uploaded to S3 with metadata

---

### Advanced Message Operations

**Save some messages with keywords:**
```
/save status production-ready
/save deployment successful
/save testing completed
```

**Search across multiple messages:**
```
/search production
```
**Expected:** Returns all messages with "production"

---

## 🐛 Testing Error Handling

### Test Rate Limiting
**Send multiple rapid /chat commands:**
```
/chat test 1
/chat test 2
/chat test 3
```
**Expected:** Should handle gracefully with rate limiting

### Test Invalid Input
```
/get nonexistent_key
```
**Expected:** ❌ No value found for key 'nonexistent_key'

```
/readnote invalid_id
```
**Expected:** ❌ Note 'invalid_id' not found

```
/save
```
**Expected:** Usage: /save <key> <value>

---

## 📋 Pre-Demo Checklist

### Before Starting Demo:

- [ ] Verify webhook is set:
  ```bash
  curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo"
  ```

- [ ] Check Lambda is healthy:
  ```bash
  aws lambda get-function --function-name telegram-bot-lambda
  ```

- [ ] Verify environment variables are set:
  ```bash
  aws lambda get-function-configuration \
    --function-name telegram-bot-lambda \
    --query 'Environment.Variables'
  ```

- [ ] Test Groq API locally:
  ```bash
  python lambda/test_groq_secure.py
  ```

- [ ] Open CloudWatch Logs in browser
- [ ] Open DynamoDB table in browser
- [ ] Open S3 bucket in browser
- [ ] Have test images/documents ready

---

## 🎤 Demo Script with Narration

**Use this script during your presentation:**

---

### **Part 1: Introduction (30 sec)**

> "Let me demonstrate our serverless Telegram bot built on AWS with Groq AI integration. I'll show you the core features, DynamoDB operations, S3 storage, and our external API integration."

**Action:** Send `/start`

> "The bot is now running on AWS Lambda, responding to Telegram webhooks through API Gateway."

---

### **Part 2: Groq AI Integration (1 min)**

> "First, let's demonstrate our external API integration with Groq AI for natural language processing."

**Action:** Send `Hello! Can you introduce yourself?`

> "Notice the natural conversation - no command needed. The bot uses Groq's llama-3.1-8b-instant model with conversation history stored in DynamoDB."

**Action:** Send `/chat What are the main AWS services?`

> "The bot maintains context across messages. Let me ask a follow-up:"

**Action:** Send `/chat What did I just ask you about?`

> "See how it remembers the previous question? This demonstrates our conversation memory feature."

---

### **Part 3: DynamoDB CRUD (1.5 min)**

> "Now let's demonstrate DynamoDB operations - the backbone of our data persistence."

**Action:** Send `/save project aws-telegram-bot`

> "Data is being written to DynamoDB with partition key user_id and sort key 'kv#project'."

**Action:** Send `/get project`

> "Retrieved from DynamoDB in milliseconds."

> "Let's do a full CRUD cycle with the notes system:"

**Action:** Send `/newnote AWS Lambda | Serverless compute service`

> "CREATE - A new note is written to DynamoDB. Notice the generated note_id."

**Action:** Copy note_id, send `/readnote <id>`

> "READ - Retrieved the note we just created."

**Action:** Send `/updatenote <id> | Updated Title | New content`

> "UPDATE - Modified the existing DynamoDB item."

**Action:** Send `/mynotes`

> "LIST - Query operation showing all notes for this user."

**Action:** Send `/deletenote <id>`

> "DELETE - Removed from DynamoDB. Full CRUD cycle complete."

---

### **Part 4: S3 File Storage (1 min)**

> "Next, let's demonstrate S3 integration for file storage."

**Action:** Send a photo

> "The file is uploaded to S3 with server-side encryption. Metadata is stored in DynamoDB for quick retrieval."

**Action:** Send `/myfiles`

> "Here's the file metadata from DynamoDB, including S3 keys, file sizes, and upload dates."

**Action:** Send `/fileinfo <file_id>`

> "Detailed file information shows the S3 object key and bucket location."

---

### **Part 5: CloudWatch Monitoring (30 sec)**

> "Let's trigger a test error to demonstrate CloudWatch monitoring."

**Action:** Send `/testerror`

**Switch to CloudWatch Console:**

> "Here in CloudWatch Logs, you can see the structured JSON log entry with full error details and stack trace. Our metric filter detects errors and feeds into this alarm."

**Show CloudWatch Alarm:**

> "The alarm triggers when we exceed 5 errors in 5 minutes, sending notifications via SNS."

---

### **Part 6: Architecture Walkthrough (1 min)**

**Switch to architecture diagram:**

> "Let me walk through the architecture:
> 
> 1. Telegram sends webhook to API Gateway
> 2. API Gateway triggers Lambda function
> 3. Lambda processes messages using Groq API for AI
> 4. Data persists to DynamoDB
> 5. Files stored in S3 with encryption
> 6. All actions logged to CloudWatch
> 7. Metric filters and alarms monitor health"

---

### **Part 7: Terraform Destroy (30 sec)**

**Switch to terminal:**

```bash
cd terraform
terraform destroy
```

> "Terraform will now clean up all resources: API Gateway, Lambda, DynamoDB table, S3 bucket, IAM roles, and CloudWatch resources. This demonstrates our complete infrastructure-as-code approach."

---

## 🔍 Questions to Anticipate

### Q: How do you handle Groq API failures?

**Answer:** 
"We implement retry logic with exponential backoff - 3 attempts with 1s, 2s, 4s delays. Rate limiting is handled with user-friendly messages. All failures are logged to CloudWatch with error details."

**Demo:** Show error handling code in handler.py

### Q: How secure are the API keys?

**Answer:**
"API keys are stored as Lambda environment variables, encrypted at rest by AWS. For production, we recommend AWS Secrets Manager with automatic rotation. Keys are never hardcoded or committed to git."

**Demo:** Show environment variables in Lambda console (with values hidden)

### Q: What are the scalability limits?

**Answer:**
"Lambda scales automatically up to account limits (1000 concurrent executions by default). DynamoDB uses on-demand billing for auto-scaling. S3 has no limits. We implement rate limiting per user to prevent abuse."

### Q: How do you monitor costs?

**Answer:**
"We use CloudWatch metrics for invocations, DynamoDB capacity units, and S3 storage. AWS Cost Explorer tracks spending. With our current usage, costs are ~$3-5/month, mostly DynamoDB and Lambda."

**Demo:** Show CloudWatch metrics dashboard

---

## 📊 Metrics to Show

### During Demo, Reference These Numbers:

- **Lambda execution time:** 500ms - 2s average
- **DynamoDB response time:** <10ms for get/put
- **S3 upload time:** <1s for typical images
- **Groq API latency:** 1-3s depending on model
- **Total cost:** ~$3-5/month for moderate usage

---

## 🎯 Success Criteria

Your demo is successful if you show:

- ✅ 3+ bot commands working (aim for 10+)
- ✅ DynamoDB CREATE and READ (show full CRUD)
- ✅ S3 upload and list (show multiple file types)
- ✅ CloudWatch logs with recent interaction
- ✅ External API (Groq) returning useful data
- ✅ Error handling and retry logic
- ✅ Terraform infrastructure
- ✅ Clean terraform destroy

---

## 💡 Pro Tips for Demo

1. **Have backup commands ready** - If one fails, move to next
2. **Keep terminal windows prepared** - AWS Console tabs already open
3. **Screenshot key moments** - Logs, metrics, successful operations
4. **Time yourself** - Practice the 5-minute flow
5. **Prepare for questions** - Know your architecture cold
6. **Have rollback plan** - If demo bot breaks, have screenshots/video

---

## 🚨 Emergency Backup Plan

If bot stops responding during demo:

1. **Check webhook:**
   ```bash
   curl "https://api.telegram.org/bot${TOKEN}/getWebhookInfo"
   ```

2. **Check Lambda logs immediately:**
   ```bash
   aws logs tail /aws/lambda/telegram-bot-lambda --follow
   ```

3. **Have screenshots ready** - Show successful test runs from earlier

4. **Have video recording** - Record a successful run beforehand as backup

---

## ✅ Final Pre-Demo Test

**Run this sequence 1 hour before presentation:**

```
/start
Hello!
/save test value
/get test
/newnote Test | Content
/mynotes
[Send photo]
/myfiles
/stats
/testerror
```

**Check AWS Console:**
- CloudWatch logs flowing
- DynamoDB items created
- S3 file uploaded
- No errors in metrics

**If all pass: You're ready! 🚀**

---

**Good luck with your presentation! 🎉**
