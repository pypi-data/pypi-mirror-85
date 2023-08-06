var MAX_TOOLTIPS_TO_OPEN = 100;
var TooltipStore = {
    tooltips: [],
    getOpenableSingleTooltips: function () {
        return this.tooltips.filter(function (tooltip) {
            // Filtering out disabled tooltips and lists of tooltips (which cause rendering issues for snapshots) using the internal 'key'
            var _internals = tooltip._reactInternalFiber || tooltip._reactInternals;
            return (!tooltip.props.disabled &&
                !_internals.key &&
                !tooltip.props.disableForVisualTest);
        });
    },
    /**
     * Called via window.__openAllTooltips in selenium tests to check tooltip snapshots
     */
    openAllTooltips: function () {
        var tooltips = this.getOpenableSingleTooltips();
        if (!tooltips.length || tooltips.length > MAX_TOOLTIPS_TO_OPEN) {
            // Pages with too many tooltip components will take too long to render and it isn't likely helpful anyway.
            return false;
        }
        tooltips.forEach(function (tooltip) {
            tooltip.setState({
                isOpen: true,
                usesGlobalPortal: false,
            });
        });
        return true;
    },
    /**
     * Called via window.__closeAllTooltips in selenium tests to cleanup tooltips after taking a snapshot
     */
    closeAllTooltips: function () {
        var tooltips = this.getOpenableSingleTooltips();
        tooltips.forEach(function (tooltip) {
            tooltip.setState({
                isOpen: false,
                usesGlobalPortal: true,
            });
        });
    },
    init: function () {
        window.__openAllTooltips = this.openAllTooltips.bind(this);
        window.__closeAllTooltips = this.closeAllTooltips.bind(this);
        return this;
    },
    addTooltip: function (tooltip) {
        this.tooltips.push(tooltip);
    },
    removeTooltip: function (tooltip) {
        this.tooltips = this.tooltips.filter(function (t) { return t !== tooltip; });
    },
};
export default TooltipStore.init();
//# sourceMappingURL=tooltipStore.jsx.map