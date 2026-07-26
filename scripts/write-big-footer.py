from datetime import date
from pathlib import Path

today = date.today()

html = f'''<footer class="big-footer">
  <div class="container footer-container">
    <div class="footer-flex">

      <div class="footer-left">
        <h4 class="footer-name"><b>Silvio Fanzon</b></h4>

        <p class="footer-line">
          <i class="fas fa-envelope"></i>
          <a href="mailto:S.Fanzon@hull.ac.uk">S.Fanzon@hull.ac.uk</a>
        </p>

        <p class="footer-line">
          <i class="fas fa-map-marker-alt"></i>
          <a href="https://www.google.com/maps/place/Robert+Blackburn+Building/@53.7714841,-0.3714448,17z" target="_blank">
            Office 311C<br>
            Robert Blackburn Building<br>
            University of Hull<br>
            Hull HU6 7RX<br>
            United Kingdom
          </a>
        </p>

        <p class="footer-line">
          <i class="fas fa-briefcase"></i>
          <a href="https://www.hull.ac.uk/staff-directory/silvio-fanzon" target="_blank">
            Homepage @ Hull
          </a>
        </p>

        <div class="social">
          <div class="contact-icons footer-contact-icons">
            <a href="https://www.linkedin.com/in/fanzon" title="LinkedIn" target="_blank">
              <i class="fa-brands fa-linkedin"></i>
            </a>
            <a href="https://scholar.google.com/citations?user=9yJyLsoAAAAJ" title="Google Scholar" target="_blank">
              <i class="ai ai-google-scholar-square"></i>
            </a>
            <a href="https://www.researchgate.net/profile/Silvio-Fanzon/" title="ResearchGate" target="_blank">
              <i class="ai ai-researchgate-square"></i>
            </a>
            <a href="https://orcid.org/0000-0003-1974-1434" title="ORCID" target="_blank">
              <i class="ai ai-orcid-square"></i>
            </a>
            <a href="https://arxiv.org/a/fanzon_s_1" title="arXiv" target="_blank">
              <i class="ai ai-arxiv-square"></i>
            </a>
            <a href="https://github.com/sfanzon" title="GitHub" target="_blank">
              <i class="fa-brands fa-github"></i>
            </a>
          </div>
        </div>

        <p class="footer-built">
          &copy; {today:%Y} Silvio Fanzon<br>
          Website built with <a href="https://quarto.org/" target="_blank">Quarto</a><br>
          Source code available on
          <a href="https://github.com/sfanzon/sfanzon.github.io" target="_blank">GitHub</a>
        </p>
      </div>

      <div class="footer-map">
        <iframe
          src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d2358.011416469691!2d-0.3714448!3d53.7714841!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4878bfaf9f89a781%3A0xf1623fd4c5175579!2sRobert%20Blackburn%2C%20Hull%20HU6%207RU!5e0!3m2!1sen!2suk"
          allowfullscreen=""
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade">
        </iframe>
      </div>

    </div>
  </div>
</footer>
'''

path = Path("includes/big-footer.html")
if not path.exists() or path.read_text(encoding="utf-8") != html:
    path.write_text(html, encoding="utf-8")
