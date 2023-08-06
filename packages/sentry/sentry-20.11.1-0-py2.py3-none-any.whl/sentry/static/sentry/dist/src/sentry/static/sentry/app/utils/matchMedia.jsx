import { NODE_ENV } from 'app/constants';
function changeFavicon(theme) {
    // only on prod because we have a development favicon
    if (NODE_ENV !== 'production') {
        return;
    }
    var n = document.querySelector('[rel="icon"][type="image/png"]');
    if (!n) {
        return;
    }
    var path = n.href.split('/sentry/')[0];
    n.href = path + "/sentry/images/" + (theme === 'dark' ? 'favicon-dark' : 'favicon') + ".png";
}
function handleColorSchemeChange(e) {
    var isDark = e.media === '(prefers-color-scheme: dark)' && e.matches;
    var type = isDark ? 'dark' : 'light';
    changeFavicon(type);
    // TODO(dark): For now, you must opt into dark mode using command palette
    // ConfigStore.set('theme', type);
}
export function prefersDark() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}
export function setupColorScheme() {
    // Set favicon to dark on load if necessary)
    if (prefersDark()) {
        changeFavicon('dark');
        // TODO(dark): (currently manual opt in only): ConfigStore.set('theme', 'dark');
    }
    // Watch for changes in preferred color scheme
    var lightMediaQuery = window.matchMedia('(prefers-color-scheme: light)');
    var darkMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    try {
        lightMediaQuery.addEventListener('change', handleColorSchemeChange);
        darkMediaQuery.addEventListener('change', handleColorSchemeChange);
    }
    catch (err) {
        // Safari 13 (maybe lower too) does not support `addEventListener`
        // `addListener` is deprecated
        lightMediaQuery.addListener(handleColorSchemeChange);
        darkMediaQuery.addListener(handleColorSchemeChange);
    }
}
//# sourceMappingURL=matchMedia.jsx.map