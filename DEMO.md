# DHI Net Demo Deploy

## Fastest Manual Demo

Use Netlify Drop for the fastest free public demo URL.

1. Run:

   ```bash
   bash scripts/build_demo.sh
   ```

2. Open:

   ```text
   https://app.netlify.com/drop
   ```

3. Drag the generated `demo/dhi-net-demo-YYYYMMDD-HHMMSS` folder into Netlify Drop.

4. Share the generated `*.netlify.app` URL.

## What The Script Does

- Regenerates `frontend/data.js` from the Excel data pipeline.
- Builds the Vite frontend into `frontend/dist`.
- Copies the static demo into `demo/dhi-net-demo-YYYYMMDD-HHMMSS`.
- Creates a zip beside it for backup or Cloudflare Pages Direct Upload.

## Notes

- Do not upload only `index.html`; upload the whole generated demo folder.
- The DHI data is bundled into the frontend build, so this static demo does not need a backend server.
- SPA deep links are supported by `frontend/public/_redirects` and `netlify.toml`.
