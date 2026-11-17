# -*- coding: utf-8 -*-
def T(head, rows):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tblwrap"><table class="tbl"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
