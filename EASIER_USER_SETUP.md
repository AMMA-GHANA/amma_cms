# Easier Way: Using Groups for Portal Users

## Why Use Groups?

Instead of assigning permissions to each user individually (which means scrolling through hundreds of permissions every time), create **Groups** with pre-set permissions, then just add users to groups.

---

## One-Time Setup: Create Groups

### Step 1: Create "News Editors" Group

1. Go to Django Admin (`/admin/`)
2. Click **"Groups"** (under Authentication and Authorization)
3. Click **"ADD GROUP +"**
4. Name: `News Editors`
5. In the "Available permissions" box, search or scroll to find:
   - `auth | group | Can manage news articles`
6. Select it and click the **→** arrow to move it to "Chosen permissions"
7. Click **"SAVE"**

### Step 2: Create "Service Managers" Group

1. Click **"ADD GROUP +"** again
2. Name: `Service Managers`
3. Select permission:
   - `auth | group | Can manage services`
4. Click **"SAVE"**

### Step 3: Create "Content Managers" Group (Optional)

1. Click **"ADD GROUP +"**
2. Name: `Content Managers`
3. Select ALL our custom permissions:
   - `auth | group | Can manage news articles`
   - `auth | group | Can manage services`
   - `auth | group | Can manage projects`
4. Click **"SAVE"**

---

## Creating Users (The Easy Way)

Now when you create a portal user:

1. Go to **"Users"** → **"ADD USER +"**
2. Set username and password
3. Click **"SAVE and continue editing"**
4. Set permissions:
   - ✅ Check "Staff status"
   - ❌ Leave "Superuser status" unchecked
5. **Scroll to "Groups"** (much easier to find!)
6. Select the appropriate group:
   - `News Editors` - for news only
   - `Service Managers` - for services only
   - `Content Managers` - for everything
7. Click the **→** arrow to add them to the group
8. Click **"SAVE"**

That's it! No scrolling through hundreds of permissions.

---

## Quick Reference

### Group Permissions

| Group Name | Permissions | Use For |
|------------|-------------|---------|
| News Editors | Can manage news articles | People who only update news |
| Service Managers | Can manage services | People who only update services |
| Content Managers | All three permissions | People who manage everything |

---

## Visual Guide

**EASIER WAY (Using Groups):**
```
Create User → Set Staff Status → Add to Group → Done!
              ✅ Staff status     (News Editors)
              ❌ Superuser
```

**HARDER WAY (Individual Permissions):**
```
Create User → Set Staff Status → Scroll through 200+ permissions → Find 3 specific ones → Done!
```

---

## Finding Groups in User Form

When editing a user, the **"Groups"** section appears BEFORE the "User permissions" section:

```
Personal info
  ├─ Username
  ├─ First name
  └─ Last name

Permissions
  ├─ Active
  ├─ Staff status        ← Check this
  └─ Superuser status    ← Leave unchecked

Groups                   ← ADD USER TO GROUP HERE (EASY!)
  └─ Available groups:
      ├─ News Editors
      ├─ Service Managers
      └─ Content Managers

User permissions         ← Or scroll through 200+ here (HARD!)
  └─ Available user permissions:
      ├─ 200+ permissions to scroll through...
      └─ ...
```

---

## Recommendation

**✅ Use Groups** - Easier to manage, faster to assign, better for multiple users

**❌ Individual Permissions** - Only use if you need very specific custom access

---

## Example Scenarios

### Scenario 1: New news editor
1. Create user
2. Staff status: ✅
3. Add to group: "News Editors"
4. Done in 30 seconds!

### Scenario 2: Someone who manages both news and services
1. Create user
2. Staff status: ✅
3. Add to groups: "News Editors" AND "Service Managers" (you can add to multiple)
4. Done!

### Scenario 3: Full content manager
1. Create user
2. Staff status: ✅
3. Add to group: "Content Managers"
4. Done!

---

## Pro Tip: Edit Groups Anytime

If you want to change what permissions a role has:

1. Go to **Groups** → Click the group name
2. Add or remove permissions
3. Save
4. **All users in that group automatically get the updated permissions!**

No need to edit each user individually.

---

This is the recommended approach for managing multiple portal users!
