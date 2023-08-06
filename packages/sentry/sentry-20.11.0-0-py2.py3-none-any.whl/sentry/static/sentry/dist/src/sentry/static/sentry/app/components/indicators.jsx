import { __extends, __makeTemplateObject, __rest } from "tslib";
import { AnimatePresence } from 'framer-motion';
import { ThemeProvider } from 'emotion-theming';
import PropTypes from 'prop-types';
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import styled from '@emotion/styled';
import { removeIndicator } from 'app/actionCreators/indicator';
import IndicatorStore from 'app/stores/indicatorStore';
import ToastIndicator from 'app/components/alerts/toastIndicator';
import theme from 'app/utils/theme';
var Toasts = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: fixed;\n  right: 30px;\n  bottom: 30px;\n  z-index: ", ";\n"], ["\n  position: fixed;\n  right: 30px;\n  bottom: 30px;\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.toast; });
var Indicators = /** @class */ (function (_super) {
    __extends(Indicators, _super);
    function Indicators() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDismiss = function (indicator) {
            removeIndicator(indicator);
        };
        return _this;
    }
    Indicators.prototype.render = function () {
        var _this = this;
        var _a = this.props, items = _a.items, props = __rest(_a, ["items"]);
        return (<Toasts {...props}>
        <AnimatePresence>
          {items.map(function (indicator, i) { return (
        // We purposefully use `i` as key here because of transitions
        // Toasts can now queue up, so when we change from [firstToast] -> [secondToast],
        // we don't want to  animate `firstToast` out and `secondToast` in, rather we want
        // to replace `firstToast` with `secondToast`
        <ToastIndicator onDismiss={_this.handleDismiss} indicator={indicator} key={i}/>); })}
        </AnimatePresence>
      </Toasts>);
    };
    Indicators.propTypes = {
        className: PropTypes.string,
        items: PropTypes.arrayOf(PropTypes.shape({
            type: PropTypes.oneOf(['error', 'success', 'loading', 'undo', '']),
            id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
            message: PropTypes.node,
            options: PropTypes.object,
        })),
    };
    Indicators.defaultProps = {
        items: [],
    };
    return Indicators;
}(React.Component));
var IndicatorsContainer = createReactClass({
    displayName: 'IndicatorsContainer',
    mixins: [Reflux.connect(IndicatorStore, 'items')],
    getInitialState: function () {
        return {
            items: [],
        };
    },
    render: function () {
        // #NEW-SETTINGS - remove ThemeProvider here once new settings is merged
        // `alerts.html` django view includes this container and doesn't have a theme provider
        // not even sure it is used in django views but this is just an easier temp solution
        return (<ThemeProvider theme={theme}>
        <Indicators {...this.props} items={this.state.items}/>
      </ThemeProvider>);
    },
});
export default IndicatorsContainer;
export { Indicators };
var templateObject_1;
//# sourceMappingURL=indicators.jsx.map