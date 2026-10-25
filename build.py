"""Baut index.html aus src/template.html.

Bettet die web-ifc-WASM-Datei und das Beispielmodell direkt in die Seite ein,
damit index.html ohne Server funktioniert (Doppelklick genügt).

Aufruf:  python build.py
"""
import base64, pathlib, urllib.request

ROOT = pathlib.Path(__file__).parent
WEB_IFC_VERSION = "0.0.66"
WASM = ROOT / "vendor" / "web-ifc.wasm"
SAMPLE = ROOT / "beispiele" / "co2Test.ifc"

if not WASM.exists():
    WASM.parent.mkdir(exist_ok=True)
    url = f"https://cdn.jsdelivr.net/npm/web-ifc@{WEB_IFC_VERSION}/web-ifc.wasm"
    print("Lade", url)
    WASM.write_bytes(urllib.request.urlopen(url).read())

html = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
ifc = SAMPLE.read_text(encoding="utf-8", errors="replace")
if "</script" in ifc.lower():
    raise SystemExit("Beispiel-IFC enthält '</script' und kann nicht eingebettet werden.")

out = (html.replace("__WASM_B64__", base64.b64encode(WASM.read_bytes()).decode())
           .replace("__SAMPLE_IFC__", ifc))
(ROOT / "index.html").write_text(out, encoding="utf-8")
print(f"index.html geschrieben ({len(out)/1e6:.1f} MB)")
