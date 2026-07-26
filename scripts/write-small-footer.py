from datetime import date
from pathlib import Path

today = date.today()
html = f'''<footer class="text-center small-footer">
  <div class="container mt-0" style="font-size: 0.70rem;">
    &copy; {today:%Y} Silvio Fanzon
    &thinsp; &#67871; &thinsp;
    <a href="/contact/">Contact</a>
    &thinsp; &#67871; &thinsp;
    Updated: {today:%m/%Y}
  </div>
</footer>
'''

path = Path("includes/small-footer.html")
if not path.exists() or path.read_text(encoding="utf-8") != html:
    path.write_text(html, encoding="utf-8")