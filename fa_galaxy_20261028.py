# -*- coding: utf-8 -*-
"""FA Galaxy dipersempit (28 Okt 2026): Galaxy hanya metode FA untuk aplikasi dan kalkulator.
Isi standar resmi IAI/IAPI (daftar PSAK, ringkasan standar) diarahkan ke updatesak.com.
Mengubah sumber FA-Indonesia_Website_SIAP-UPLOAD-v58 (apps/ dan galaxy/). Idempoten."""
import os, re
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FA-Indonesia_Website_SIAP-UPLOAD-v58")
U = "https://updatesak.com"

def sub1(t, old, new, label):
    if new in t: return t
    assert old in t, "tidak ketemu: " + label
    return t.replace(old, new, 1)

def i18n(t, key, en, zh):
    # ganti nilai key di blok en dan zh (urutan kemunculan: en dulu, lalu zh)
    vals = [en, zh]; out = []; pos = 0; n = 0
    for m in re.finditer(r'"%s": "((?:[^"\\]|\\.)*)"' % re.escape(key), t):
        if n >= 2: break
        out.append(t[pos:m.start()]); out.append('"%s": "%s"' % (key, vals[n].replace('"', '\\"'))); pos = m.end(); n += 1
    assert n == 2, "i18n key %s ditemukan %d kali" % (key, n)
    out.append(t[pos:]); return "".join(out)

# ---------- apps/index.html ----------
p = os.path.join(B, "apps", "index.html"); t = open(p, encoding="utf-8").read()
t = re.sub(r'(<p class="kick" data-i18n="e1">)[^<]*(</p>)', r'\1Panduan dan Metodologi FA\2', t, 1)
t = re.sub(r'(<p data-i18n="e2" class="desc">)[^<]*(</p>)', r'\1Cara pakai setiap aplikasi FA, metodologi yang kami sesuaikan di baliknya, dan cara membaca hasil kalkulator. Standar resmi IAI dan IAPI ada di Update SAK.\2', t, 1)
old5 = re.search(r'<div class="ap-app"><div class="nm"><b data-i18n="e5n">.*?</a></div>', t, re.S).group(0)
new5 = ('<div class="ap-app"><div class="nm"><b data-i18n="e5n">Update SAK · Standar IAI dan IAPI</b><span class="chip on" data-i18n="e5c">Standar</span></div>'
        '<p data-i18n="e5d">Daftar PSAK, ISAK, SAK EP, dan SAK EMKM terbaru beserta ringkasannya, diperbarui mengikuti SAK Online IAI.</p>'
        '<a class="btn solid sm" href="' + U + '/eksplor/" target="_blank" rel="noopener" data-i18n="e5b">Buka Update SAK</a></div>')
t = t.replace(old5, new5, 1)
t = re.sub(r'(<p data-i18n="e4d">)[^<]*(</p>)', r'\1Tulisan praktis dari pengalaman FA tentang laporan keuangan, audit, kredit bank, dan persiapan IPO.\2', t, 1)
t = i18n(t, "e1", "FA Guides and Methodology", "FA 指南与方法论")
t = i18n(t, "e2", "How to use each FA app, the methodology we adapted behind it, and how to read calculator results. Official IAI and IAPI standards live on Update SAK.",
         "每个 FA 应用的使用方法、我们为其调整的方法论，以及如何解读计算器结果。IAI 与 IAPI 的正式准则请见 Update SAK。")
t = i18n(t, "e5n", "Update SAK · IAI and IAPI Standards", "Update SAK · IAI 与 IAPI 准则")
t = i18n(t, "e5c", "Standards", "准则")
t = i18n(t, "e5d", "Current PSAK, ISAK, SAK EP and SAK EMKM with summaries, updated in line with IAI SAK Online.", "最新 PSAK、ISAK、SAK EP 与 SAK EMKM 及其摘要，随 IAI SAK Online 更新。")
t = i18n(t, "e5b", "Open Update SAK", "打开 Update SAK")
t = i18n(t, "e4d", "Practical writing from FA's work on financial statements, audit, bank credit, and IPO readiness.", "来自 FA 实务经验的文章，涵盖财务报表、审计、银行信贷和 IPO 准备。")
open(p, "w", encoding="utf-8").write(t)

# ---------- galaxy/index.html ----------
p = os.path.join(B, "galaxy", "index.html"); t = open(p, encoding="utf-8").read()
t = re.sub(r'(<span data-i18n="t5">)[^<]*(</span>)', r'\1Standar IAI dan IAPI\2', t, 1)
t = re.sub(r'(<h2 data-i18n="p0h">)[^<]*(</h2>)', r'\1Standar Resmi di Update SAK\2', t, 1)
t = re.sub(r'(<p data-i18n="p0" class="intro">)[^<]*(</p>)', r'\1FA Galaxy hanya berisi metode yang kami sesuaikan untuk aplikasi dan kalkulator FA. Isi standar resmi IAI dan IAPI, dari PSAK dan ISAK sampai SAK EP dan SAK EMKM, kami kumpulkan di Update SAK dan diperbarui mengikuti SAK Online IAI.\2', t, 1)
sec = re.search(r'(<article class="gx-sec" id="psak">.*?)<ul class="gx-read">.*?</ul>', t, re.S)
items = [("/eksplor/", "Linimasa Update PSAK 2026 sampai 2029", "Hub"),
         ("/psak/118/", "PSAK 118: Penyajian dan Pengungkapan dalam Laporan Keuangan", "Efektif 2027"),
         ("/psak/119/", "PSAK 119: Entitas Anak tanpa Akuntabilitas Publik", "Efektif 2027"),
         ("/psak/221/", "PSAK 221: Pengaruh Perubahan Kurs Valuta Asing", "Amendemen 2027"),
         ("/psak/228/", "PSAK 228: Investasi pada Entitas Asosiasi dan Ventura Bersama", "Amendemen 2027"),
         ("/psak/401/", "PSAK 401: Penyajian Laporan Keuangan Syariah", "Efektif 2027"),
         ("/psak/109/", "PSAK 109 dan PSAK 107: Instrumen Keuangan", "Amendemen 2026"),
         ("/psak/120/", "PSAK 120: Aset dan Liabilitas Regulatori", "Efektif 2029")]
ul = '<ul class="gx-read">' + "".join('<li><a href="%s%s" target="_blank" rel="noopener"><span>%s</span><small>Update SAK · %s</small></a></li>' % (U, h, n, s) for h, n, s in items) + '</ul>'
btn = '<a class="btn solid" href="' + U + '/" target="_blank" rel="noopener" style="justify-self:start;margin-top:18px" data-i18n="p0b">Buka Update SAK</a>'
if 'data-i18n="p0b"' not in t:
    t = t[:sec.start()] + sec.group(1) + ul + btn + t[sec.end():]
t = t.replace('Lihat <a href="/artikel/daftar-psak-isak-2026-2027/">daftar PSAK dan ISAK 2026-2027</a>.',
              'Daftar lengkapnya ada di <a href="' + U + '/eksplor/" target="_blank" rel="noopener">Update SAK</a>.', 1)
t = i18n(t, "t5", "IAI & IAPI Standards", "IAI 与 IAPI 准则")
t = i18n(t, "p0h", "Official Standards on Update SAK", "Update SAK 上的正式准则")
t = i18n(t, "p0", "FA Galaxy only covers the methods we adapted for FA's apps and calculators. The official IAI and IAPI standards, from PSAK and ISAK to SAK EP and SAK EMKM, are collected on Update SAK and kept in line with IAI SAK Online.",
         "FA Galaxy 只收录我们为 FA 应用和计算器调整的方法。IAI 与 IAPI 的正式准则，从 PSAK、ISAK 到 SAK EP 和 SAK EMKM，统一收录在 Update SAK，并随 IAI SAK Online 更新。")
t = i18n(t, "mr1", "<b>Accounting standards:</b> current PSAK numbering per SAK Online (IAI). The full list is on <a href='" + U + "/eksplor/' target='_blank' rel='noopener'>Update SAK</a>.",
         "<b>会计准则：</b>采用 IAI SAK Online 的最新 PSAK 编号。完整清单见 <a href='" + U + "/eksplor/' target='_blank' rel='noopener'>Update SAK</a>。")
if '"p0b"' not in t:
    t = t.replace('"en": {', '"en": {"p0b": "Open Update SAK", ', 1).replace('"zh": {', '"zh": {"p0b": "打开 Update SAK", ', 1)
open(p, "w", encoding="utf-8").write(t)
print("ok")
