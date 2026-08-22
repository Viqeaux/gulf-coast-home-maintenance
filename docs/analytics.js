/* Google Analytics 4.
 *
 * The Measurement ID lives here and nowhere else. Every measured page loads
 * this file, and a constant pasted into pages is a constant that drifts: the
 * project has already paid for that lesson with the four version markers.
 *
 * An empty GA_ID means no tracking at all. Nothing is requested, no cookie is
 * set, and every page behaves exactly as it did before this file existed. That
 * is the state this shipped in, so pasting the ID below is the only step
 * between here and live.
 *
 * What this collects is described in docs/privacy.html. The two are a pair:
 * that page promises visitors it says so before anything watches them, so if
 * this file changes what it gathers, that page changes in the same release.
 *
 * Not loaded by docs/404.html or docs/privacy.html. Both run no script on
 * purpose, both see almost no traffic, and widening their policy would buy
 * nothing worth the trade.
 */

var GA_ID = "G-KB3D46WDYK";

if (GA_ID) {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };

  window.gtag("js", new Date());
  window.gtag("config", GA_ID);

  /* Appended rather than written inline so the page's script-src does not have
     to trust anything beyond googletagmanager.com, which the CSP names. */
  var tag = document.createElement("script");
  tag.async = true;
  tag.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
  document.head.appendChild(tag);
}
