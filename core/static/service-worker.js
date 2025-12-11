const CACHE_NAME = "bhoomitra-cache-v1";

const STATIC_ASSETS = [
  "/",
  "/static/core/style.css",

  // PWA files
  "/static/manifest.json",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-512x512.png",

  // Optional: cache chart.js for offline functionality
  "https://cdn.jsdelivr.net/npm/chart.js",
];

// -------- INSTALL --------
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log("[SW] Caching static assets");
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// -------- FETCH --------
self.addEventListener("fetch", event => {
  const req = event.request;
  const url = new URL(req.url);

  // Do NOT interfere with API or WebSocket requests
  if (url.pathname.startsWith("/api/") || url.pathname.startsWith("/ws/")) {
    return event.respondWith(fetch(req));
  }

  // Cache-first strategy for static files
  event.respondWith(
    caches.match(req).then(cachedRes => {
      if (cachedRes) return cachedRes;

      // Otherwise fetch from network & cache dynamically
      return fetch(req).then(networkRes => {
        return caches.open(CACHE_NAME).then(cache => {
          // Cache only static files, not POST responses
          if (req.method === "GET" && url.pathname.startsWith("/static/")) {
            cache.put(req, networkRes.clone());
          }
          return networkRes;
        });
      });
    })
  );
});
