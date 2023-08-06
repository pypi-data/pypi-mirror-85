/**
 * Converts arg from a `select2` choices array to a `react-select` `options` array
 */
var convertFromSelect2Choices = function (choices) {
    // TODO(ts): This is to make sure that this function is backwards compatible, ideally,
    // this function only accepts arrays
    if (!Array.isArray(choices)) {
        return null;
    }
    // Accepts an array of strings or an array of tuples
    return choices.map(function (choice) {
        return Array.isArray(choice)
            ? { value: choice[0], label: choice[1] }
            : { value: choice, label: choice };
    });
};
export default convertFromSelect2Choices;
//# sourceMappingURL=convertFromSelect2Choices.jsx.map