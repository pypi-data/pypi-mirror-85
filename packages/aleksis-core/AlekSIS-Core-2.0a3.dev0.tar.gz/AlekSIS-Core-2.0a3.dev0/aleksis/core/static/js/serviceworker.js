// This is the AlekSIS service worker

const CACHE = "aleksis-cache";

const precacheFiles = [
    '',
];

const offlineFallbackPage = '/offline';

const avoidCachingPaths = [
    '/admin',
    '/settings',
    '/accounts/login'
]; // TODO: More paths are needed

function pathComparer(requestUrl, pathRegEx) {
    return requestUrl.match(new RegExp(pathRegEx));
}

function comparePaths(requestUrl, pathsArray) {
    if (requestUrl) {
        for (let index = 0; index < pathsArray.length; index++) {
            const pathRegEx = pathsArray[index];
            if (pathComparer(requestUrl, pathRegEx)) {
                return true;
            }
        }
    }

    return false;
}

self.addEventListener("install", function (event) {
    console.log("[AlekSIS PWA] Install Event processing.");

    console.log("[AlekSIS PWA] Skipping waiting on install.");
    self.skipWaiting();

    event.waitUntil(
        caches.open(CACHE).then(function (cache) {
            console.log("[AlekSIS PWA] Caching pages during install.");

            return cache.addAll(precacheFiles).then(function () {
                return cache.add(offlineFallbackPage);
            });
        })
    );
});

// Allow sw to control of current page
self.addEventListener("activate", function (event) {
    console.log("[AlekSIS PWA] Claiming clients for current page.");
    event.waitUntil(self.clients.claim());
});

// If any fetch fails, it will look for the request in the cache and serve it from there first
self.addEventListener("fetch", function (event) {
    if (event.request.method !== "GET") return;
    networkFirstFetch(event);
});

function networkFirstFetch(event) {
    event.respondWith(
        fetch(event.request)
            .then(function (response) {
                // If request was successful, add or update it in the cache
                console.log("[AlekSIS PWA] Network request successful.");
                event.waitUntil(updateCache(event.request, response.clone()));
                return response;
            })
            .catch(function (error) {
                console.log("[AlekSIS PWA] Network request failed. Serving content from cache: " + error);
                return fromCache(event);
            })
    );
}

function fromCache(event) {
    // Check to see if you have it in the cache
    // Return response
    // If not in the cache, then return offline fallback page
    return caches.open(CACHE).then(function (cache) {
        return cache.match(event.request)
            .then(function (matching) {
                if (!matching || matching.status === 404) {
                    console.log("[AlekSIS PWA] Cache request failed. Serving offline fallback page.");
                    // Use the precached offline page as fallback
                    return caches.match(offlineFallbackPage)
                }

                return matching;
            });
    });
}

function updateCache(request, response) {
    if (!comparePaths(request.url, avoidCachingPaths)) {
        return caches.open(CACHE).then(function (cache) {
            return cache.put(request, response);
        });
    }

    return Promise.resolve();
}
