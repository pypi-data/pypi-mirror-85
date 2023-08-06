function createLocalStorage() {
    var localStorage = window.localStorage;
    try {
        var mod = 'sentry';
        localStorage.setItem(mod, mod);
        localStorage.removeItem(mod);
        return {
            setItem: localStorage.setItem.bind(localStorage),
            getItem: localStorage.getItem.bind(localStorage),
            removeItem: localStorage.removeItem.bind(localStorage),
        };
    }
    catch (e) {
        return {
            setItem: function () {
                return;
            },
            // Returns null if key doesn't exist:
            // https://developer.mozilla.org/en-US/docs/Web/API/Storage/getItem
            getItem: function () {
                return null;
            },
            removeItem: function () {
                return null;
            },
        };
    }
}
var functions = createLocalStorage();
export default functions;
//# sourceMappingURL=localStorage.jsx.map