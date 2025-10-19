# Content Blocks Quick Reference

## Block Types Summary

| Block Type | Purpose | Key Features | Editor Support |
|------------|---------|--------------|----------------|
| **text** | Paragraphs & descriptions | Simple text with optional title, custom colors | ✅ Full |
| **service_grid** | Multiple service cards | Grid of cards with descriptions & bullet lists | ✅ Full |
| **list** | Bulleted lists | Checkmark icons, optional description | ✅ Full |
| **steps** | Process workflows | Numbered steps in grid layout | ✅ Full |
| **notice** | Alerts & important info | Colored border box with icon | ✅ Full |
| **table** | Tabular data | Headers, rows, colored header | ✅ Full |
| **document** | File downloads | Document cards with links | ⚠️ Partial |
| **image** | Images & photos | Image display with caption | ⚠️ Partial |

---

## Quick JSON Examples

### Text Block
```json
{
  "block_type": "text",
  "title": "Overview",
  "content": "Your text here...",
  "data": {"color": "#1a1a1a"},
  "order": 0
}
```

### List Block
```json
{
  "block_type": "list",
  "title": "Requirements",
  "content": "You need:",
  "data": {
    "color": "#d4af37",
    "items": ["Item 1", "Item 2", "Item 3"]
  },
  "order": 1
}
```

### Service Grid
```json
{
  "block_type": "service_grid",
  "title": "Services",
  "data": {
    "color": "#d4af37",
    "items": [
      {
        "title": "Service Name",
        "description": "Description...",
        "list": ["Feature 1", "Feature 2"]
      }
    ]
  },
  "order": 2
}
```

### Steps Block
```json
{
  "block_type": "steps",
  "title": "Process",
  "data": {
    "color": "#d4af37",
    "steps": [
      {
        "title": "Step 1",
        "description": "Do this...",
        "list": ["Requirement A", "Requirement B"]
      }
    ]
  },
  "order": 3
}
```

### Notice Block
```json
{
  "block_type": "notice",
  "title": "Important",
  "content": "Pay attention to this!",
  "data": {"color": "#ef4444"},
  "order": 4
}
```

### Table Block
```json
{
  "block_type": "table",
  "title": "Fees",
  "data": {
    "color": "#6c6c6c",
    "headers": ["Item", "Cost", "Time"],
    "rows": [
      ["Fee A", "50", "1 day"],
      ["Fee B", "100", "2 days"]
    ]
  },
  "order": 5
}
```

---

## Common Color Codes

| Color Name | Hex Code | Use Case |
|------------|----------|----------|
| Black/Default | `#1a1a1a` | Text content |
| AMMA Gold | `#d4af37` | Brand accent |
| Green | `#10b981` | Success, positive |
| Blue | `#3b82f6` | Information |
| Red | `#ef4444` | Warnings, alerts |
| Purple | `#8b5cf6` | Special features |
| Gray | `#6b7280` | Neutral info |

---

## Available Icons

- `file-text` - Document (default)
- `folder` - Folder
- `briefcase` - Business
- `users` - People
- `home` - Home/Housing
- `building` - Building/Construction
- `truck` - Transport/Delivery
- `clipboard` - Forms/Applications

---

## Pre-built Templates

| Template Key | Description |
|--------------|-------------|
| `outdoor_advertising` | Full outdoor advertising permit |
| `environmental_health` | Health services grid |
| `waste_management` | Waste management services |
| `3_step_process` | Simple 3-step workflow |
| `requirements_list` | Basic requirements list |
| `fees_table` | Standard fees table |

---

## JSON Editor Commands

| Action | Button | Description |
|--------|--------|-------------|
| Show/Hide | "Show"/"Hide" | Toggle JSON editor visibility |
| Format | "Format JSON" | Pretty-print the JSON |
| Apply | "Apply JSON Changes" | Import JSON to visual editor |

---

## Tips & Tricks

1. **Copy/Paste Services**: Export JSON from one service, paste into another
2. **Bulk Edit**: Use JSON editor to quickly change all colors or titles
3. **Templates**: Start with a template, customize with visual editor
4. **Auto-Sync**: Visual changes automatically update JSON (unless manually edited)
5. **Validation**: Always use "Format JSON" to check syntax before applying

---

## Common Patterns

### Basic Service Page
1. Text (Overview)
2. List (Requirements)
3. Steps (Process)
4. Table (Fees)

### Service Catalog Page
1. Text (Introduction)
2. Service Grid (Multiple services)
3. Notice (Important info)

### Complex Application Page
1. Text (Overview)
2. List (Requirements)
3. Service Grid (Subcategories)
4. Steps (Process)
5. Table (Fees)
6. Notice (Important notes)

---

## Keyboard Shortcuts in JSON Editor

- `Ctrl/Cmd + A` - Select all
- `Ctrl/Cmd + C` - Copy
- `Ctrl/Cmd + V` - Paste
- `Tab` - Indent (2 spaces)
- `Shift + Tab` - Unindent

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| JSON won't apply | Click "Format JSON" to see error message |
| Visual changes not showing | Click "Apply JSON Changes" after JSON edit |
| Lost changes | Visual editor changes auto-save on "Save Service" |
| Color not showing | Ensure format is `#rrggbb` (6-digit hex) |
| List items not appearing | Check that `data.items` is an array of strings |

---

## Full Service JSON Structure

```json
{
  "service": {
    "name": "string",
    "description": "string",
    "icon": "string",
    "has_detail_page": boolean,
    "is_active": boolean,
    "link_url": "string",
    "order": number
  },
  "blocks": [
    {
      "block_type": "text|service_grid|list|steps|notice|table|document|image",
      "title": "string (optional)",
      "content": "string",
      "data": {},
      "order": number
    }
  ]
}
```
