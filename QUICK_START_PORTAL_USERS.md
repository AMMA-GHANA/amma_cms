# Quick Start: Creating Your First Portal User

## 5-Minute Setup Guide

### Step 1: Access Django Admin (30 seconds)
1. Go to: `http://your-site.com/admin/`
2. Log in with your superuser account

### Step 2: Create User (1 minute)
1. Click **"Users"** in the left sidebar
2. Click **"ADD USER +"** (top right)
3. Fill in:
   - Username: `editor1` (or any name)
   - Password: (set a strong password)
4. Click **"SAVE and continue editing"**

### Step 3: Configure Permissions (2 minutes)
1. Scroll to **"Permissions"** section
2. ✅ **Check** "Staff status"
3. ❌ **Leave unchecked** "Superuser status"
4. Scroll to **"User permissions"**
5. Find and select (use Ctrl+Click):
   - `auth | group | Can manage news articles`
   - `auth | group | Can manage services`
6. Click the **→** arrow to move to "Chosen permissions"
7. Click **"SAVE"** at the bottom

### Step 4: Test It (1.5 minutes)
1. Open a private/incognito browser window
2. Go to: `http://your-site.com/admin/login/`
3. Log in with the new user credentials
4. You should be redirected to `/portal/` dashboard
5. Try accessing `/admin/` - you'll be blocked ✅
6. Navigate to News or Services - it works! ✅

---

## Quick Reference

### Required Settings for Portal User
- ✅ Staff status: **Checked**
- ❌ Superuser status: **Unchecked**
- At least one permission from:
  - Can manage news articles
  - Can manage services
  - Can manage projects

### Common Permission Sets

**News Editor Only:**
- `Can manage news articles`

**Service Manager Only:**
- `Can manage services`

**Full Content Manager:**
- `Can manage news articles`
- `Can manage services`
- `Can manage projects`

---

## Troubleshooting

**User can't log in?**
→ Check "Staff status" is checked

**User sees empty dashboard?**
→ Assign at least one permission

**User can access admin panel?**
→ Uncheck "Superuser status"

**Navigation menu empty?**
→ Permissions not assigned correctly

---

## What's Next?

1. ✅ Create your first portal user (you just did this!)
2. Read `PORTAL_USERS_GUIDE.md` for detailed instructions
3. Create more users as needed
4. Consider creating Groups for common permission sets

---

## Need Help?

- **Detailed Guide**: See `PORTAL_USERS_GUIDE.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Technical Support**: Run `python manage.py check` for errors

---

That's it! You now have a multi-user portal system. 🎉
