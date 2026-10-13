# Architecture

```
pyblade-ui/
├── src/pyblade_ui/
│   ├── utils.py              # cn() / tw_merge() et le filtre de template `cn`
│   ├── apps.py               # AppConfig Django (enregistre le filtre)
│   ├── config.py             # lit pyblade.toml et pyblade-ui.toml
│   ├── themes/__init__.py    # palettes OKLCH et génération de theme.css
│   ├── registry/
│   │   ├── registry.json     # le catalogue (source de vérité)
│   │   ├── registry.schema.json
│   │   ├── ui/*.html         # composants -> components/ui/
│   │   └── blocks/*.html     # blocs      -> components/blocks/
│   └── cli/main.py           # pyblade-ui init | add | list | diff | theme
├── tests/                    # rendu réel de chaque composant avec PyBlade
├── scripts/                  # check_registry.py, gen_docs.py
├── docs/
└── examples/demo/            # projet PyBlade de démonstration (Tailwind v4)
```

## Le parcours d'un composant

```
registry/ui/button.html  ──pyblade-ui add──▶  <projet>/components/ui/button.html  ──▶  <pb-ui.button>
```

Le chemin d'un fichier dans le registre indique aussi où il sera copié, à l'intérieur du dossier `paths.components` défini dans `pyblade.toml`. C'est ce chemin qui donne l'espace de noms de la balise : `ui/` devient `pb-ui.` et `blocks/` devient `pb-blocks.`.

## Règles pour écrire un composant (PyBlade 0.3)

Ces règles viennent de tests sur le moteur PyBlade 0.3.0 lui-même. Sur plusieurs points, la documentation de PyBlade ne correspond pas à son comportement réel.

1. **Les noms de fichiers sont en snake_case.** La balise `<pb-ui.card-header>` est convertie en `ui.card_header`, et PyBlade ne cherche que `card_header.html`. Un fichier nommé `card-header.html` n'est pas trouvé, contrairement à ce qu'annonce la doc.
2. **Un composant n'a qu'un seul élément racine.** `@props(...)` peut le précéder. Une racine conditionnelle (`@if … <a> @else <button> @endif`) est refusée : c'est pour cela que `button-link` est un composant séparé.
3. **Utilisez `{{ attributes.cn(...) }}` sur l'élément racine, et non `{{ attributes }}`.** Avec `{{ attributes }}`, la `class` de l'appelant devient un *deuxième* attribut `class`, que le navigateur ignore. Le sandbox interdit aussi `attributes.get()`, `attributes.merge()` et `attributes['class']`. Le filtre `cn` fourni par `pyblade_ui` règle ces trois problèmes.
4. **Gérez les variantes avec un dictionnaire indexé** : `{'default': '…', 'outline': '…'}[variant]`. Une expression peut s'étendre sur plusieurs lignes. Les ternaires `a if b else c` ne sont **pas** acceptés : écrivez par exemple `str(bool(open)).lower()`.
5. **Pour Alpine.js, préférez `x-on:` et `x-bind:`** à `@click` et `:class`. Les deux formes passent aujourd'hui, mais `@…` est aussi la syntaxe des directives PyBlade.
6. **Ajoutez `data-slot="nom"`** sur la racine, comme shadcn. Cela permet de cibler les sous-parties, par exemple `has-data-[slot=card-action]:…`.
7. **Ne nommez pas une prop `default`, `class` ou `for`** : ce sont des mots-clés Python, donc illisibles dans `{{ }}`. Ces noms restent utilisables comme attributes HTML, qui passent par `attributes`.
8. **Partagez l'état par la portée Alpine.** `tabs` déclare `x-data="{ tab }"`, et `tabs-trigger` et `tabs-content` le lisent. C'est ce qui permet de composer comme dans shadcn.
9. **Un état qui doit survivre au rechargement se rend côté serveur.** Le composant le reçoit en prop (`:open="sidebar_open"`) et pose les attributs `data-*` correspondants dès le HTML ; tout le CSS en dépend, Alpine ne fait que les mettre à jour. C'est ce que fait `sidebar-provider` avec le cookie `sidebar_state` (voir `pyblade_ui/sidebar.py`).
10. **Pas d'opérateur `in` ni de `round()` dans `{{ }}`** : le bac à sable de PyBlade les refuse. Pour savoir si un champ a une erreur, utilisez `@error(name)…@enderror`, y compris dans un attribut.
11. **Avec Alpine, liez `style` en objet** (`x-bind:style="{ left: x + 'px' }"`) sur un élément qui a aussi `x-show` : une chaîne remplace tout l'attribut et efface le `display: none` de `x-show`. De même, `x-bind:disabled` doit recevoir un booléen : une chaîne vide désactive l'élément.

## Le registre

Chaque entrée de `registry.json` a la forme suivante (voir `registry.schema.json`) :

```json
{
  "name": "dialog",
  "type": "registry:ui",
  "title": "Dialog",
  "description": "A modal window…",
  "files": ["ui/dialog.html", "ui/dialog_header.html"],
  "registryDependencies": ["button"],
  "dependencies": { "js": ["alpinejs"], "python": [] },
  "usage": "<pb-ui.dialog>…</pb-ui.dialog>"
}
```

### Publier son propre registre

Un registre est un dossier qui contient `registry.json` et les fichiers qu'il référence. Pour l'utiliser depuis un dépôt GitHub :

```bash
pyblade-ui init --registry https://raw.githubusercontent.com/<org>/<repo>/main/registry
# ou plus tard dans pyblade-ui.toml : [ui] registry = "…"
```

Avant de publier, lancez `python scripts/check_registry.py chemin/vers/registry`.

## Le thème

`themes/__init__.py` associe les nuances d'une palette Tailwind (50 à 950, en OKLCH) aux variables de shadcn, en mode clair et en mode sombre. La couleur d'accent remplace ensuite `--primary`, `--primary-foreground` et `--ring`. Le CSS généré contient, dans l'ordre :

- la variante `dark` ;
- les blocs `:root` et `.dark` ;
- `@theme inline`, qui fait de chaque variable une couleur Tailwind ;
- une couche `base` ;
- le marqueur `custom`, sous lequel vos ajouts sont conservés.

## Pistes pour la suite

- Relier `pagination` à `copy:stubs --pagination`, et proposer une data-table côté serveur (tri et pagination par l'URL, ou Live Components) pour les gros volumes.
- Écrire des versions Live Components pour les composants à état serveur, comme une data-table avec tri et pagination.
- Ajouter un site de documentation, lui-même fait avec PyBlade, avec un aperçu en direct de chaque composant.
- Proposer à PyBlade une commande `pyblade add`, ainsi que la correction de la fusion `class` et des noms de fichiers kebab-case.
