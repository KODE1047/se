self.addEventListener('install', (e) => {
  console.log('[Service Worker] Install');
});

self.addEventListener('fetch', (e) => {
  // Pass all requests through to the network
  e.respondWith(fetch(e.request));
});