const CACHE_VERSION = "v6";  
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;

const STATIC_ASSETS = [
  "/",
  "/static/core/style.css",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-512x512.png",
  "/static/core/manifest.json",
  "/service-worker.js"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => k !== STATIC_CACHE && k !== DYNAMIC_CACHE)
          .map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  const req = event.request;
  const url = new URL(req.url);

  // Cache static assets (cache-first)
  if (STATIC_ASSETS.includes(url.pathname)) {
    event.respondWith(
      caches.match(req).then(cacheRes =>
        cacheRes ||
        fetch(req).then(fetchRes => {
          caches.open(STATIC_CACHE).then(cache =>
            cache.put(req, fetchRes.clone())
          );
          return fetchRes;
        })
      )
    );
    return;
  }

  // HTML pages → network first
  if (req.headers.get("accept")?.includes("text/html")) {
    event.respondWith(
      fetch(req)
        .then(fetchRes => {
          caches.open(DYNAMIC_CACHE).then(cache =>
            cache.put(req, fetchRes.clone())
          );
          return fetchRes;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // Default → cache first
  event.respondWith(
    caches.match(req).then(cacheRes => cacheRes || fetch(req))
  );
});
