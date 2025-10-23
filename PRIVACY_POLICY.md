# 🔒 TTZ.KT AI - Privacy Policy & Data Handling

## Privacy-First Architecture

**Last Updated:** 2025
**Effective Date:** Upon Deployment

---

## 🎯 Our Commitment

**We do NOT store, save, or retain ANY of your documents or data.**

This is not just a policy - it's built into our architecture. We literally **cannot** access your documents because we don't store them.

---

## 📋 How It Works

### What Happens When You Upload a Document:

```
1. You upload document
   ↓
2. Document processed in memory (RAM) only
   ↓
3. Temporary vector embeddings created (RAM)
   ↓
4. You ask questions and get answers
   ↓
5. You close browser
   ↓
6. ALL DATA AUTOMATICALLY DELETED ✅
```

### Technical Details:

- ✅ **No disk storage** - Documents never touch permanent storage
- ✅ **Memory-only processing** - All processing in volatile RAM
- ✅ **Temporary files deleted immediately** - Any temp files removed instantly
- ✅ **Session-based** - Each browser session is isolated
- ✅ **Auto-cleanup** - Data cleared when session ends

---

## 🔐 What We DON'T Store

### We do NOT store:
- ❌ Your uploaded documents
- ❌ Document contents
- ❌ Vector embeddings
- ❌ Chat history (after session)
- ❌ Questions you ask
- ❌ Answers provided
- ❌ Personal information
- ❌ Email addresses
- ❌ IP addresses (beyond basic Streamlit logs)
- ❌ Usage patterns

### What This Means:
**If someone hacked our servers, they would find ZERO user documents. Because we don't have them!** 🔒

---

## ✅ What We DO Use

### OpenAI API:
- Your questions and documents are sent to OpenAI's API for processing
- OpenAI's data usage policy applies: https://openai.com/policies/privacy-policy
- OpenAI does NOT train on API data (as of their current policy)

### Streamlit Cloud (if deployed there):
- Basic hosting logs (standard for any web service)
- Session management (standard for web apps)
- No document content in logs

---

## 🌍 Data Location

### During Processing:
- **Location:** RAM of Streamlit Cloud server (USA/Europe depending on deployment)
- **Duration:** Only while your browser session is active
- **Access:** Only you, via your browser

### After Session Ends:
- **Location:** Nowhere - completely deleted
- **Duration:** N/A - doesn't exist
- **Access:** Nobody - data is gone

---

## 🔒 Security Measures

### Technical Security:
1. **Memory-only architecture** - No permanent storage
2. **HTTPS encryption** - All communication encrypted
3. **Session isolation** - Each user's session is separate
4. **Immediate deletion** - Temp files removed instantly
5. **No database** - No database to breach

### Privacy by Design:
- We **cannot** access your documents (they're not stored)
- We **cannot** recover your documents (they're deleted)
- We **cannot** share your documents (we don't have them)

---

## 👥 Multi-User Privacy

### User Isolation:
```
User A uploads document → Processes in Session A
User B uploads document → Processes in Session B

Sessions are SEPARATE
Users CANNOT see each other's documents ✅
```

### What This Means:
- Your documents are private to your browser session
- Other users cannot access your documents
- Even we (the operators) cannot access your documents

---

## ⚖️ Compliance

### GDPR Compliant:
- ✅ **Right to be forgotten:** Automatic - data deleted after session
- ✅ **Data minimization:** We don't store anything
- ✅ **Purpose limitation:** Data used only for your queries
- ✅ **Storage limitation:** Zero permanent storage
- ✅ **Data portability:** N/A - we don't store your data

### HIPAA Considerations:
- ⚠️ **Not HIPAA certified** - Don't use for regulated healthcare data
- ⚠️ Even though we don't store data, OpenAI API is involved
- ⚠️ For HIPAA compliance, use on-premise deployment

### General Compliance:
- ✅ No data retention = Minimal compliance risk
- ✅ Reduced liability
- ✅ Simple privacy policy

---

## 📊 What Users Should Know

### Before Using:

**Advantages:**
- ✅ Maximum privacy
- ✅ Your data is never stored
- ✅ No data breach risk
- ✅ Automatic cleanup

**Trade-offs:**
- ⚠️ Must re-upload documents each session
- ⚠️ Cannot resume from different device
- ⚠️ Data sent to OpenAI API (their policy applies)
- ⚠️ Session ends → data gone (expected behavior)

---

## 🎯 Use Cases

### Perfect For:
- ✅ Sensitive business documents
- ✅ Personal information
- ✅ Confidential contracts
- ✅ Private research
- ✅ Legal documents
- ✅ Financial records
- ✅ Medical records (non-HIPAA)
- ✅ Any privacy-sensitive content

### Not Ideal For:
- ⚠️ Long-term document repositories
- ⚠️ Team collaboration requiring persistence
- ⚠️ Large datasets needing repeated access
- ⚠️ HIPAA-regulated healthcare data

---

## 🔄 Session Lifecycle

### During Active Session:
```
Browser Open → Document in RAM → Can query → Get answers
```

### When Session Ends:
```
Close Browser → RAM cleared → Document GONE → Cannot recover
```

### Starting New Session:
```
Open Browser → Fresh start → Must re-upload → New processing
```

---

## 🆘 User Rights

### Your Rights:
1. **Access:** See your data during active session (in browser)
2. **Deletion:** Automatic when session ends (or click Reset button)
3. **Portability:** N/A - we don't store your data
4. **Rectification:** N/A - we don't store your data
5. **Restriction:** Close browser = data deleted

### How to Exercise Rights:
- **Delete immediately:** Click "Reset" button in app
- **Delete after session:** Just close browser
- **Prevent tracking:** We don't track (nothing to prevent)

---

## 📞 Contact

### Questions about Privacy:
- Review this policy
- Check our GitHub: https://github.com/tharun-kumar-22/openai_docs_assistant
- For technical questions: Open GitHub issue

### Data Breaches:
**Risk Level: Minimal** - We don't store data, so nothing to breach!

If hypothetically something happened:
- We would notify via GitHub repository
- But realistically: No data stored = No data breached

---

## 🔄 Policy Updates

### Changes:
- Any changes will be posted to GitHub
- Version-controlled in repository
- Check regularly for updates

### Current Version:
- **Version:** 1.0
- **Date:** 2025
- **Architecture:** Memory-only (no plans to change)

---

## ⚖️ Legal Disclaimers

### Service "As-Is":
- Provided without warranties
- Use at your own risk
- We are not liable for OpenAI API behavior

### Third-Party Services:
- OpenAI API: https://openai.com/policies/privacy-policy
- Streamlit Cloud: https://streamlit.io/privacy-policy
- Their policies apply to their services

### Recommendations:
- ✅ Review sensitive documents before uploading
- ✅ Don't upload highly regulated data (HIPAA, etc.)
- ✅ Remember: session-based = temporary
- ✅ For maximum security: Self-host on-premise

---

## 🌟 Our Philosophy

**"The best data protection is not storing data at all."**

We believe in:
- Privacy by design
- Minimal data collection
- User control
- Transparency

---

## ✅ Summary

### What Makes Us Different:

**Traditional Apps:**
```
Upload → Store in database → Process → Keep forever
Risk: Data breaches, compliance, liability
```

**TTZ.KT AI:**
```
Upload → Process in RAM → Answer → Delete
Risk: Minimal (no storage = no breach)
```

### Your Data Journey:

```
Your Computer → Our RAM → OpenAI API → Answer → Deleted
                ↓
           Temporary only
                ↓
        Automatic deletion
                ↓
           Gone forever ✅
```

---

## 🎉 Bottom Line

**We built this app specifically to NOT store your data.**

**Why?**
- Maximum privacy for users
- Minimal liability for us
- Simple compliance
- User trust

**Result:**
- ✅ Your data stays private
- ✅ No data breaches possible
- ✅ Clean architecture
- ✅ Peace of mind

---

**Your privacy = Our priority** 🔒

---

*This is a privacy-first application. We cannot access your documents because we don't store them. It's that simple.*
