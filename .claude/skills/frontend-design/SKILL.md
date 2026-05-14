---
name: spendly-ui-designer
description: Generates modern, production-ready UI components and pages for Spendly — a personal expense tracker built with Python/Flask, SQLite, and Jinja2 templates. Use this skill whenever the user asks to design, create, build, redesign, or improve any UI element for Spendly. Triggers on phrases like "design the page", "create UI for", "build component for", "redesign", "improve the layout", or any Spendly frontend work. Always use this skill for Spendly UI tasks even if the request seems simple — consistency depends on it.
disable-model-invocation: true
---

# Spendly UI Designer

Spendly is a personal expense tracker with a Flask/SQLite backend and Jinja2-templated frontend. The stack:
- **Backend**: Python + Flask, SQLite (raw sqlite3), Werkzeug
- **Frontend**: Jinja2 templates, plain HTML/CSS, vanilla JS where needed
- **Icons**: Lucide via CDN (`https://unpkg.com/lucide@latest`)

---

## Step 0: Gather Context Before Designing

**Always do this first — do not skip.**

Before generating any UI, you need to know what already exists. Spendly's design consistency depends on this.

Ask the user for:
1. **A screenshot or description of existing pages** — especially the base layout, nav, and color palette. If they haven't provided one, ask: *"Can you share a screenshot of an existing Spendly page? I need to match the design."*
2. **What data this component/page will display** — column names, data types, empty states
3. **Any constraints** — mobile support needed? Specific Flask route? Form that POSTs somewhere?

If the user says they don't have screenshots and this is a new project/page, proceed with the Spendly Design System below as the baseline.

---

## Spendly Design System (Baseline)

Use these tokens when no existing design reference is available. If screenshots are provided, extract and match the actual values instead.

### Color Palette
```css
:root {
  --color-bg:           #F8F9FA;   /* Page background */
  --color-surface:      #FFFFFF;   /* Cards, modals */
  --color-border:       #E9ECEF;   /* Dividers, card borders */
  --color-text-primary: #1A1D23;   /* Headings, labels */
  --color-text-muted:   #6C757D;   /* Secondary text, placeholders */
  --color-accent:       #4F6EF7;   /* Primary actions, links */
  --color-accent-light: #EEF1FE;   /* Accent backgrounds, chips */
  --color-danger:       #E74C3C;   /* Expenses, deletions */
  --color-danger-light: #FDECEA;
  --color-success:      #27AE60;   /* Income, confirmations */
  --color-success-light:#E9F7EF;
  --color-warning:      #F39C12;
  --color-warning-light:#FEF9E7;
}
```

### Typography
```css
/* Load via <link> in base template */
/* font-family: 'Inter', sans-serif — via Google Fonts */

--font-size-xs:   11px;
--font-size-sm:   13px;
--font-size-base: 14px;
--font-size-md:   16px;
--font-size-lg:   20px;
--font-size-xl:   24px;
--font-size-2xl:  32px;

--font-weight-regular: 400;
--font-weight-medium:  500;
--font-weight-semibold: 600;
--font-weight-bold:    700;
```

### Spacing (8px grid)
```
4px   — tight padding inside chips/badges
8px   — small gaps, icon-to-label spacing
12px  — compact padding (table cells, form inputs)
16px  — standard card padding, list item padding
24px  — section spacing, card gaps
32px  — page section margins
48px  — major section breaks
```

### Component Tokens
```css
--radius-sm:   4px;
--radius-md:   8px;
--radius-lg:   12px;
--radius-xl:   16px;

--shadow-card: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
--shadow-hover: 0 4px 12px rgba(0,0,0,0.10);
--shadow-modal: 0 20px 60px rgba(0,0,0,0.15);

--transition: 150ms ease;
```

---

## Output Format

For every UI request, produce **three sections**:

### 1. Layout Brief (before code)
2–4 sentences max. State:
- What sections/components are on this page
- One key UX decision you made and why
- Any assumptions about data or Flask context variables

### 2. Code
Deliver as **one complete Jinja2 template** (`.html` file). Structure:

```html
{% extends "base.html" %}
{% block title %}Page Title{% endblock %}
{% block content %}

<!-- Page HTML here -->

{% endblock %}

{% block styles %}
<style>
  /* Page-scoped CSS here */
  /* Use CSS variables from design system */
  /* No inline styles */
</style>
{% endblock %}

{% block scripts %}
<script>
  // Vanilla JS only — no frameworks
  // Keep minimal; only if interactive behaviour needed
</script>
{% endblock %}
```

**Lucide icons** — load once in base template, use anywhere:
```html
<!-- In <head> of base.html -->
<script src="https://unpkg.com/lucide@latest"></script>

<!-- Usage (call lucide.createIcons() after DOM load) -->
<i data-lucide="trending-up"></i>
<script>lucide.createIcons();</script>
```

### 3. Design Notes
Bullet list of decisions worth flagging:
- Anything the user may want to change (color, label, layout variant)
- Empty state handling
- Mobile behaviour (if relevant)
- Flask variables assumed (e.g. `{{ expenses }}`, `{{ total }}`)

---

## Design Rules

**Do:**
- Card-based layout with `--shadow-card`
- Consistent 8px-grid spacing
- Rounded corners (`--radius-md` default, `--radius-lg` for cards)
- Color-coded amounts: expenses in `--color-danger`, income in `--color-success`
- Muted secondary text for dates, categories, metadata
- Hover states on interactive elements (`--shadow-hover`, subtle bg shift)
- Empty states with icon + message (never blank space)
- Use Lucide icons consistently for actions (trash, edit, plus, filter, etc.)

**Don't:**
- Inline styles (use CSS variables and classes)
- Bootstrap, Tailwind, or any CSS framework (plain CSS only)
- Random color choices outside the palette
- Tables for layouts (use CSS Grid or Flexbox)
- Dense, cluttered forms — group related fields, use spacing

---

## Spendly-Specific Patterns

### Expense Row (standard)
```html
<div class="expense-row">
  <div class="expense-icon">
    <i data-lucide="shopping-cart"></i>
  </div>
  <div class="expense-meta">
    <span class="expense-title">Groceries</span>
    <span class="expense-category">Food</span>
  </div>
  <div class="expense-date">May 12</div>
  <div class="expense-amount negative">-₹850</div>
  <div class="expense-actions">
    <button class="btn-icon"><i data-lucide="edit-2"></i></button>
    <button class="btn-icon danger"><i data-lucide="trash-2"></i></button>
  </div>
</div>
```

### Summary Card
```html
<div class="summary-card">
  <div class="summary-label">Total Spent</div>
  <div class="summary-value negative">₹12,450</div>
  <div class="summary-delta">↑ 8% vs last month</div>
</div>
```

### Category Badge
```html
<span class="badge badge--food">Food</span>
```

---

## When the Request is Ambiguous

If the user says something like "design the dashboard" without context:
1. Ask for a screenshot of any existing page (to match design)
2. Ask what data is available in the Flask route (template variables)
3. Don't guess and generate — a wrong structure wastes both rounds

If they say "just make something, I'll adjust" — proceed with design system defaults and flag all assumptions in Design Notes. 