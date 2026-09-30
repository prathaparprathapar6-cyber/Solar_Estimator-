/* VoltRoof minimal offline shell */
const CACHE = "voltroof-shell-v3";
const ASSETS = ["/", "/index.html", "/VoltRoof_Combined.html"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS).catch(() => {})));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  // Network-first for API, cache-first for same-origin navigations
  if (url.pathname.startsWith("/api/")) {
    e.respondWith(fetch(e.request).catch(() => new Response(JSON.stringify({ offline: true }), { headers: { "Content-Type": "application/json" } })));
    return;
  }
  if (e.request.mode === "navigate") {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request).then((r) => r || caches.match("/")))
    );
    return;
  }
  // CDN fonts / chart - cache fallback
  e.respondWith(
    caches.open(CACHE).then(async (cache) => {
      const cached = await cache.match(e.request);
      try {
        const fresh = await fetch(e.request);
        if (fresh && fresh.ok && (url.hostname.includes("jsdelivr") || url.hostname.includes("googleapis") || url.hostname.includes("gstatic"))) {
          cache.put(e.request, fresh.clone());
        }
        return fresh;
      } catch {
        return cached || Response.error();
      }
    })
  );
});
