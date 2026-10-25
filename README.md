# FA Websites (deploy otomatis Cloudflare Pages)

Setiap push ke branch `main` otomatis di-deploy Cloudflare Pages:

| Project Pages (Git) | Domain | Output dir |
|---|---|---|
| faindonesia-web | faindonesia.co.id | `out/faindonesia` |
| cariakuntan-web | cariakuntan.com | `out/cariakuntan` |

Alur update: edit sumber (`FA-Indonesia_Website_SIAP-UPLOAD-v58/`, `cariakuntan/gen/*.json`, `cariakuntan/feed.json`), jalankan
`python3 cariakuntan/build.py && python3 prep.py`, lalu commit dan push. Folder `out/` ikut di-commit supaya Cloudflare tidak perlu build.

Detail lain ada di README-DEPLOY.md.
