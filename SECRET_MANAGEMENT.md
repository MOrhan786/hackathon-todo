# 🔐 Secret Management Guide

This document explains how to manage secrets and environment variables securely in this project.

## ⚠️ Critical Security Rules

1. **NEVER commit secrets to version control** - API keys, database passwords, JWT secrets, etc.
2. **ALWAYS use `.env.example` files** as templates for required environment variables
3. **Rotate secrets immediately** if they are accidentally committed
4. **Use different secrets** for development, staging, and production

---

## 📁 Environment Files Structure

```
project-root/
├── .env.example              # Template for root-level env vars (if needed)
├── backend/
│   ├── .env.example          # ✅ Safe to commit - template with placeholder values
│   └── .env                  # ❌ NEVER commit - contains actual secrets
├── frontend/
│   ├── .env.local.example    # ✅ Safe to commit - template
│   └── .env.local            # ❌ NEVER commit - contains actual config
└── helm/
    └── todo-app/
        ├── values.yaml       # ✅ Safe - placeholder values only
        └── values-secrets.yaml  # ❌ NEVER commit - actual secrets (create locally)
```

---

## 🚀 Quick Start Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Copy the example environment file
cp .env.example .env

# Edit .env with your actual secrets
# IMPORTANT: .env is gitignored - never commit it!
```

### 2. Generate Secure Keys

```bash
# Generate JWT Secret Key (64 character hex string)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# Generate JWT Refresh Secret Key
JWT_REFRESH_SECRET_KEY=$(openssl rand -hex 32)

# Example output:
# JWT_SECRET_KEY=a3f8b2c1d4e5f6789012345678901234567890123456789012345678901234
```

### 3. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add it to your `.env` file

### 4. Configure Database URL

```bash
# Local PostgreSQL example:
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/todo_db

# Production example (use environment-specific credentials):
DATABASE_URL=postgresql://user:password@host:port/database
```

---

## 📝 Required Environment Variables

### Backend (FastAPI)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET_KEY` | ✅ | Secret for JWT access tokens | `openssl rand -hex 32` |
| `JWT_REFRESH_SECRET_KEY` | ✅ | Secret for JWT refresh tokens | `openssl rand -hex 32` |
| `OPENAI_API_KEY` | ✅ | OpenAI API key for chatbot | `sk-...` |
| `SERVER_HOST` | ❌ | Server host (default: `0.0.0.0`) | `0.0.0.0` |
| `SERVER_PORT` | ❌ | Server port (default: `8000`) | `8000` |
| `DEBUG` | ❌ | Debug mode (default: `False`) | `False` |
| `KAFKA_BOOTSTRAP_SERVERS` | ❌ | Kafka servers (default: `localhost:9092`) | `redpanda:9092` |
| `KAFKA_ENABLED` | ❌ | Enable Kafka (default: `False`) | `True` |
| `DAPR_ENABLED` | ❌ | Enable Dapr (default: `False`) | `False` |

### Frontend (Next.js)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | ✅ | Backend API URL | `http://localhost:8000` |
| `NODE_ENV` | ❌ | Environment (default: `development`) | `production` |

---

## 🛡️ Security Best Practices

### 1. Use Strong Secrets

```bash
# ✅ Good: Random 64-character hex string
JWT_SECRET_KEY=$(openssl rand -hex 32)

# ❌ Bad: Predictable or short secrets
JWT_SECRET_KEY="mysecret123"
```

### 2. Environment-Specific Secrets

Use different secrets for each environment:

```bash
# Development
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/todo_dev

# Staging
DATABASE_URL=postgresql://staging_user:staging_pass@staging-db:5432/todo_staging

# Production
DATABASE_URL=postgresql://prod_user:prod_pass@prod-db:5432/todo_prod
```

### 3. Kubernetes Secrets

For Helm deployments, use Kubernetes secrets:

```bash
# Create secret (values are base64 encoded automatically)
kubectl create secret generic backend-secret \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=OPENAI_API_KEY="sk-..." \
  --from-literal=JWT_SECRET_KEY="..." \
  --from-literal=JWT_REFRESH_SECRET_KEY="..." \
  -n todo-app

# Reference in Helm values.yaml
secrets:
  DATABASE_URL: ""  # Will be overridden by Kubernetes secret
```

### 4. Docker Compose Secrets

```yaml
# docker-compose.yml
services:
  backend:
    env_file:
      - ./backend/.env  # Make sure this file exists and is NOT committed
```

---

## 🔍 If You Accidentally Commit Secrets

### 1. Rotate Immediately

- Change your OpenAI API key
- Generate new JWT secrets
- Change database passwords

### 2. Remove from Git History

```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove the file from history
git-filter-repo --path backend/.env --invert-paths

# Force push (WARNING: rewrites history)
git push --force --all
```

### 3. Check for Leaks

- Review GitHub commits for exposed secrets
- Check if secrets were pushed to any public branches
- Monitor API usage for unauthorized access

---

## 🧪 Testing with Environment Variables

### Local Testing

```bash
# Backend tests automatically use .env file
cd backend
pytest

# Or run with explicit environment
export DATABASE_URL=postgresql://test@localhost:5432/test_db
export OPENAI_API_KEY=sk-test-key
python test_openai.py
```

### CI/CD Testing

Use GitHub Secrets or your CI provider's secret management:

```yaml
# .github/workflows/test.yml
jobs:
  test:
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      JWT_SECRET_KEY: ${{ secrets.JWT_SECRET_KEY }}
```

---

## 📋 Checklist Before Committing

- [ ] No `.env` files are staged for commit
- [ ] No hardcoded API keys in source code
- [ ] No database passwords in configuration files
- [ ] `.env.example` files have placeholder values (not real secrets)
- [ ] `values-secrets.yaml` or similar files are in `.gitignore`
- [ ] All team members know how to set up their local `.env` files

---

## 🆘 Troubleshooting

### "Environment variable not set" errors

```bash
# Check if .env file exists
ls -la backend/.env

# Check file permissions
chmod 600 backend/.env

# Verify variable names match exactly (case-sensitive)
cat backend/.env
```

### "Invalid API key" errors

1. Verify the key starts with `sk-`
2. Check for extra spaces or quotes
3. Ensure you're using the correct key type (secret key, not publishable key)

### Database connection errors

1. Verify PostgreSQL is running
2. Check database name, username, and password
3. Ensure the database user has proper permissions

---

## 📚 Additional Resources

- [12-Factor App: Config](https://12factor.net/config)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [PostgreSQL Connection Strings](https://www.postgresql.org/docs/current/libpq-connect.html)
- [JWT Best Practices](https://auth0.com/blog/jwt-security-best-practices/)

---

**Last Updated**: March 2026  
**Version**: 1.0
