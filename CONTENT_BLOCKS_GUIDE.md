# Service Content Blocks Guide

Complete reference for all content block types used in the AMMA CMS service pages.

## Overview

Content blocks are modular components that can be combined to create rich service detail pages. Each block has:
- **block_type**: The type of block (text, list, steps, etc.)
- **title**: Optional heading for the block
- **content**: Main text content (supports markdown/linebreaks)
- **data**: JSON object containing additional structured data
  - **color**: Customizable color for accent elements (default: `#1a1a1a` for text blocks, `#d4af37` for others)
- **order**: Display order (0-indexed)

---

## Block Types

### 1. Text Block
**Type:** `text`

Simple text content with optional title. Perfect for paragraphs, descriptions, and explanatory content.

**Structure:**
```json
{
  "block_type": "text",
  "title": "Overview",
  "content": "This service allows citizens to apply for building permits...",
  "data": {
    "color": "#1a1a1a"
  },
  "order": 0
}
```

**Fields:**
- `title` (optional): Heading displayed above the content
- `content`: The main text (supports line breaks)
- `data.color`: Text color (default: `#1a1a1a` - dark gray)

**Visual Output:**
- Large heading (if title provided)
- Formatted paragraph text with the specified color
- Responsive text formatting

---

### 2. Service Grid Block
**Type:** `service_grid`

Grid of service cards with titles, descriptions, and optional bullet points. Great for showcasing multiple related services or features.

**Structure:**
```json
{
  "block_type": "service_grid",
  "title": "Available Services",
  "content": "",
  "data": {
    "color": "#d4af37",
    "items": [
      {
        "title": "Food Handlers' Certificate",
        "description": "Medical screening for food handlers",
        "list": [
          "Process takes 2 weeks",
          "Only medically fit clients receive cards"
        ]
      },
      {
        "title": "Hospitality Premises",
        "description": "Inspection and monitoring services",
        "list": [
          "Standard enforcement",
          "Safety inspections",
          "Sanitation monitoring"
        ]
      }
    ]
  },
  "order": 1
}
```

**Fields:**
- `title` (optional): Section heading
- `data.items`: Array of service cards
  - `title`: Card heading
  - `description`: Card description
  - `list`: Array of bullet points (optional)
- `data.color`: Accent color for checkmarks (default: `#d4af37` - gold)

**Visual Output:**
- Responsive grid (1 column mobile, 2 tablet, 3 desktop)
- White cards with shadow effects
- Checkmark icons for list items
- Hover effects on cards

---

### 3. List Block
**Type:** `list`

Simple bulleted list with optional description. Perfect for requirements, features, or any enumerated content.

**Structure:**
```json
{
  "block_type": "list",
  "title": "Required Documents",
  "content": "Please submit the following documents with your application:",
  "data": {
    "color": "#d4af37",
    "items": [
      "Completed application form",
      "Valid identification",
      "Proof of address",
      "Payment receipt"
    ]
  },
  "order": 0
}
```

**Fields:**
- `title` (optional): Section heading
- `content` (optional): Description before the list
- `data.items`: Array of list items (strings)
- `data.color`: Color for checkmark icons and text (default: `#d4af37`)

**Visual Output:**
- Large heading
- Description paragraph (if provided)
- Bulleted list with circular checkmark icons
- Custom colored text and icons

---

### 4. Process Steps Block
**Type:** `steps`

Numbered process steps displayed in a grid. Ideal for application procedures, workflows, or sequential instructions.

**Structure:**
```json
{
  "block_type": "steps",
  "title": "Application Process",
  "content": "Follow these steps to complete your application:",
  "data": {
    "color": "#d4af37",
    "steps": [
      {
        "title": "Submission",
        "description": "Submit your application with required documents",
        "list": [
          "Complete application form",
          "Attach all documents"
        ]
      },
      {
        "title": "Processing",
        "description": "Application review takes 10 working days",
        "list": []
      },
      {
        "title": "Collection",
        "description": "Pay fees and collect your permit",
        "list": []
      }
    ]
  },
  "order": 2
}
```

**Fields:**
- `title` (optional): Section heading
- `content` (optional): Introduction text
- `data.steps`: Array of step objects
  - `title`: Step name
  - `description`: Step details
  - `list`: Optional requirements/notes for this step
- `data.color`: Color for step numbers and checkmarks (default: `#d4af37`)

**Visual Output:**
- Responsive grid (1 column mobile, 2 tablet, 3 desktop)
- Each step has a colored circular number badge
- White cards with shadow effects
- Optional bullet points within each step

---

### 5. Notice/Alert Block
**Type:** `notice`

Highlighted notice box with colored border. Perfect for important information, warnings, or special notes.

**Structure:**
```json
{
  "block_type": "notice",
  "title": "Important Note",
  "content": "All fees shall be determined based on the Assembly's Fee-Fixing Resolution.",
  "data": {
    "color": "#d4af37"
  },
  "order": 3
}
```

**Fields:**
- `title` (optional): Notice heading with info icon
- `content`: Notice message
- `data.color`: Border and background tint color (default: `#d4af37`)

**Visual Output:**
- Bordered box with left accent stripe
- Colored background (20% opacity of accent color)
- Info icon next to title (if provided)
- Rounded corners

**Color Suggestions:**
- Gold (`#d4af37`): General information
- Blue (`#3b82f6`): Informational
- Red (`#ef4444`): Warnings/Alerts
- Green (`#10b981`): Success/Tips

---

### 6. Table Block
**Type:** `table`

Data table with headers and rows. Perfect for fees, schedules, specifications, or any tabular data.

**Structure:**
```json
{
  "block_type": "table",
  "title": "Fees and Charges",
  "content": "",
  "data": {
    "color": "#6c6c6c",
    "headers": ["Service", "Fee (GHS)", "Processing Time"],
    "rows": [
      ["Application Fee", "50.00", "1-2 days"],
      ["Permit Fee", "200.00", "5-7 days"],
      ["Annual Renewal", "100.00", "3-5 days"]
    ]
  },
  "order": 0
}
```

**Fields:**
- `title` (optional): Table heading
- `data.headers`: Array of column headers
- `data.rows`: Array of arrays (each inner array is a row)
- `data.color`: Header background color (default: `#6c6c6c`)

**Visual Output:**
- Responsive table with horizontal scroll on mobile
- Colored header row
- Hover effects on data rows
- Clean borders and spacing

---

### 7. Document/Download Block
**Type:** `document`

⚠️ **Note:** Currently defined in models but not fully implemented in the visual editor.

Grid of downloadable documents with links. Useful for forms, PDFs, and attachments.

**Structure:**
```json
{
  "block_type": "document",
  "title": "Required Forms",
  "content": "",
  "data": {
    "documents": [
      {
        "title": "Application Form",
        "description": "Main application form (PDF)",
        "url": "/media/forms/application.pdf"
      },
      {
        "title": "Terms and Conditions",
        "description": "Please read before applying",
        "url": "/media/forms/terms.pdf"
      }
    ]
  },
  "order": 0
}
```

**Fields:**
- `title` (optional): Section heading
- `data.documents`: Array of document objects
  - `title`: Document name
  - `description`: Brief description
  - `url`: Download link

**Visual Output:**
- Grid of clickable document cards
- File icon with gold accent
- Hover effects
- Opens in new tab

---

### 8. Image Block
**Type:** `image`

⚠️ **Note:** Currently defined in models but not fully implemented in the visual editor.

Display images with optional captions.

**Structure:**
```json
{
  "block_type": "image",
  "title": "Office Location",
  "content": "",
  "data": {
    "url": "/media/images/office.jpg",
    "alt": "Office building exterior",
    "caption": "Visit us at our main office"
  },
  "order": 0
}
```

**Fields:**
- `title` (optional): Image heading
- `data.url`: Image file path
- `data.alt`: Alt text for accessibility
- `data.caption`: Optional caption below image

**Visual Output:**
- Full-width responsive image
- Rounded corners with shadow
- Optional caption in italics

---

## Color Customization

All blocks support custom colors via the `data.color` field. Colors are used for:

- **Text Block**: Main text color
- **Service Grid**: Checkmark icons
- **List Block**: Checkmark icons and list item text
- **Steps Block**: Step number badges and checkmarks
- **Notice Block**: Border and background tint
- **Table Block**: Header background

**Preset Colors:**
- `#1a1a1a` - Default/Black (for text)
- `#d4af37` - AMMA Gold (brand color)
- `#10b981` - Green (success/positive)
- `#3b82f6` - Blue (information)
- `#ef4444` - Red (warnings/alerts)
- `#8b5cf6` - Purple
- `#6b7280` - Gray

You can also use any custom hex color code.

---

## Pre-built Templates

The system includes several pre-built templates you can load when creating services:

### 1. **Outdoor Advertising Permit (Full)**
Complete template with text, list, steps, and notice blocks.

### 2. **Environmental Health Services**
Service grid template showcasing multiple health services.

### 3. **Waste Management Services**
Comprehensive template with service grid and notice blocks.

### 4. **3-Step Process**
Simple 3-step process template.

### 5. **Requirements List**
Basic bulleted list of requirements.

### 6. **Fees Table**
Standard fees and charges table.

---

## JSON Editor Usage

The JSON editor allows you to edit the entire service configuration at once:

```json
{
  "service": {
    "name": "Building Permit Application",
    "description": "Apply for building permits and approvals",
    "icon": "building",
    "has_detail_page": true,
    "is_active": true,
    "link_url": "",
    "order": 0
  },
  "blocks": [
    {
      "block_type": "text",
      "title": "Overview",
      "content": "Apply for various building permits...",
      "data": {
        "color": "#1a1a1a"
      },
      "order": 0
    },
    {
      "block_type": "list",
      "title": "Required Documents",
      "content": "Submit the following:",
      "data": {
        "color": "#d4af37",
        "items": [
          "Completed form",
          "Site plan",
          "Architectural drawings"
        ]
      },
      "order": 1
    }
  ]
}
```

**Tips:**
- Use the "Format JSON" button to clean up formatting
- JSON automatically syncs with visual editor
- Click "Apply JSON Changes" to import edits
- JSON validates before import

---

## Best Practices

1. **Use Meaningful Titles**: Help users navigate content quickly
2. **Keep Content Concise**: Break long content into multiple blocks
3. **Choose Appropriate Colors**: Use colors consistently (gold for general, red for warnings, etc.)
4. **Order Logically**: Arrange blocks in a logical flow (overview → requirements → process → fees)
5. **Combine Block Types**: Mix different blocks for rich, engaging pages
6. **Test Responsiveness**: Preview on different screen sizes

---

## Example: Complete Service Page

```json
{
  "service": {
    "name": "Business Operating Permit",
    "description": "Apply for a license to operate your business",
    "icon": "briefcase",
    "has_detail_page": true,
    "is_active": true,
    "link_url": "",
    "order": 1
  },
  "blocks": [
    {
      "block_type": "text",
      "title": "Overview",
      "content": "All businesses must obtain a Business Operating Permit (BOP) before commencing operations.",
      "data": {"color": "#1a1a1a"},
      "order": 0
    },
    {
      "block_type": "list",
      "title": "Required Documents",
      "content": "Prepare the following documents:",
      "data": {
        "color": "#d4af37",
        "items": [
          "Completed application form",
          "Certificate of incorporation",
          "Tax Identification Number (TIN)",
          "Proof of premises"
        ]
      },
      "order": 1
    },
    {
      "block_type": "steps",
      "title": "Application Process",
      "content": "",
      "data": {
        "color": "#d4af37",
        "steps": [
          {
            "title": "Submit",
            "description": "Submit application with documents",
            "list": []
          },
          {
            "title": "Inspection",
            "description": "Site inspection within 5 days",
            "list": []
          },
          {
            "title": "Approval",
            "description": "Receive permit within 10 days",
            "list": []
          }
        ]
      },
      "order": 2
    },
    {
      "block_type": "table",
      "title": "Fees",
      "content": "",
      "data": {
        "color": "#6c6c6c",
        "headers": ["Category", "Annual Fee (GHS)"],
        "rows": [
          ["Small Business", "500"],
          ["Medium Business", "1,500"],
          ["Large Business", "3,000"]
        ]
      },
      "order": 3
    },
    {
      "block_type": "notice",
      "title": "Important",
      "content": "Operating without a valid permit is punishable by law.",
      "data": {"color": "#ef4444"},
      "order": 4
    }
  ]
}
```

---

## Visual Editor vs JSON Editor

**Visual Editor:**
- ✅ Beginner-friendly
- ✅ Real-time preview
- ✅ No syntax errors
- ✅ Drag-and-drop reordering

**JSON Editor:**
- ✅ Faster for experienced users
- ✅ Copy/paste entire configurations
- ✅ Bulk editing
- ✅ Easier to duplicate blocks

**Best Approach:** Use both! Build visually, then fine-tune with JSON.

---

## Need Help?

- **File Location:** `/home/mufti/dev/amma_cms/apps/services/models.py` (Block definitions)
- **Templates:** `/home/mufti/dev/amma_cms/apps/staff_portal/block_templates.py`
- **Editor:** `/home/mufti/dev/amma_cms/templates/staff_portal/services/edit.html`
- **Frontend Display:** `/home/mufti/dev/amma_cms/templates/services/detail.html`
