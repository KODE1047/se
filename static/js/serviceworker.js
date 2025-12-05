var staticCacheName = 'uni-library-v2';

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
            return cache.addAll([
                '/',
                '/dashboard/',
                '/guest/',
                '/static/css/style.css',
                '/static/images/icon-160.png',
                'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
                'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
    var requestUrl = new URL(event.request.url);
    if (requestUrl.origin === location.origin) {
        if ((requestUrl.pathname === '/')) {
            event.respondWith(caches.match('/'));
            return;
        }
    }
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});
