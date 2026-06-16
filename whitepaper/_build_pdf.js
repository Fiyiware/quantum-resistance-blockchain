#!/usr/bin/env node
/**
 * Convierte el whitepaper de Markdown a PDF.
 *
 * Cómo funciona:
 *   1) marked convierte Markdown → HTML.
 *   2) Se envuelve en una plantilla con CSS para PDF profesional A4.
 *   3) Chrome / Edge / Chromium headless imprime el HTML como PDF.
 *
 * Requisitos:
 *   - Node.js (ya instalado)
 *   - Chrome, Edge o Chromium
 *   - Paquete 'marked' (npm install marked)
 *
 * Uso:
 *   cd whitepaper
 *   npm install marked
 *   node _build_pdf.js          # español (por defecto)  -> whitepaper-v0.2.pdf
 *   node _build_pdf.js en       # inglés                 -> whitepaper-v0.2.en.pdf
 */

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { marked } = require("marked");

const here = __dirname;

// --- Selección de idioma -----------------------------------------------------
const lang = (process.argv[2] || "es").toLowerCase();
const VARIANTS = {
  es: { md: "whitepaper-v0.2.md",    pdf: "whitepaper-v0.2.pdf",    htmlLang: "es", title: "QRB Whitepaper v0.2" },
  en: { md: "whitepaper-v0.2.en.md", pdf: "whitepaper-v0.2.en.pdf", htmlLang: "en", title: "QRB Whitepaper v0.2 (EN)" },
};
const variant = VARIANTS[lang];
if (!variant) {
  console.error("ERROR: idioma no soportado '" + lang + "'. Usa 'es' o 'en'.");
  process.exit(1);
}

const mdPath = path.join(here, variant.md);
const htmlPath = path.join(here, "_" + variant.pdf.replace(/\.pdf$/, ".html"));
const pdfPath = path.join(here, variant.pdf);

if (!fs.existsSync(mdPath)) {
  console.error("ERROR: no se encuentra " + mdPath);
  process.exit(1);
}

console.log("Leyendo Markdown (" + lang + ")...");
const md = fs.readFileSync(mdPath, "utf-8");

console.log("Convirtiendo Markdown a HTML...");
marked.setOptions({ gfm: true, breaks: false });
const bodyHtml = marked.parse(md);

const css = `
  @page { size: A4; margin: 22mm 20mm 22mm 20mm; }
  * { box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10.5pt; line-height: 1.55; color: #1a1a1a;
    margin: 0; padding: 0;
  }
  h1 {
    font-size: 24pt; color: #0b3d91; margin-top: 0;
    border-bottom: 2px solid #0b3d91; padding-bottom: 6pt;
  }
  h2 {
    font-size: 16pt; color: #0b3d91; margin-top: 1.4em;
    border-bottom: 1px solid #cccccc; padding-bottom: 4pt;
    page-break-after: avoid;
  }
  h3 {
    font-size: 12.5pt; color: #1a1a1a; margin-top: 1.0em;
    page-break-after: avoid;
  }
  h4 { font-size: 11pt; color: #333; margin-top: 0.8em; page-break-after: avoid; }
  p, li { text-align: justify; }
  ul, ol { padding-left: 22pt; }
  li { margin: 2pt 0; }
  table {
    border-collapse: collapse; width: 100%;
    margin: 10pt 0; font-size: 9.5pt;
    page-break-inside: avoid;
  }
  th, td {
    border: 1px solid #888888; padding: 4pt 6pt;
    text-align: left; vertical-align: top;
  }
  th { background: #e8eef8; font-weight: 600; }
  code {
    font-family: 'Cascadia Code', Consolas, 'Courier New', monospace;
    background: #f4f4f4; padding: 1pt 4pt;
    font-size: 9.2pt; border-radius: 2pt;
  }
  pre {
    background: #f4f4f4; padding: 10pt;
    font-size: 8.5pt; line-height: 1.3;
    overflow-x: hidden; white-space: pre-wrap;
    page-break-inside: avoid;
    font-family: 'Cascadia Code', Consolas, 'Courier New', monospace;
    border-left: 3px solid #0b3d91;
  }
  pre code { background: transparent; padding: 0; }
  blockquote {
    border-left: 4px solid #0b3d91;
    padding: 6pt 14pt; color: #2a2a2a; font-style: italic;
    background: #f8f9fc; margin: 12pt 0;
  }
  blockquote p { margin: 4pt 0; }
  hr { border: none; border-top: 1px solid #cccccc; margin: 1.6em 0; }
  a { color: #0b3d91; text-decoration: none; }
  strong { color: #0b3d91; }
  .cover {
    text-align: center; padding: 80pt 0 40pt;
    border-bottom: 1px solid #cccccc;
  }
`;

const html = `<!DOCTYPE html>
<html lang="${variant.htmlLang}">
<head>
<meta charset="utf-8">
<title>${variant.title}</title>
<style>${css}</style>
</head>
<body>
${bodyHtml}
</body>
</html>`;

console.log("Guardando HTML intermedio...");
fs.writeFileSync(htmlPath, html, "utf-8");

console.log("Localizando Chrome / Edge / Chromium...");
// Rutas habituales en Windows...
const winCandidates = [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
];
// ...y nombres de binario habituales en Linux/macOS (se resuelven vía PATH).
const nixCandidates = [
  "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
  "microsoft-edge", "/usr/bin/google-chrome", "/usr/bin/chromium",
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
];

function resolveBrowser() {
  for (const p of winCandidates) {
    if (fs.existsSync(p)) return p;
  }
  for (const name of nixCandidates) {
    if (name.includes("/") || name.includes("\\")) {
      if (fs.existsSync(name)) return name;
    } else {
      try {
        const resolved = execFileSync("command", ["-v", name], { shell: true })
          .toString().trim();
        if (resolved) return resolved;
      } catch (_) { /* no está, probar siguiente */ }
    }
  }
  return null;
}

const browser = resolveBrowser();
if (!browser) {
  console.error("ERROR: no se encontró Chrome, Edge ni Chromium.");
  console.error("Instala uno de ellos o ejecuta este script en una máquina que lo tenga.");
  process.exit(1);
}
console.log("  Navegador: " + browser);

const fileUrl = "file://" + htmlPath.replace(/\\/g, "/").replace(/^([A-Za-z]:)/, "/$1");

console.log("Imprimiendo a PDF...");
execFileSync(
  browser,
  [
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    "--print-to-pdf=" + pdfPath,
    fileUrl,
  ],
  { stdio: "inherit" }
);

const sizeKB = (fs.statSync(pdfPath).size / 1024).toFixed(1);
console.log("");
console.log("OK PDF generado: " + pdfPath);
console.log("   Tamaño: " + sizeKB + " KB");
