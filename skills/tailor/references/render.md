# Rendering cv.html to cv.pdf

Try these in order and use the first that works. Tell the person which one you used.

## 1. Headless Chrome (preferred)

Find Chrome, then print:

```
"<chrome>" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="<company>/cv.pdf" "file://<absolute path to>/<company>/cv.html"
```

Typical Chrome locations:

- macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Linux: `google-chrome`, `chromium`, `chromium-browser` on the PATH
- Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`

Add `--no-sandbox` only when running as root (for example in a container); never otherwise.

## 2. The agent's browser tool

If a browser tool is available, open `cv.html` and export to PDF from there with background graphics off and no headers or footers, saving as `<company>/cv.pdf`.

## 3. Ask the person to print

If neither works, keep `cv.html`, tell the person plainly, and ask them to open it in a browser and use Print, then Save as PDF, with headers and footers off and A4 paper, saving as `<company>/cv.pdf`. Do not claim a PDF exists that does not.

## After rendering

Confirm the file exists and, if `pdftotext` is available, extract its text for the checks. If it is not available, read the PDF with the agent's PDF reading tool.
