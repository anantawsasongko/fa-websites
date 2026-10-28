# Bagian "Salah Langkah yang Paling Mahal": diagram kebocoran nilai + 5 penyebab (ID).
CAUSES_ID = dict(
  sub="Uang sudah keluar untuk akuntan, konsultan, atau audit, tapi hasilnya berakhir jadi arsip. Nilainya bocor di lima titik ini.",
  start="Biaya Dibayar", end="Benar-Benar Dipakai",
  cap="Ilustrasi alur nilai pekerjaan akuntan dan konsultan sebelum sampai ke bank, investor, atau tim internal.",
  items=[
   ("Tujuan Tidak Dikunci", "Laporan dibuat tanpa tahu dipakai bank, investor, atau pajak.", "Tentukan pemakai dan syaratnya dulu"),
   ("Format Bukan Milik Pemakai", "Rapi, tapi bank minta format dan rasio yang lain.", "Pakai checklist bank atau investor sejak awal"),
   ("Data Dasar Belum Bersih", "Saldo belum rekonsiliasi, auditor membongkar ulang.", "Rapikan pembukuan sebelum disusun"),
   ("Tidak Ada Pemilik Internal", "Konsultan selesai, tim tidak paham, dokumen masuk laci.", "Serah terima dan PIC internal"),
   ("Datang Setelah Ditolak", "Riwayat penolakan sudah tercatat di banyak bank.", "Screening sebelum mengajukan"),
  ])

CSS = """
.c-sub{color:var(--muted);max-width:640px;margin-top:12px}
.leak{margin:26px 0 0;border:1px solid var(--line);background:var(--panel);padding:18px 16px 10px}
.leak svg{display:block;width:100%;height:auto}
.leak .st{fill:#1F5BFF;transform-box:fill-box;transform-origin:left center;transform:scaleX(0)}
.leak .st.ok{fill:#0B7A5A}
.leak .gate{stroke:#E5484D;stroke-width:2;stroke-dasharray:4 4}
.leak .nb{fill:#fff;stroke:#E5484D;stroke-width:1.5}.leak .nt{fill:#B42318;font:600 13px var(--body);text-anchor:middle}
.leak .lb{fill:var(--ink);font:600 14px var(--body)}.leak .lb.ok{fill:#0B7A5A}
.leak .dp{fill:#E5484D;opacity:0}
.leak .v{display:none}.leak .vb{fill:#1F5BFF;transform-box:fill-box;transform-origin:left center;transform:scaleX(0)}.leak .vb.ok{fill:#0B7A5A}.leak .vt{fill:var(--ink);font:500 13px var(--body)}.leak .vn{fill:#B42318;font:700 12px var(--body);text-anchor:middle}.rv.in .leak .vb{animation:bar .6s ease both;animation-delay:calc(var(--i)*200ms)}
.leak figcaption{color:var(--muted);font-size:.82rem;margin-top:6px}
.rv.in .leak .st{animation:bar .6s ease both;animation-delay:calc(var(--i)*220ms)}
.rv.in .leak .dp{animation:drip 2.4s ease-in infinite;animation-delay:calc(var(--i)*220ms + .8s)}
@keyframes drip{0%{opacity:0;transform:translateY(0)}15%{opacity:1}100%{opacity:0;transform:translateY(56px)}}
.causes{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:16px}
.cause{border:1px solid var(--line);background:var(--paper);padding:16px 14px;display:grid;gap:6px;align-content:start;position:relative;opacity:0}
.cause::after{content:"";position:absolute;left:0;top:0;height:3px;width:0;background:#E5484D}
.cause .n{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;background:#FDECEC;color:#B42318;font-weight:700;font-size:.85rem}
.cause b{font-family:var(--display);font-size:1.02rem;font-weight:600;line-height:1.25}
.cause span{color:var(--muted);font-size:.88rem;line-height:1.45}
.cause em{font-style:normal;color:#0B7A5A;font-size:.85rem;font-weight:600;border-top:1px dashed var(--line);padding-top:8px;margin-top:2px}
.cause em::before{content:"✓ "}
.cause:hover{border-color:#E5484D}
.rv.in .cause{animation:up .5s ease both;animation-delay:calc(var(--i)*140ms + .4s)}
.rv.in .cause::after{animation:line .8s ease both;animation-delay:calc(var(--i)*140ms + .7s)}
@media (max-width:980px){.causes{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){.causes{grid-template-columns:1fr}.leak .h{display:none}.leak .v{display:block}}
@media (prefers-reduced-motion:reduce){.leak .dp{display:none}.leak .st{transform:none}.cause{opacity:1}}
"""

def leak_svg(C):
    hs = [150, 128, 104, 80, 58, 38]
    W, x0, sw, cy = 960, 0, 140, 110
    parts, gates = [], []
    for i, h in enumerate(hs):
        x = x0 + i * sw
        parts.append(f'<rect class="st" style="--i:{i}" x="{x}" y="{cy-h/2}" width="{sw}" height="{h}" fill-opacity="{1-i*.12:.2f}"/>')
        if i:
            gates.append(f'<line class="gate" x1="{x}" y1="18" x2="{x}" y2="{cy+80}"/><circle class="dp" style="--i:{i}" cx="{x+6}" cy="{cy-hs[i-1]/2+4}" r="4"/>'
                         f'<circle class="nb" cx="{x}" cy="{cy+96}" r="13"/><text class="nt" x="{x}" y="{cy+101}">{i}</text>')
    xe = x0 + len(hs) * sw
    parts.append(f'<rect class="st ok" style="--i:6" x="{xe}" y="{cy-12}" width="{W-xe}" height="24"/>')
    gates.append(f'<line class="gate" x1="{xe}" y1="18" x2="{xe}" y2="{cy+80}"/>')
    lab = f'<text class="lb" x="6" y="22">{C["start"]}</text><text class="lb ok" x="{W-4}" y="22" text-anchor="end">{C["end"]}</text>'
    return (f'<figure class="leak"><svg class="h" viewBox="0 0 {W} 230" role="img" aria-label="{C["start"]} bocor di lima titik sebelum {C["end"]}">'
            + "".join(parts) + "".join(gates) + lab + '</svg>' + vsvg(C) + f'<figcaption>{C["cap"]}</figcaption></figure>')

def causes_section(L, C):
    cards = "".join(f'<div class="cause" style="--i:{i}"><span class="n">{i+1}</span><b>{t}</b><span>{p}</span><em>{f}</em></div>'
                    for i, (t, p, f) in enumerate(C["items"]))
    return (f'<section><div class="wrap"><h2 class="sec-h">{L["trap_h2"]}</h2><p class="c-sub">{C["sub"]}</p>'
            + leak_svg(C) + f'<div class="causes">{cards}</div><p class="fixline"><i>✓</i>{L["fix"]}</p></div></section>')

def vsvg(C):
    ws = [300, 256, 208, 160, 116, 76]
    rows = [(C["start"], "")] + [(t, str(i + 1)) for i, (t, _, _) in enumerate(C["items"])]
    out, y = [], 6
    for i, ((t, n), w) in enumerate(zip(rows, ws)):
        out.append(f'<rect class="vb" style="--i:{i}" x="30" y="{y}" width="{w}" height="14" fill-opacity="{1-i*.12:.2f}"/>')
        if n: out.append(f'<circle class="nb" cx="12" cy="{y+7}" r="10"/><text class="vn" x="12" y="{y+11}">{n}</text>')
        out.append(f'<text class="vt" x="30" y="{y+32}">{"Setelah: " + t if n else t}</text>')
        y += 46
    out.append(f'<rect class="vb ok" style="--i:6" x="30" y="{y}" width="40" height="14"/><text class="vt" x="78" y="{y+12}" style="fill:#0B7A5A;font-weight:600">{C["end"]}</text>')
    return f'<svg class="v" viewBox="0 0 340 {y+22}" aria-hidden="true">' + "".join(out) + "</svg>"
