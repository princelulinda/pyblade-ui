# PyBlade UI

Des composants à copier dans votre projet [PyBlade](https://docs.pyblade.com), sur le modèle de shadcn/ui.

Ce n'est **pas** une bibliothèque de composants qu'on importe. La commande `pyblade-ui add` copie le code des composants dans votre projet. Le code vous appartient ensuite : vous le modifiez librement, sans attendre une nouvelle version.

- 59 composants (button, card, dialog, sidebar, data-table, chart, combobox, date-picker, command, menubar…) et deux blocs (`sidebar-layout`, `login-form`)
- Des thèmes en variables CSS au format shadcn (OKLCH, Tailwind CSS v4), avec mode clair et mode sombre
- Un CLI pour ajouter, comparer et mettre à jour les composants, et pour changer de thème
- Des registres distants : publiez votre propre catalogue de composants

Prérequis : Python 3.11 ou plus récent, PyBlade 0.3 ou plus récent et Tailwind CSS v4. Les composants interactifs ont aussi besoin d'Alpine.js.

## Démarrage

```bash
pip install pyblade-ui
cd mon-projet-pyblade            # là où se trouve pyblade.toml
pyblade-ui init --base zinc --color blue
pyblade-ui add button card dialog
```

`init` effectue les opérations suivantes :

1. Il écrit `pyblade-ui.toml`.
2. Il génère `static/css/theme.css`.
3. Il ajoute `@import "./theme.css";` dans `static/css/tailwind.css`.
4. Il installe `theme-script` et `mode-toggle`.

Ensuite :

```python
# Django : settings.py
INSTALLED_APPS = [..., "pyblade_ui"]

# Flask, FastAPI… : une fois au démarrage
import pyblade_ui
```

```html
<head>
  <pb-ui.theme-script />
  <link rel="stylesheet" href="@static('css/app.css')" />
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.9/dist/cdn.min.js"></script>
</head>
```

Adaptez le chemin de la feuille de style compilée (`@static`) à votre framework.

```html
<pb-ui.card class="max-w-md">
  <pb-ui.card-header>
    <pb-ui.card-title>Équipe</pb-ui.card-title>
    <pb-ui.card-description>Invitez vos collègues.</pb-ui.card-description>
  </pb-ui.card-header>
  <pb-ui.card-content>
    <pb-ui.button variant="outline" class="w-full">Inviter</pb-ui.button>
  </pb-ui.card-content>
</pb-ui.card>
```

La liste complète des composants, avec un exemple pour chacun, se trouve dans [docs/components.md](docs/components.md).

## Le CLI

| Commande | Rôle |
|---|---|
| `pyblade-ui init [--base] [--color] [--radius]` | Configure le projet et génère le thème |
| `pyblade-ui add <noms…> \| --all [--overwrite] [--dry-run]` | Copie des composants avec leurs dépendances |
| `pyblade-ui list` | Liste le registre et indique ce qui est déjà installé |
| `pyblade-ui diff [noms…]` | Montre vos modifications par rapport au registre |
| `pyblade-ui theme list \| show \| set --base slate --color rose --radius 0.75rem` | Gère le thème |

`add` ne remplace jamais un fichier que vous avez modifié, sauf si vous passez `--overwrite`. Utilisez `diff` pour voir ce qui a changé avant de mettre à jour.

## Thèmes

- **Bases** : `neutral`, `zinc`, `slate`, `stone`, `gray`. C'est la teinte des gris utilisés pour les fonds, les bordures et le texte atténué.
- **Couleurs** : `neutral`, `blue`, `green`, `violet`, `rose`, `red`, `orange`, `yellow`. Elles définissent `--primary` et `--ring`.
- **Rayon** : la variable `--radius`. Elle sert à calculer `rounded-sm`, `rounded-md`, `rounded-lg` et `rounded-xl`.
- **Ombres** : les variables `--shadow-2xs` à `--shadow-2xl`, reliées aux classes `shadow-*` de Tailwind. Par défaut ce sont exactement les ombres de Tailwind ; `render_theme(shadow={...})` les calcule à partir d'une ombre de base (couleur, opacité, flou, étalement, décalage X et Y), et l'éditeur de thèmes les règle. Un projet existant les obtient avec `pyblade-ui theme set`.

Les variables suivent le format de shadcn/ui : `--background`, `--foreground`, `--card`, `--popover`, `--primary`, `--secondary`, `--muted`, `--accent`, `--destructive`, `--border`, `--input`, `--ring` et `--chart-1` à `--chart-5`. Deux couples s'ajoutent : `--success`/`--success-foreground` et `--warning`/`--warning-foreground`. Elles sont exposées à Tailwind via `@theme inline`, ce qui permet d'écrire `bg-primary`, `text-muted-foreground`, `border-border`, etc.

Pour personnaliser une variable, écrivez-la **sous le marqueur** `/* pyblade-ui:custom … */` de `theme.css`. `pyblade-ui theme set` régénère tout le fichier sauf cette partie :

```css
/* pyblade-ui:custom -- everything below this line is kept when the theme is regenerated */
:root { --primary: oklch(0.6 0.2 160); }
.dark { --primary: oklch(0.7 0.18 160); }
```

Le mode sombre repose sur la classe `.dark` posée sur `<html>`. `theme-script` l'applique avant l'affichage de la page, sans clignotement, et `mode-toggle` la bascule.

## Sidebar et état côté serveur

Le sidebar enregistre son état (replié ou déplié) dans le cookie `sidebar_state`. Relisez-le côté serveur pour que la page soit rendue directement dans le bon état, sans clignotement :

```python
# Django : ajoutez le context processor, qui fournit `sidebar_open`
"OPTIONS": {"context_processors": [..., "pyblade_ui.context_processors.sidebar"]}

# Flask, FastAPI… : passez-le vous-même
from pyblade_ui import sidebar_open
render("dashboard", sidebar_open=sidebar_open(request))
```

```html
<pb-ui.sidebar-provider :open="sidebar_open" collapsible="icon">…</pb-ui.sidebar-provider>
```

Le sidebar utilise les variables `--sidebar-*` du thème : sur un projet existant, lancez `pyblade-ui theme set` pour les ajouter à `theme.css`.

## Données Python et erreurs de formulaire

`pyblade_ui` ajoute le filtre `tojson`, qui passe des données Python à Alpine : c'est ainsi que `data-table` et `chart` reçoivent leurs lignes.

```html
<pb-ui.data-table :rows="payments" :columns="columns" selectable search="email" />
<pb-ui.chart type="bar" x="month" :data="visitors" :series="[{'key': 'desktop', 'label': 'Desktop'}]" />
```

`field` et `field-error` affichent les erreurs de validation avec `@error`. Un composant ne voit pas les variables du template parent : passez-leur les erreurs.

```html
<pb-ui.field :errors="form.errors" name="email">
  <pb-ui.field-label for="email">Email</pb-ui.field-label>
  <pb-ui.input id="email" name="email" />
  <pb-ui.field-error :errors="form.errors" name="email" />
</pb-ui.field>
```

## Écrire un composant

Voir [docs/architecture.md](docs/architecture.md). En bref :

```html
@props({'variant': 'default'})
<span data-slot="badge" {{ attributes.cn(
    "inline-flex rounded-md px-2 py-0.5 text-xs",
    {'default': 'bg-primary text-primary-foreground', 'outline': 'border'}[variant],
) }}>{{ slot }}</span>
```

`attributes.cn(...)` produit **un seul** attribut `class`. On y trouve les classes du composant, puis celles de l'appelant, et les conflits Tailwind sont résolus en faveur de l'appelant : `px-8` remplace `px-4`. Viennent ensuite tous les autres attributes passés par l'appelant (`id`, `disabled`, `x-on:click`, `hx-post`…).

## Développement

```bash
pip install -e ".[dev]"
pytest                               # 90 tests : thèmes, registre, CLI, rendu de chaque composant
python scripts/check_registry.py     # valide le registre avant publication
python scripts/gen_docs.py           # régénère docs/components.md
cd examples/demo && npm install && npm run build   # page de démo dans dist/index.html
```
