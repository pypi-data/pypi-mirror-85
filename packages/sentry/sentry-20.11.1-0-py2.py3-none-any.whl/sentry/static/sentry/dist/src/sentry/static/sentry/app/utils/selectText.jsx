export function selectText(node) {
    if (node instanceof HTMLInputElement && node.type === 'text') {
        node.select();
    }
    else if (node instanceof Node && window.getSelection) {
        var range = document.createRange();
        range.selectNode(node);
        var selection = window.getSelection();
        if (selection) {
            selection.removeAllRanges();
            selection.addRange(range);
        }
    }
}
//# sourceMappingURL=selectText.jsx.map