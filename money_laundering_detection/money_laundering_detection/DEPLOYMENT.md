# 🚀 Production Deployment Guide

## ⚠️ **IMPORTANT: Development vs Production**

**NEVER use Flask's built-in server in production!** It's single-threaded, insecure, and not suitable for real-world use.

## 🎯 **Production Deployment Options**

### **Option 1: Waitress (Windows/Linux - Recommended)**

Waitress is a pure Python WSGI server that's production-ready and cross-platform.

```bash
# Install Waitress
pip install waitress

# Run production server
python run_production.py
```

**Benefits:**
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Pure Python (no C dependencies)
- ✅ Production-ready
- ✅ Easy to configure

### **Option 2: Gunicorn (Linux/Unix)**

Gunicorn is a high-performance WSGI server for Unix systems.

```bash
# Install Gunicorn
pip install gunicorn

# Run production server
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

**Benefits:**
- ✅ High performance
- ✅ Process management
- ✅ Load balancing
- ✅ Industry standard

### **Option 3: uWSGI (Advanced)**

uWSGI is a full-featured WSGI server with advanced features.

```bash
# Install uWSGI
pip install uwsgi

# Run production server
uwsgi --http 0.0.0.0:5000 --module wsgi:app --processes 4 --threads 2
```

## 🔧 **Production Configuration**

### **Environment Variables**

Create a `.env` file (never commit this to version control):

```bash
# .env file
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key
HOST=0.0.0.0
PORT=5000
THREADS=4
DATABASE_URL=your_database_connection_string
```

### **Security Settings**

The production config automatically enables:
- ✅ Secure cookies
- ✅ HTTPS headers
- ✅ XSS protection
- ✅ Content type protection
- ✅ Frame protection

## 🚀 **Quick Production Start**

### **For Windows Users:**

```bash
# Stop the development server (Ctrl+C)
# Then run:
python run_production.py
```

### **For Linux/Unix Users:**

```bash
# Stop the development server (Ctrl+C)
# Then run:
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

## 🌐 **Production Features**

✅ **Multi-threaded**: Handle multiple requests simultaneously
✅ **Security**: Production-grade security headers
✅ **Performance**: Optimized for high traffic
✅ **Monitoring**: Better error handling and logging
✅ **Scalability**: Can handle production workloads

## 📊 **Performance Comparison**

| Server Type | Threads | Security | Performance | Production Ready |
|-------------|---------|----------|-------------|------------------|
| Flask Dev   | 1       | ❌       | ❌          | ❌               |
| Waitress    | 4+      | ✅       | ✅          | ✅               |
| Gunicorn    | 4+      | ✅       | ✅✅        | ✅               |
| uWSGI       | 4+      | ✅       | ✅✅✅      | ✅               |

## 🔒 **Security Checklist**

- [ ] `FLASK_ENV=production`
- [ ] `DEBUG=False`
- [ ] Strong `SECRET_KEY`
- [ ] HTTPS enabled (in production)
- [ ] Secure headers enabled
- [ ] File upload limits set
- [ ] Error messages sanitized

## 📝 **Production Commands**

### **Start Production Server:**
```bash
# Windows
python run_production.py

# Linux
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# With environment
FLASK_ENV=production python run_production.py
```

### **Stop Server:**
```bash
# Press Ctrl+C in the terminal
```

### **Check Server Status:**
```bash
# Check if port is listening
netstat -an | grep 5000
```

## 🚨 **Emergency Fallback**

If production server fails, you can temporarily use:

```bash
# Only for emergency use!
FLASK_ENV=production python app.py
```

**But immediately fix the production server!**

## 🎯 **Next Steps**

1. **Stop Development Server**: Ctrl+C in current terminal
2. **Install Production Dependencies**: `pip install waitress`
3. **Run Production Server**: `python run_production.py`
4. **Test**: Visit `http://localhost:5000`
5. **Monitor**: Check for any errors

## ✅ **Success Indicators**

- ✅ No "development server" warnings
- ✅ Multiple threads available
- ✅ Security headers enabled
- ✅ Better performance
- ✅ Production-ready logging

Your Money Laundering Detection System is now **production-ready**! 🎉
