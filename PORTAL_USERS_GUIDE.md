# AMMA CMS Portal User Management Guide

## Overview

The AMMA CMS Portal now supports multiple portal users with permission-based access control. This guide explains how to create and manage portal users who can update website content without accessing the Django admin panel.

---

## Key Concepts

### 1. **User Types**

- **Superuser (You)**: Full access to everything including Django admin panel
- **Portal Users**: Can log in to the portal and manage content based on assigned permissions
- **Staff Members (Database)**: These are NOT users - they are just data displayed on the website

### 2. **Portal vs Admin**

- **Django Admin Panel** (`/admin/`): Only superusers can access this
- **AMMA CMS Portal** (`/portal/`): Portal users access this to manage content
- Portal users are blocked from accessing `/admin/` by middleware

### 3. **Permissions**

Portal users can be assigned these permissions:
- **Can manage news articles**: Create, edit, delete news
- **Can manage services**: Create, edit, delete services
- **Can manage projects**: Create, edit, delete projects (future feature)

---

## How to Create a Portal User

### Step 1: Log in to Django Admin

1. Go to: `http://your-site.com/admin/`
2. Log in with your superuser credentials

### Step 2: Create the User

1. Click on **"Users"** under **Authentication and Authorization**
2. Click **"Add User"** button (top right)
3. Enter the username and password
4. Click **"Save and continue editing"**

### Step 3: Configure User Permissions

**Important Settings:**

1. **Personal Info Section:**
   - Set first name and last name (optional)
   - Set email address (recommended for password resets)

2. **Permissions Section:**
   - ✅ Check **"Staff status"** (REQUIRED - this allows portal login)
   - ❌ Leave **"Superuser status"** UNCHECKED (they should NOT be superuser)

3. **User Permissions Section:**
   - Scroll down to find these permissions:
     - `auth | group | Can manage news articles`
     - `auth | group | Can manage services`
     - `auth | group | Can manage projects`
   - Select the permissions this user should have
   - Use Ctrl+Click (or Cmd+Click on Mac) to select multiple
   - Click the arrow button to move them to "Chosen permissions"

4. Click **"Save"** at the bottom

### Example Configuration

For a user who should only manage news:
- ✅ Staff status: **Checked**
- ❌ Superuser status: **Unchecked**
- Permissions: `Can manage news articles` only

For a user who can manage both news and services:
- ✅ Staff status: **Checked**
- ❌ Superuser status: **Unchecked**
- Permissions: `Can manage news articles` + `Can manage services`

---

## What Portal Users Can Do

### When They Log In

1. Portal users go to: `http://your-site.com/admin/login/`
2. After logging in, they are automatically redirected to `/portal/`
3. If they try to access `/admin/`, they are blocked and redirected to `/portal/`

### Dashboard

Portal users see a dashboard showing:
- Statistics for content they have permission to manage
- Quick action buttons (only for permitted sections)
- Navigation menu (only shows permitted sections)

### Permissions in Action

**With "Can manage news articles" permission:**
- ✅ Can create, edit, delete news articles
- ✅ Can create news categories
- ✅ See "News" in navigation menu
- ✅ See news statistics on dashboard

**With "Can manage services" permission:**
- ✅ Can create, edit, delete services
- ✅ Can create content blocks for services
- ✅ See "Services" in navigation menu
- ✅ See service statistics on dashboard

**Without permission:**
- ❌ Cannot see the section in navigation
- ❌ Cannot access the URLs (redirected to dashboard)
- ❌ Statistics show as 0 on dashboard

---

## How to Edit Portal User Permissions

### Adding/Removing Permissions

1. Go to Django Admin (`/admin/`)
2. Click **"Users"**
3. Click on the username
4. Scroll to **"User permissions"**
5. Add or remove permissions as needed
6. Click **"Save"**

### Removing Portal Access

To remove someone's portal access entirely:
1. Go to Django Admin → Users → Click username
2. **Uncheck "Staff status"**
3. Click **"Save"**

The user will no longer be able to log into the portal.

### Deleting a User

1. Go to Django Admin → Users
2. Check the checkbox next to the user
3. Select "Delete selected users" from the Action dropdown
4. Click "Go"
5. Confirm deletion

---

## Troubleshooting

### User Can't Log In

**Check:**
1. Is "Staff status" checked?
2. Is the password correct?
3. Is the account active? (Active checkbox should be checked)

### User Gets "Permission Denied" Error

**Check:**
1. Do they have the right permission assigned?
2. Permission names must match exactly:
   - `Can manage news articles`
   - `Can manage services`
   - `Can manage projects`

### User Sees Empty Dashboard

This is normal if they have no permissions assigned. They can log in but can't do anything until you assign permissions.

### User Accidentally Got Admin Access

**If a portal user becomes a superuser:**
1. Edit the user in Django Admin
2. **Uncheck "Superuser status"**
3. Save
4. They will now be blocked from `/admin/`

---

## Best Practices

### 1. **Use Groups for Common Permission Sets**

Instead of assigning permissions to each user individually:

1. Create a Group (Django Admin → Groups)
2. Assign permissions to the group
3. Add users to the group

**Example Groups:**
- **News Editors**: `Can manage news articles`
- **Service Managers**: `Can manage services`
- **Content Managers**: All permissions

### 2. **Regular Permission Audits**

Periodically review who has access:
1. Go to Django Admin → Users
2. Filter by "Staff status"
3. Review each user's permissions
4. Remove unnecessary permissions

### 3. **Use Strong Passwords**

When creating portal users:
- Use Django's password generator
- Require users to change password on first login
- Set password expiration policies (optional)

### 4. **Keep Superuser Accounts Minimal**

Only you (the admin) should be a superuser. All content editors should be portal users with specific permissions.

---

## Quick Reference

### Portal User Checklist
- [ ] Username and password set
- [ ] Staff status: ✅ **Checked**
- [ ] Superuser status: ❌ **Unchecked**
- [ ] At least one permission assigned
- [ ] Email address set (recommended)

### Permission Codenames
For reference when working with code:
- `auth.can_manage_news`
- `auth.can_manage_services`
- `auth.can_manage_projects`

### Important URLs
- Django Admin: `/admin/`
- Portal Login: `/admin/login/` (redirects to portal after login)
- Portal Dashboard: `/portal/`

---

## Technical Details

### Files Modified
- `apps/staff_portal/permissions.py` - Permission definitions
- `apps/staff_portal/middleware.py` - Blocks admin access
- `apps/staff_portal/decorators.py` - Permission decorators
- `apps/staff_portal/views.py` - Permission checks
- `apps/staff_portal/context_processors.py` - Template permissions
- `config/settings.py` - Middleware and context processor registration

### Database Changes
- Created custom permissions via migration
- Permissions stored in `auth_permission` table
- User permissions stored in `auth_user_user_permissions` table

---

## Support

If you encounter issues with the portal user system:

1. Check this guide first
2. Verify Django admin settings
3. Check the user's permissions in Django admin
4. Ensure migrations are up to date: `python manage.py migrate`
5. Check for errors: `python manage.py check`

Remember: Staff Members (in database) ≠ Portal Users (actual people who log in)
