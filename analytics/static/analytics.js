(function () {
  const COOKIE_NAME = "an_id";
  const ENDPOINT = "http://analytics.test:9100/collect";

  function readCookie(name) {
    const hit = document.cookie.split("; ").find(c => c.startsWith(name + "="));
    return hit ? hit.split("=")[1] : null;
  }

  function writeCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
  }

  function newId() {
    const bytes = new Uint8Array(8);
    crypto.getRandomValues(bytes);
    return Array.from(bytes, b => b.toString(16).padStart(2, "0")).join("");
  }

  // 1-2-3-4: check, generate, store, persist
  let aid = readCookie(COOKIE_NAME);
  const isNew = !aid;
  if (isNew) {
    aid = newId();
    writeCookie(COOKIE_NAME, aid, 365);
  }

  function beacon(extra) {
    const params = new URLSearchParams(Object.assign({
      aid:    aid,
      site:   location.hostname,
      page:   location.pathname,
      title:  document.title,
      lang:   navigator.language,
      screen: screen.width + "x" + screen.height,
      tz:     Intl.DateTimeFormat().resolvedOptions().timeZone
    }, extra));
    new Image().src = ENDPOINT + "?" + params.toString();
  }

  // page view
  beacon({ event: "pageview" });

  // browsing activity: outbound clicks
  document.addEventListener("click", function (e) {
    const link = e.target.closest("a");
    if (link) beacon({ event: "click", target: link.getAttribute("href") });
  });

  console.log("[analytics] aid =", aid, "| new =", isNew,
              "| document.cookie =", document.cookie);
})();