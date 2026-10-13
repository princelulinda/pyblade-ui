# Composants

Page générée par `scripts/gen_docs.py` depuis `registry.json` : ne pas éditer à la main.

## Button

Displays a button, in six variants and four sizes.

```bash
pyblade-ui add button
```

Fichiers : `components/ui/button.html`

```html
<pb-ui.button variant="outline" size="sm">Save</pb-ui.button>
```

## Button link

A link styled as a button.

```bash
pyblade-ui add button-link
```

Fichiers : `components/ui/button_link.html`

```html
<pb-ui.button-link href="/docs" variant="secondary">Docs</pb-ui.button-link>
```

## Badge

A small status label.

```bash
pyblade-ui add badge
```

Fichiers : `components/ui/badge.html`

```html
<pb-ui.badge variant="success">Paid</pb-ui.badge>
```

## Card

A container with header, title, description, action, content and footer.

```bash
pyblade-ui add card
```

Fichiers : `components/ui/card.html`, `components/ui/card_header.html`, `components/ui/card_title.html`, `components/ui/card_description.html`, `components/ui/card_action.html`, `components/ui/card_content.html`, `components/ui/card_footer.html`

```html
<pb-ui.card>
  <pb-ui.card-header><pb-ui.card-title>Title</pb-ui.card-title></pb-ui.card-header>
  <pb-ui.card-content>Body</pb-ui.card-content>
</pb-ui.card>
```

## Alert

A callout for important messages.

```bash
pyblade-ui add alert
```

Fichiers : `components/ui/alert.html`, `components/ui/alert_title.html`, `components/ui/alert_description.html`

```html
<pb-ui.alert variant="destructive">
  <pb-ui.alert-title>Error</pb-ui.alert-title>
  <pb-ui.alert-description>Your session has expired.</pb-ui.alert-description>
</pb-ui.alert>
```

## Avatar

An image with a fallback for the user.

```bash
pyblade-ui add avatar
```

Fichiers : `components/ui/avatar.html`

```html
<pb-ui.avatar :src="user.photo_url" fallback="JD" />
```

## Input

A text field.

```bash
pyblade-ui add input
```

Fichiers : `components/ui/input.html`

```html
<pb-ui.input name="email" type="email" placeholder="Email" />
```

## Textarea

A multi-line text field that grows with its content.

```bash
pyblade-ui add textarea
```

Fichiers : `components/ui/textarea.html`

```html
<pb-ui.textarea name="bio" rows="4"></pb-ui.textarea>
```

## Label

A label for a form control.

```bash
pyblade-ui add label
```

Fichiers : `components/ui/label.html`

```html
<pb-ui.label for="email">Email</pb-ui.label>
```

## Select

A native select, styled.

```bash
pyblade-ui add select
```

Fichiers : `components/ui/select.html`

```html
<pb-ui.select name="role">
  <option value="admin">Admin</option>
</pb-ui.select>
```

## Checkbox

A native checkbox, styled.

```bash
pyblade-ui add checkbox
```

Fichiers : `components/ui/checkbox.html`

```html
<pb-ui.checkbox id="terms" name="terms" />
```

## Switch

A toggle between on and off, on a native checkbox.

```bash
pyblade-ui add switch
```

Fichiers : `components/ui/switch.html`

```html
<pb-ui.switch name="notifications" checked />
```

## Separator

A horizontal or vertical divider.

```bash
pyblade-ui add separator
```

Fichiers : `components/ui/separator.html`

```html
<pb-ui.separator orientation="vertical" />
```

## Skeleton

A placeholder while content loads.

```bash
pyblade-ui add skeleton
```

Fichiers : `components/ui/skeleton.html`

```html
<pb-ui.skeleton class="h-4 w-48" />
```

## Progress

A progress bar from 0 to 100.

```bash
pyblade-ui add progress
```

Fichiers : `components/ui/progress.html`

```html
<pb-ui.progress :value="66" />
```

## Table

A responsive table and its parts.

```bash
pyblade-ui add table
```

Fichiers : `components/ui/table.html`, `components/ui/table_header.html`, `components/ui/table_body.html`, `components/ui/table_row.html`, `components/ui/table_head.html`, `components/ui/table_cell.html`, `components/ui/table_caption.html`

```html
<pb-ui.table>
  <pb-ui.table-header><pb-ui.table-row><pb-ui.table-head>Name</pb-ui.table-head></pb-ui.table-row></pb-ui.table-header>
  <pb-ui.table-body>
    @for(user in users)
    <pb-ui.table-row><pb-ui.table-cell>{{ user.name }}</pb-ui.table-cell></pb-ui.table-row>
    @endfor
  </pb-ui.table-body>
</pb-ui.table>
```

## Tabs

Panels shown one at a time.

```bash
pyblade-ui add tabs
```

Nécessite : alpinejs.

Fichiers : `components/ui/tabs.html`, `components/ui/tabs_list.html`, `components/ui/tabs_trigger.html`, `components/ui/tabs_content.html`

```html
<pb-ui.tabs value="account">
  <pb-ui.tabs-list>
    <pb-ui.tabs-trigger value="account">Account</pb-ui.tabs-trigger>
    <pb-ui.tabs-trigger value="password">Password</pb-ui.tabs-trigger>
  </pb-ui.tabs-list>
  <pb-ui.tabs-content value="account">...</pb-ui.tabs-content>
  <pb-ui.tabs-content value="password">...</pb-ui.tabs-content>
</pb-ui.tabs>
```

## Accordion

Sections that expand one at a time.

```bash
pyblade-ui add accordion
```

Nécessite : alpinejs.

Fichiers : `components/ui/accordion.html`, `components/ui/accordion_item.html`

```html
<pb-ui.accordion value="q1">
  <pb-ui.accordion-item value="q1" title="Is it accessible?">Yes.</pb-ui.accordion-item>
</pb-ui.accordion>
```

## Dialog

A modal window, opened by its trigger or by name.

```bash
pyblade-ui add dialog
```

Installe aussi : `button`.

Nécessite : alpinejs.

Fichiers : `components/ui/dialog.html`, `components/ui/dialog_header.html`, `components/ui/dialog_title.html`, `components/ui/dialog_description.html`, `components/ui/dialog_footer.html`, `components/ui/dialog_close.html`

```html
<pb-ui.dialog name="delete">
  <pb-slot:trigger><pb-ui.button variant="destructive">Delete</pb-ui.button></pb-slot:trigger>
  <pb-ui.dialog-header>
    <pb-ui.dialog-title>Are you sure?</pb-ui.dialog-title>
    <pb-ui.dialog-description>This cannot be undone.</pb-ui.dialog-description>
  </pb-ui.dialog-header>
  <pb-ui.dialog-footer>
    <pb-ui.dialog-close><pb-ui.button variant="outline">Cancel</pb-ui.button></pb-ui.dialog-close>
  </pb-ui.dialog-footer>
</pb-ui.dialog>
{# Or from anywhere: $dispatch('dialog-open', 'delete') #}
```

## Dropdown menu

A menu opened by a trigger.

```bash
pyblade-ui add dropdown-menu
```

Installe aussi : `button`.

Nécessite : alpinejs.

Fichiers : `components/ui/dropdown_menu.html`, `components/ui/dropdown_menu_item.html`, `components/ui/dropdown_menu_label.html`, `components/ui/dropdown_menu_separator.html`

```html
<pb-ui.dropdown-menu align="end">
  <pb-slot:trigger><pb-ui.button variant="outline">Open</pb-ui.button></pb-slot:trigger>
  <pb-ui.dropdown-menu-label>My account</pb-ui.dropdown-menu-label>
  <pb-ui.dropdown-menu-separator />
  <pb-ui.dropdown-menu-item href="/profile">Profile</pb-ui.dropdown-menu-item>
  <pb-ui.dropdown-menu-item variant="destructive">Log out</pb-ui.dropdown-menu-item>
</pb-ui.dropdown-menu>
```

## Tooltip

A hint shown on hover and focus, in CSS only.

```bash
pyblade-ui add tooltip
```

Fichiers : `components/ui/tooltip.html`

```html
<pb-ui.tooltip text="Add to library"><pb-ui.button variant="outline">Hover</pb-ui.button></pb-ui.tooltip>
```

## Toaster

Toast notifications, raised from JavaScript with toast({...}).

```bash
pyblade-ui add toaster
```

Nécessite : alpinejs.

Fichiers : `components/ui/toaster.html`

```html
<pb-ui.toaster position="bottom-right" />
<pb-ui.button x-on:click="toast({ title: 'Saved', variant: 'success' })">Save</pb-ui.button>
```

## Theme script

Applies the saved light or dark mode before the page paints. Goes in <head>.

```bash
pyblade-ui add theme-script
```

Fichiers : `components/ui/theme_script.html`

```html
<pb-ui.theme-script />
```

## Mode toggle

Switches between light and dark mode.

```bash
pyblade-ui add mode-toggle
```

Installe aussi : `theme-script`.

Nécessite : alpinejs.

Fichiers : `components/ui/mode_toggle.html`

```html
<pb-ui.mode-toggle />
```

## Radio group

A set of options where only one can be chosen, on native radios.

```bash
pyblade-ui add radio-group
```

Fichiers : `components/ui/radio_group.html`, `components/ui/radio_group_item.html`

```html
<pb-ui.radio-group>
  <label class="flex items-center gap-3"><pb-ui.radio-group-item name="plan" value="free" checked /> Free</label>
  <label class="flex items-center gap-3"><pb-ui.radio-group-item name="plan" value="pro" /> Pro</label>
</pb-ui.radio-group>
```

## Slider

A range input, styled, with its filled track.

```bash
pyblade-ui add slider
```

Nécessite : alpinejs.

Fichiers : `components/ui/slider.html`

```html
<pb-ui.slider name="volume" min="0" max="100" value="50" />
```

## Toggle

A two-state button that can be on or off.

```bash
pyblade-ui add toggle
```

Nécessite : alpinejs.

Fichiers : `components/ui/toggle.html`

```html
<pb-ui.toggle variant="outline" aria-label="Bold">B</pb-ui.toggle>
```

## Toggle group

A set of toggles, single or multiple choice.

```bash
pyblade-ui add toggle-group
```

Nécessite : alpinejs.

Fichiers : `components/ui/toggle_group.html`, `components/ui/toggle_group_item.html`

```html
<pb-ui.toggle-group type="single" value="center">
  <pb-ui.toggle-group-item value="left">Left</pb-ui.toggle-group-item>
  <pb-ui.toggle-group-item value="center">Center</pb-ui.toggle-group-item>
  <pb-ui.toggle-group-item value="right">Right</pb-ui.toggle-group-item>
</pb-ui.toggle-group>
```

## Kbd

A keyboard key or shortcut.

```bash
pyblade-ui add kbd
```

Fichiers : `components/ui/kbd.html`, `components/ui/kbd_group.html`

```html
<pb-ui.kbd-group><pb-ui.kbd>Ctrl</pb-ui.kbd><pb-ui.kbd>K</pb-ui.kbd></pb-ui.kbd-group>
```

## Spinner

A loading indicator.

```bash
pyblade-ui add spinner
```

Fichiers : `components/ui/spinner.html`

```html
<pb-ui.spinner class="size-6" />
```

## Aspect ratio

Keeps its content at a given ratio.

```bash
pyblade-ui add aspect-ratio
```

Fichiers : `components/ui/aspect_ratio.html`

```html
<pb-ui.aspect-ratio ratio="16 / 9" class="rounded-lg bg-muted">
  <img src="/photo.jpg" alt="" class="size-full object-cover" />
</pb-ui.aspect-ratio>
```

## Scroll area

A scrollable region with a thin, themed scrollbar.

```bash
pyblade-ui add scroll-area
```

Fichiers : `components/ui/scroll_area.html`

```html
<pb-ui.scroll-area class="h-72 w-48 rounded-md border">...</pb-ui.scroll-area>
```

## Button group

Joins buttons into one control.

```bash
pyblade-ui add button-group
```

Installe aussi : `button`.

Fichiers : `components/ui/button_group.html`

```html
<pb-ui.button-group>
  <pb-ui.button variant="outline">Archive</pb-ui.button>
  <pb-ui.button variant="outline">Report</pb-ui.button>
</pb-ui.button-group>
```

## Breadcrumb

The path to the current page.

```bash
pyblade-ui add breadcrumb
```

Fichiers : `components/ui/breadcrumb.html`, `components/ui/breadcrumb_list.html`, `components/ui/breadcrumb_item.html`, `components/ui/breadcrumb_link.html`, `components/ui/breadcrumb_page.html`, `components/ui/breadcrumb_separator.html`, `components/ui/breadcrumb_ellipsis.html`

```html
<pb-ui.breadcrumb>
  <pb-ui.breadcrumb-list>
    <pb-ui.breadcrumb-item><pb-ui.breadcrumb-link href="/">Home</pb-ui.breadcrumb-link></pb-ui.breadcrumb-item>
    <pb-ui.breadcrumb-separator />
    <pb-ui.breadcrumb-item><pb-ui.breadcrumb-page>Settings</pb-ui.breadcrumb-page></pb-ui.breadcrumb-item>
  </pb-ui.breadcrumb-list>
</pb-ui.breadcrumb>
```

## Pagination

Links to the pages of a list.

```bash
pyblade-ui add pagination
```

Fichiers : `components/ui/pagination.html`, `components/ui/pagination_content.html`, `components/ui/pagination_item.html`, `components/ui/pagination_link.html`, `components/ui/pagination_previous.html`, `components/ui/pagination_next.html`, `components/ui/pagination_ellipsis.html`

```html
<pb-ui.pagination>
  <pb-ui.pagination-content>
    <pb-ui.pagination-item><pb-ui.pagination-previous href="?page=1" /></pb-ui.pagination-item>
    <pb-ui.pagination-item><pb-ui.pagination-link href="?page=1">1</pb-ui.pagination-link></pb-ui.pagination-item>
    <pb-ui.pagination-item><pb-ui.pagination-link href="?page=2" active>2</pb-ui.pagination-link></pb-ui.pagination-item>
    <pb-ui.pagination-item><pb-ui.pagination-ellipsis /></pb-ui.pagination-item>
    <pb-ui.pagination-item><pb-ui.pagination-next href="?page=3" /></pb-ui.pagination-item>
  </pb-ui.pagination-content>
</pb-ui.pagination>
```

## Empty

An empty state, with media, title, description and actions.

```bash
pyblade-ui add empty
```

Fichiers : `components/ui/empty.html`, `components/ui/empty_header.html`, `components/ui/empty_media.html`, `components/ui/empty_title.html`, `components/ui/empty_description.html`, `components/ui/empty_content.html`

```html
<pb-ui.empty class="border">
  <pb-ui.empty-header>
    <pb-ui.empty-title>No projects yet</pb-ui.empty-title>
    <pb-ui.empty-description>Create your first project to get started.</pb-ui.empty-description>
  </pb-ui.empty-header>
  <pb-ui.empty-content><pb-ui.button>Create project</pb-ui.button></pb-ui.empty-content>
</pb-ui.empty>
```

## Field

A form field: label, control, description and error, wired to @error.

```bash
pyblade-ui add field
```

Installe aussi : `input`.

Fichiers : `components/ui/field.html`, `components/ui/field_label.html`, `components/ui/field_description.html`, `components/ui/field_error.html`

```html
<pb-ui.field :errors="form.errors" name="email">
  <pb-ui.field-label for="email">Email</pb-ui.field-label>
  <pb-ui.input id="email" name="email" type="email" />
  <pb-ui.field-description>We never share it.</pb-ui.field-description>
  <pb-ui.field-error :errors="form.errors" name="email" />
</pb-ui.field>
```

## Alert dialog

A modal that asks for confirmation and cannot be dismissed by clicking outside.

```bash
pyblade-ui add alert-dialog
```

Installe aussi : `button`.

Nécessite : alpinejs.

Fichiers : `components/ui/alert_dialog.html`, `components/ui/alert_dialog_header.html`, `components/ui/alert_dialog_footer.html`, `components/ui/alert_dialog_title.html`, `components/ui/alert_dialog_description.html`, `components/ui/alert_dialog_action.html`, `components/ui/alert_dialog_cancel.html`

```html
<pb-ui.alert-dialog name="delete">
  <pb-slot:trigger><pb-ui.button variant="outline">Delete</pb-ui.button></pb-slot:trigger>
  <pb-ui.alert-dialog-header>
    <pb-ui.alert-dialog-title>Are you absolutely sure?</pb-ui.alert-dialog-title>
    <pb-ui.alert-dialog-description>This cannot be undone.</pb-ui.alert-dialog-description>
  </pb-ui.alert-dialog-header>
  <pb-ui.alert-dialog-footer>
    <pb-ui.alert-dialog-cancel><pb-ui.button variant="outline">Cancel</pb-ui.button></pb-ui.alert-dialog-cancel>
    <pb-ui.alert-dialog-action><pb-ui.button>Continue</pb-ui.button></pb-ui.alert-dialog-action>
  </pb-ui.alert-dialog-footer>
</pb-ui.alert-dialog>
```

## Sheet

A panel that slides in from an edge of the screen.

```bash
pyblade-ui add sheet
```

Installe aussi : `button`.

Nécessite : alpinejs.

Fichiers : `components/ui/sheet.html`, `components/ui/sheet_header.html`, `components/ui/sheet_footer.html`, `components/ui/sheet_title.html`, `components/ui/sheet_description.html`, `components/ui/sheet_close.html`

```html
<pb-ui.sheet side="right">
  <pb-slot:trigger><pb-ui.button variant="outline">Open</pb-ui.button></pb-slot:trigger>
  <pb-ui.sheet-header>
    <pb-ui.sheet-title>Edit profile</pb-ui.sheet-title>
    <pb-ui.sheet-description>Save when you are done.</pb-ui.sheet-description>
  </pb-ui.sheet-header>
  <pb-ui.sheet-footer>
    <pb-ui.sheet-close><pb-ui.button variant="outline">Close</pb-ui.button></pb-ui.sheet-close>
  </pb-ui.sheet-footer>
</pb-ui.sheet>
{# Or from anywhere: $dispatch('sheet-open', 'name') #}
```

## Popover

Rich content in a floating panel, opened by its trigger.

```bash
pyblade-ui add popover
```

Installe aussi : `button`.

Nécessite : alpinejs.

Fichiers : `components/ui/popover.html`

```html
<pb-ui.popover align="start">
  <pb-slot:trigger><pb-ui.button variant="outline">Open</pb-ui.button></pb-slot:trigger>
  <p class="text-sm">Place any content here.</p>
</pb-ui.popover>
```

## Hover card

A preview card shown on hover and focus, in CSS only.

```bash
pyblade-ui add hover-card
```

Fichiers : `components/ui/hover_card.html`

```html
<pb-ui.hover-card>
  <pb-slot:trigger><a href="/u/ada" class="underline">@ada</a></pb-slot:trigger>
  <p class="text-sm">Ada Lovelace, first programmer.</p>
</pb-ui.hover-card>
```

## Collapsible

A section that shows and hides its content.

```bash
pyblade-ui add collapsible
```

Installe aussi : `button`.

Nécessite : alpinejs.

Fichiers : `components/ui/collapsible.html`, `components/ui/collapsible_trigger.html`, `components/ui/collapsible_content.html`

```html
<pb-ui.collapsible>
  <pb-ui.collapsible-trigger><pb-ui.button variant="ghost">Toggle</pb-ui.button></pb-ui.collapsible-trigger>
  <pb-ui.collapsible-content>Hidden content</pb-ui.collapsible-content>
</pb-ui.collapsible>
```

## Context menu

A menu opened with a right click on its area.

```bash
pyblade-ui add context-menu
```

Installe aussi : `dropdown-menu`.

Nécessite : alpinejs.

Fichiers : `components/ui/context_menu.html`

```html
<pb-ui.context-menu>
  <pb-slot:trigger><div class="grid h-36 place-items-center rounded-md border border-dashed">Right click here</div></pb-slot:trigger>
  <pb-ui.dropdown-menu-item>Back</pb-ui.dropdown-menu-item>
  <pb-ui.dropdown-menu-item>Reload</pb-ui.dropdown-menu-item>
</pb-ui.context-menu>
```

## Command

A searchable list of commands, with keyboard navigation.

```bash
pyblade-ui add command
```

Nécessite : alpinejs.

Fichiers : `components/ui/command.html`, `components/ui/command_input.html`, `components/ui/command_list.html`, `components/ui/command_empty.html`, `components/ui/command_group.html`, `components/ui/command_item.html`, `components/ui/command_separator.html`, `components/ui/command_shortcut.html`

```html
<pb-ui.command class="rounded-lg border shadow-md">
  <pb-ui.command-input placeholder="Type a command or search..." />
  <pb-ui.command-list>
    <pb-ui.command-empty>No results found.</pb-ui.command-empty>
    <pb-ui.command-group heading="Suggestions">
      <pb-ui.command-item href="/calendar">Calendar</pb-ui.command-item>
      <pb-ui.command-item>Search emoji</pb-ui.command-item>
    </pb-ui.command-group>
  </pb-ui.command-list>
</pb-ui.command>
```

## Carousel

Slides you scroll through, with buttons, swipe and arrow keys.

```bash
pyblade-ui add carousel
```

Nécessite : alpinejs.

Fichiers : `components/ui/carousel.html`, `components/ui/carousel_content.html`, `components/ui/carousel_item.html`, `components/ui/carousel_previous.html`, `components/ui/carousel_next.html`

```html
<pb-ui.carousel class="w-full max-w-xs">
  <pb-ui.carousel-content>
    <pb-ui.carousel-item>Slide 1</pb-ui.carousel-item>
    <pb-ui.carousel-item>Slide 2</pb-ui.carousel-item>
  </pb-ui.carousel-content>
  <pb-ui.carousel-previous />
  <pb-ui.carousel-next />
</pb-ui.carousel>
```

## Input OTP

A one-time code input, one box per character, with paste support.

```bash
pyblade-ui add input-otp
```

Nécessite : alpinejs.

Fichiers : `components/ui/input_otp.html`

```html
<pb-ui.input-otp name="code" :length="6" />
```

## Sidebar

A collapsible app sidebar: offcanvas or icon mode, a sheet on mobile, Ctrl/⌘+B, and its state kept in a cookie read on the server.

```bash
pyblade-ui add sidebar
```

Nécessite : alpinejs.

Fichiers : `components/ui/sidebar_provider.html`, `components/ui/sidebar.html`, `components/ui/sidebar_trigger.html`, `components/ui/sidebar_rail.html`, `components/ui/sidebar_inset.html`, `components/ui/sidebar_header.html`, `components/ui/sidebar_footer.html`, `components/ui/sidebar_separator.html`, `components/ui/sidebar_content.html`, `components/ui/sidebar_input.html`, `components/ui/sidebar_group.html`, `components/ui/sidebar_group_label.html`, `components/ui/sidebar_group_action.html`, `components/ui/sidebar_group_content.html`, `components/ui/sidebar_menu.html`, `components/ui/sidebar_menu_item.html`, `components/ui/sidebar_menu_button.html`, `components/ui/sidebar_menu_action.html`, `components/ui/sidebar_menu_badge.html`, `components/ui/sidebar_menu_skeleton.html`, `components/ui/sidebar_menu_sub.html`, `components/ui/sidebar_menu_sub_item.html`, `components/ui/sidebar_menu_sub_button.html`

```html
<pb-ui.sidebar-provider :open="sidebar_open" collapsible="icon">
  <pb-ui.sidebar>
    <pb-ui.sidebar-content>
      <pb-ui.sidebar-group>
        <pb-ui.sidebar-group-label>Application</pb-ui.sidebar-group-label>
        <pb-ui.sidebar-menu>
          <pb-ui.sidebar-menu-item>
            <pb-ui.sidebar-menu-button href="/" active tooltip="Home"><span>Home</span></pb-ui.sidebar-menu-button>
          </pb-ui.sidebar-menu-item>
        </pb-ui.sidebar-menu>
      </pb-ui.sidebar-group>
    </pb-ui.sidebar-content>
    <pb-ui.sidebar-rail />
  </pb-ui.sidebar>
  <pb-ui.sidebar-inset>
    <header class="flex h-14 items-center gap-2 border-b px-4"><pb-ui.sidebar-trigger /></header>
    <main class="p-4">...</main>
  </pb-ui.sidebar-inset>
</pb-ui.sidebar-provider>
{# sidebar_open comes from the cookie: pyblade_ui.sidebar_open(request), or the Django context processor #}
```

## Combobox

A select you can search, with keyboard navigation; its value is posted with the form.

```bash
pyblade-ui add combobox
```

Nécessite : alpinejs.

Fichiers : `components/ui/combobox.html`, `components/ui/combobox_item.html`

```html
<pb-ui.combobox name="framework" placeholder="Select a framework..." class="w-56">
  <pb-ui.combobox-item value="django">Django</pb-ui.combobox-item>
  <pb-ui.combobox-item value="flask">Flask</pb-ui.combobox-item>
  <pb-ui.combobox-item value="fastapi">FastAPI</pb-ui.combobox-item>
</pb-ui.combobox>
```

## Calendar

A month grid to pick a date, localized, with min and max and arrow-key navigation.

```bash
pyblade-ui add calendar
```

Nécessite : alpinejs.

Fichiers : `components/ui/calendar.html`

```html
<pb-ui.calendar name="day" value="2026-10-13" locale="fr-FR" :week_start="1" class="rounded-md border" />
```

## Date picker

A button that opens a calendar; the chosen date is posted as YYYY-MM-DD.

```bash
pyblade-ui add date-picker
```

Installe aussi : `calendar`.

Nécessite : alpinejs.

Fichiers : `components/ui/date_picker.html`

```html
<pb-ui.date-picker name="due" placeholder="Pick a date" locale="fr-FR" :week_start="1" class="w-60" />
```

## Data table

A table with filtering, sorting, pagination and row selection, from Python data.

```bash
pyblade-ui add data-table
```

Nécessite : alpinejs.

Fichiers : `components/ui/data_table.html`

```html
<pb-ui.data-table selectable search="email" :page_size="5"
  :columns="[{'key': 'email', 'label': 'Email', 'sortable': True}, {'key': 'amount', 'label': 'Amount', 'sortable': True, 'align': 'right', 'format': 'currency'}]"
  :rows="[{'id': 1, 'email': 'ada@example.com', 'amount': 316}, {'id': 2, 'email': 'grace@example.com', 'amount': 242}]" />
```

## Chart

Bar, line and area charts in SVG, themed with --chart-1 to --chart-5, with a tooltip.

```bash
pyblade-ui add chart
```

Nécessite : alpinejs.

Fichiers : `components/ui/chart.html`

```html
<pb-ui.chart type="bar" x="month" :height="240"
  :series="[{'key': 'desktop', 'label': 'Desktop'}, {'key': 'mobile', 'label': 'Mobile'}]"
  :data="[{'month': 'Jan', 'desktop': 186, 'mobile': 80}, {'month': 'Feb', 'desktop': 305, 'mobile': 200}]" />
```

## Navigation menu

Site navigation with panels that open on hover and click.

```bash
pyblade-ui add navigation-menu
```

Nécessite : alpinejs.

Fichiers : `components/ui/navigation_menu.html`, `components/ui/navigation_menu_list.html`, `components/ui/navigation_menu_item.html`, `components/ui/navigation_menu_trigger.html`, `components/ui/navigation_menu_content.html`, `components/ui/navigation_menu_link.html`

```html
<pb-ui.navigation-menu>
  <pb-ui.navigation-menu-list>
    <pb-ui.navigation-menu-item>
      <pb-ui.navigation-menu-trigger>Products</pb-ui.navigation-menu-trigger>
      <pb-ui.navigation-menu-content class="w-64">
        <pb-ui.navigation-menu-link href="/ui">UI kit</pb-ui.navigation-menu-link>
      </pb-ui.navigation-menu-content>
    </pb-ui.navigation-menu-item>
    <pb-ui.navigation-menu-item>
      <pb-ui.navigation-menu-link href="/docs">Docs</pb-ui.navigation-menu-link>
    </pb-ui.navigation-menu-item>
  </pb-ui.navigation-menu-list>
</pb-ui.navigation-menu>
```

## Menubar

A desktop-style menu bar: File, Edit, View...

```bash
pyblade-ui add menubar
```

Nécessite : alpinejs.

Fichiers : `components/ui/menubar.html`, `components/ui/menubar_menu.html`, `components/ui/menubar_trigger.html`, `components/ui/menubar_content.html`, `components/ui/menubar_item.html`, `components/ui/menubar_separator.html`, `components/ui/menubar_label.html`, `components/ui/menubar_shortcut.html`

```html
<pb-ui.menubar>
  <pb-ui.menubar-menu>
    <pb-ui.menubar-trigger>File</pb-ui.menubar-trigger>
    <pb-ui.menubar-content>
      <pb-ui.menubar-item>New Tab <pb-ui.menubar-shortcut>⌘T</pb-ui.menubar-shortcut></pb-ui.menubar-item>
      <pb-ui.menubar-separator />
      <pb-ui.menubar-item>Print</pb-ui.menubar-item>
    </pb-ui.menubar-content>
  </pb-ui.menubar-menu>
</pb-ui.menubar>
```

## Drawer

A panel that rises from the bottom; drag its handle down to close it.

```bash
pyblade-ui add drawer
```

Installe aussi : `button`.

Nécessite : alpinejs.

Fichiers : `components/ui/drawer.html`, `components/ui/drawer_header.html`, `components/ui/drawer_footer.html`, `components/ui/drawer_title.html`, `components/ui/drawer_description.html`, `components/ui/drawer_close.html`

```html
<pb-ui.drawer>
  <pb-slot:trigger><pb-ui.button variant="outline">Open</pb-ui.button></pb-slot:trigger>
  <pb-ui.drawer-header>
    <pb-ui.drawer-title>Move goal</pb-ui.drawer-title>
    <pb-ui.drawer-description>Set your daily activity goal.</pb-ui.drawer-description>
  </pb-ui.drawer-header>
  <pb-ui.drawer-footer>
    <pb-ui.drawer-close><pb-ui.button variant="outline">Cancel</pb-ui.button></pb-ui.drawer-close>
  </pb-ui.drawer-footer>
</pb-ui.drawer>
```

## Input group

An input with icons, text, buttons or a keyboard hint attached inside it.

```bash
pyblade-ui add input-group
```

Nécessite : alpinejs.

Fichiers : `components/ui/input_group.html`, `components/ui/input_group_input.html`, `components/ui/input_group_textarea.html`, `components/ui/input_group_addon.html`, `components/ui/input_group_button.html`, `components/ui/input_group_text.html`

```html
<pb-ui.input-group>
  <pb-ui.input-group-input placeholder="example.com" />
  <pb-ui.input-group-addon><pb-ui.input-group-text>https://</pb-ui.input-group-text></pb-ui.input-group-addon>
  <pb-ui.input-group-addon align="inline-end"><pb-ui.input-group-button>Go</pb-ui.input-group-button></pb-ui.input-group-addon>
</pb-ui.input-group>
```

## Item

A row of content: media, title, description and actions.

```bash
pyblade-ui add item
```

Fichiers : `components/ui/item.html`, `components/ui/item_group.html`, `components/ui/item_separator.html`, `components/ui/item_media.html`, `components/ui/item_content.html`, `components/ui/item_title.html`, `components/ui/item_description.html`, `components/ui/item_actions.html`

```html
<pb-ui.item variant="outline">
  <pb-ui.item-content>
    <pb-ui.item-title>Two-factor authentication</pb-ui.item-title>
    <pb-ui.item-description>Verify via email or phone number.</pb-ui.item-description>
  </pb-ui.item-content>
  <pb-ui.item-actions><pb-ui.button size="sm">Enable</pb-ui.button></pb-ui.item-actions>
</pb-ui.item>
```

## Resizable

Panels you resize by dragging the handle between them, or with the arrow keys.

```bash
pyblade-ui add resizable
```

Nécessite : alpinejs.

Fichiers : `components/ui/resizable_group.html`, `components/ui/resizable_panel.html`, `components/ui/resizable_handle.html`

```html
<pb-ui.resizable-group direction="horizontal" class="min-h-48 rounded-lg border">
  <pb-ui.resizable-panel :size="50"><div class="p-6">One</div></pb-ui.resizable-panel>
  <pb-ui.resizable-handle with_handle />
  <pb-ui.resizable-panel :size="50"><div class="p-6">Two</div></pb-ui.resizable-panel>
</pb-ui.resizable-group>
```

## Typography

Text styles: headings, paragraph, lead, blockquote, list, inline code, and a prose wrapper for HTML content.

```bash
pyblade-ui add typography
```

Fichiers : `components/ui/typography_h1.html`, `components/ui/typography_h2.html`, `components/ui/typography_h3.html`, `components/ui/typography_h4.html`, `components/ui/typography_p.html`, `components/ui/typography_lead.html`, `components/ui/typography_large.html`, `components/ui/typography_small.html`, `components/ui/typography_muted.html`, `components/ui/typography_blockquote.html`, `components/ui/typography_list.html`, `components/ui/typography_inline_code.html`, `components/ui/prose.html`

```html
<pb-ui.typography-h1>The Joke Tax Chronicles</pb-ui.typography-h1>
<pb-ui.typography-lead>Once upon a time, in a far-off land...</pb-ui.typography-lead>
<pb-ui.prose>{!! article.html !!}</pb-ui.prose>
```

## Login form

A login card with email and password.

```bash
pyblade-ui add login-form
```

Installe aussi : `card`, `label`, `input`, `button`.

Fichiers : `components/blocks/login_form.html`

```html
<pb-blocks.login-form action="/login">@csrf</pb-blocks.login-form>
```

## Sidebar layout

An application shell: a sidebar with brand, navigation, a collapsible group and the user, beside a header and your page.

```bash
pyblade-ui add sidebar-layout
```

Installe aussi : `sidebar`, `collapsible`.

Nécessite : alpinejs.

Fichiers : `components/blocks/sidebar_layout.html`

```html
<pb-blocks.sidebar-layout :open="sidebar_open" title="Dashboard">
  <p>Your page</p>
</pb-blocks.sidebar-layout>
```
