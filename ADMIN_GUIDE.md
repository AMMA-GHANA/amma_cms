# AMMA CMS Admin Guide

Complete guide for managing content in the Asokore Mampong Municipal Assembly Content Management System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Accessing the Admin Panel](#accessing-the-admin-panel)
3. [Managing Content](#managing-content)
4. [Adding Images](#adding-images)
5. [Publishing Workflow](#publishing-workflow)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- Admin account credentials (default: username `admin`, password `admin123`)
- Basic understanding of web content management
- Images prepared in appropriate formats (JPG, PNG)

### First Time Setup

1. **Start the Development Server**
   ```bash
   cd /home/mufti/amma_projects/amma_cms
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Populate Sample Data** (if not done already)
   ```bash
   python manage.py populate_sample_data
   ```

3. **Copy Static Images** (optional)
   ```bash
   python manage.py copy_static_images
   ```

---

## Accessing the Admin Panel

### Login

1. Open your browser and navigate to: `http://127.0.0.1:8000/admin/`
2. Enter your credentials:
   - **Username:** `admin`
   - **Password:** `admin123`
3. Click "Log in"

### Admin Dashboard

After logging in, you'll see the main dashboard organized by apps:

- **Core** - Site settings, hero slides, statistics, about section
- **News** - News categories and articles
- **Projects** - Project categories and projects
- **Services** - Municipal services
- **Staff** - Departments and staff members
- **Documents** - Document categories and files
- **Gallery** - Gallery categories and images
- **Contact** - Contact form submissions

---

## Managing Content

### Site Settings

**Location:** Core → Site Settings

Site settings control global information displayed across the website.

#### Editing Site Settings

1. Click on "Site Settings" in the Core section
2. Click on the existing settings record (there should only be one)
3. Update the following fields:
   - **Site Name:** Organization name
   - **Tagline:** Brief motto or tagline
   - **Description:** Short description of the organization
   - **Address:** Physical address
   - **Phone:** Contact phone number
   - **Email:** Contact email address
   - **Social Media Links:** Facebook, Twitter, Instagram, YouTube URLs
   - **Office Hours:** Operating hours
   - **Footer Text:** Text displayed in website footer
4. Upload **Logo** (recommended: 200x200px PNG with transparent background)
5. Upload **Favicon** (16x16px or 32x32px .ico file)
6. Click "Save"

### Hero Slides

**Location:** Core → Hero Slides

Hero slides are the large banner images and text shown at the top of the homepage.

#### Adding a New Hero Slide

1. Navigate to Core → Hero Slides
2. Click "Add Hero Slide" button
3. Fill in the form:
   - **Title:** Main headline (max 200 characters)
   - **Subtitle:** Supporting text (max 300 characters)
   - **Image:** Upload hero image (recommended: 1920x1080px, max 2MB)
   - **Button Text:** Optional CTA button text (e.g., "Learn More")
   - **Button Link:** Optional link URL (e.g., `/about/`)
   - **Order:** Display order (lower numbers appear first)
   - **Is Active:** Check to display on homepage
4. Click "Save"

**Best Practices:**
- Use high-quality, relevant images
- Keep titles short and impactful
- Limit to 3-5 active slides
- Test slides on mobile devices

### Statistics

**Location:** Core → Statistics

Statistics are the number counters displayed on the homepage.

#### Adding/Editing Statistics

1. Navigate to Core → Statistics
2. Click "Add Statistic" or edit existing
3. Fill in:
   - **Label:** Description (e.g., "Total Population")
   - **Value:** Number or text (e.g., "191,402")
   - **Icon:** Icon name (users, briefcase, home, map)
   - **Order:** Display order
   - **Is Active:** Check to display
4. Click "Save"

### News Articles

**Location:** News → News Articles

#### Creating a News Article

1. Navigate to News → News Articles
2. Click "Add News Article"
3. Fill in the form:
   - **Title:** Article headline
   - **Slug:** Auto-generated URL (can be edited)
   - **Excerpt:** Short summary (150-200 characters)
   - **Content:** Full article content (use rich text editor)
   - **Featured Image:** Upload article image (recommended: 1200x800px)
   - **Category:** Select appropriate category
   - **Author:** Select author (usually your admin account)
   - **Status:** Choose:
     - **Draft:** Not visible on website
     - **Published:** Live on website
     - **Archived:** Hidden but preserved
   - **Is Featured:** Check to display on homepage
   - **Published Date:** When to publish (can be future date)
4. Click "Save"

**Rich Text Editor Tips:**
- Use heading styles for structure
- Add images inline using the image button
- Create bulleted/numbered lists for readability
- Add links to related content
- Preview before publishing

### Projects

**Location:** Projects → Projects

#### Adding a Project

1. Navigate to Projects → Projects
2. Click "Add Project"
3. Fill in:
   - **Title:** Project name
   - **Slug:** Auto-generated URL
   - **Description:** Detailed project description
   - **Category:** Select project category
   - **Status:** Completed, Ongoing, or Planned
   - **Start Date:** Project start date
   - **End Date:** Completion date (optional)
   - **Budget:** Project budget (optional)
   - **Impact Text:** Brief impact statement (e.g., "500+ students served")
   - **Impact Icon:** FontAwesome icon name
   - **Is Featured:** Check to display on homepage
   - **Order:** Display order
4. Click "Save and continue editing"
5. Scroll to "Project Images" section
6. Click "Add another Project Image"
7. Upload images and check "Is Primary" for main image
8. Click "Save"

### Services

**Location:** Services → Services

#### Adding a Municipal Service

1. Navigate to Services → Services
2. Click "Add Service"
3. Fill in:
   - **Name:** Service name
   - **Description:** What the service provides
   - **Icon:** FontAwesome icon name (e.g., home, briefcase, certificate)
   - **Link Text:** Button text (e.g., "Apply Now")
   - **Link URL:** Where button links to
   - **Order:** Display order
   - **Is Active:** Check to display
4. Click "Save"

### Staff Members

**Location:** Staff → Staff Members

#### Adding a Staff Member

1. Navigate to Staff → Staff Members
2. Click "Add Staff Member"
3. Fill in:
   - **Full Name:** Complete name
   - **Position:** Job title
   - **Position Type:** Leadership, Management, or Staff
   - **Department:** Select department
   - **Email:** Work email
   - **Phone:** Work phone
   - **Photo:** Upload professional headshot (recommended: 800x800px, square)
   - **Bio:** Brief biography
   - **Display Order:** Order on staff page
   - **Is Active:** Check to display
4. Click "Save"

**Photo Guidelines:**
- Use high-resolution professional photos
- Square aspect ratio (1:1)
- Consistent background across all staff photos
- Good lighting and clear facial features

---

## Adding Images

### Image Requirements

| Image Type | Recommended Size | Max File Size | Format |
|-----------|------------------|---------------|--------|
| Hero Slides | 1920x1080px | 2MB | JPG, PNG |
| Featured Images (News/Projects) | 1200x800px | 1MB | JPG, PNG |
| Staff Photos | 800x800px | 500KB | JPG, PNG |
| Gallery Images | 1200x900px | 1MB | JPG, PNG |
| Logo | 200x200px | 200KB | PNG (transparent) |
| Favicon | 32x32px | 50KB | ICO, PNG |

### Uploading Images

1. In any admin form with an image field, click "Choose File" or "Browse"
2. Select your image file
3. Click "Save" to upload

### Replacing Images

1. In the edit form, you'll see the current image
2. Click "Clear" checkbox to remove current image
3. Choose new file
4. Click "Save"

### Managing Media Files

Uploaded files are stored in `/media/` directory:
- `/media/hero/` - Hero slide images
- `/media/news/` - News article images
- `/media/projects/` - Project images
- `/media/staff/` - Staff photos
- `/media/gallery/` - Gallery images
- `/media/documents/` - Uploaded documents

---

## Publishing Workflow

### Content Lifecycle

1. **Draft** → Create and edit content
2. **Review** → Preview and verify accuracy
3. **Published** → Make live on website
4. **Archived** → Remove from public view but preserve record

### Publishing a News Article

1. Create article with Status = "Draft"
2. Add content and images
3. Set **Published Date** (can be future date for scheduled publishing)
4. Change Status to "Published"
5. Click "Save"
6. Visit website to verify it appears correctly

### Unpublishing Content

To temporarily hide content without deleting:

1. Edit the item
2. Change Status to "Draft" or uncheck "Is Active"
3. Click "Save"

---

## Common Tasks

### Changing Homepage Hero Slides

1. Go to Core → Hero Slides
2. To reorder: Change the "Order" field numbers
3. To hide: Uncheck "Is Active"
4. To add new: Click "Add Hero Slide"

### Featuring Content on Homepage

**Featured News:**
1. Edit news article
2. Check "Is Featured" checkbox
3. Save (limited to 3 on homepage)

**Featured Projects:**
1. Edit project
2. Check "Is Featured" checkbox
3. Save (limited to 3 on homepage)

### Updating Contact Information

1. Go to Core → Site Settings
2. Update phone, email, address fields
3. Update social media links
4. Click "Save"

### Adding a New Service

1. Go to Services → Services
2. Click "Add Service"
3. Fill in details
4. Choose appropriate icon from FontAwesome
5. Set display order
6. Save

### Managing Contact Form Submissions

1. Go to Contact → Contact Inquiries
2. Click on a submission to view details
3. Check "Is Read" after reviewing
4. Add admin notes if needed
5. Save

---

## Troubleshooting

### Images Not Displaying

**Problem:** Uploaded images don't show on website

**Solutions:**
1. Check file size (must be under limits)
2. Verify file format (JPG, PNG only)
3. Ensure "Is Active" is checked
4. Clear browser cache (Ctrl+Shift+R)
5. Check that media files exist in `/media/` directory

### Content Not Appearing

**Problem:** Published content doesn't show on website

**Checklist:**
- [ ] Status is set to "Published"
- [ ] "Is Active" is checked (where applicable)
- [ ] Published date is not in the future
- [ ] Correct category is selected
- [ ] Clear browser cache

### Slug Already Exists Error

**Problem:** "Slug already exists" error when saving

**Solution:**
1. Change the slug to something unique
2. Or edit/delete the conflicting item
3. Slugs must be unique within each content type

### Rich Text Editor Not Working

**Problem:** CKEditor doesn't load or format properly

**Solutions:**
1. Refresh the page (F5)
2. Clear browser cache
3. Try a different browser (Chrome recommended)
4. Check browser console for JavaScript errors

### Can't Upload Large Files

**Problem:** File upload fails for large images/documents

**Solutions:**
1. Compress images before uploading
2. Use online tools like TinyPNG or Squoosh
3. Reduce image dimensions if too large
4. Convert to JPG if using PNG for photos

---

## Best Practices

### Content Guidelines

1. **Be Concise:** Keep titles under 60 characters for better display
2. **Use Clear Language:** Write for general audience, avoid jargon
3. **Update Regularly:** Keep news and announcements current
4. **Check Links:** Verify all links work before publishing
5. **Proofread:** Check spelling and grammar before publishing

### Image Guidelines

1. **Optimize File Size:** Compress images before uploading
2. **Use Descriptive Names:** Name files clearly (e.g., `mce-official-photo.jpg`)
3. **Maintain Consistency:** Use similar styles across all images
4. **Check Mobile:** Verify images look good on small screens

### Security

1. **Strong Passwords:** Use complex passwords for admin accounts
2. **Logout After Use:** Always logout when done
3. **Limited Access:** Only give admin access to trusted staff
4. **Regular Backups:** Backup database regularly

---

## Getting Help

### Resources

- **Django Documentation:** https://docs.djangoproject.com/
- **CKEditor Guide:** https://ckeditor.com/docs/
- **FontAwesome Icons:** https://fontawesome.com/icons

### Support

For technical support or questions:
- Email: admin@amma.gov.gh
- Check the README.md file in project root
- Review Django admin logs for error messages

---

## Quick Reference

### Admin URLs

- **Admin Login:** http://127.0.0.1:8000/admin/
- **Site Homepage:** http://127.0.0.1:8000/
- **News List:** http://127.0.0.1:8000/news/
- **Projects List:** http://127.0.0.1:8000/projects/
- **Services:** http://127.0.0.1:8000/services/
- **Contact:** http://127.0.0.1:8000/contact/

### Keyboard Shortcuts (in admin)

- **Save:** Alt+S (Ctrl+S on Mac)
- **Save and Continue:** Alt+Shift+S
- **Delete:** Alt+D

### Common Icons (FontAwesome)

- `home` - House/Home
- `users` - People/Group
- `briefcase` - Work/Business
- `graduation-cap` - Education
- `hospital` - Healthcare
- `tint` - Water
- `file-alt` - Document
- `phone` - Telephone
- `envelope` - Email
- `map-marker-alt` - Location

---

**Last Updated:** 2025-10-14
**Version:** 1.0
