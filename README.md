# Portfolio

Short notes for running and testing the site locally.

## Requirements

- Node.js 22, as defined in `.node-version`
- npm
- Python 3 for CV generation

## Local Setup

```sh
npm install
npm run setup:cv
```

Install Liberation Sans locally for the closest CV rendering. The GitHub Pages
pipeline installs it automatically.

## Development

Start the Astro dev server:

```sh
npm run dev
```

Open the local URL printed by Astro, usually `http://localhost:4321`.

## Checks

Run linting:

```sh
npm run lint
```

Check formatting:

```sh
npm run format:check
```

Build the CV, production site, and Pagefind index:

```sh
npm run build
```

Preview the production build:

```sh
npm run preview
```

`npm run build` is the best all-in-one local test before publishing.
