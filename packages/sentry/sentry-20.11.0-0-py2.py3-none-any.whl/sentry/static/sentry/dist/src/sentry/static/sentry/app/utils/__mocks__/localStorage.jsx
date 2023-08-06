var localStorageMock = function () {
    var store = {};
    return {
        getItem: jest.fn(function (key) { return store[key]; }),
        setItem: jest.fn(function (key, value) {
            store[key] = value.toString();
        }),
        clear: jest.fn(function () {
            store = {};
        }),
    };
};
export default localStorageMock();
//# sourceMappingURL=localStorage.jsx.map