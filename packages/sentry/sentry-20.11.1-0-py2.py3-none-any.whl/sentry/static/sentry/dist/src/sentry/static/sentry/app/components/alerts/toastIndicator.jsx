import { __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import classNames from 'classnames';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { t } from 'app/locale';
import { IconCheckmark, IconClose } from 'app/icons';
import LoadingIndicator from 'app/components/loadingIndicator';
import testableTransition from 'app/utils/testableTransition';
import space from 'app/styles/space';
var Toast = styled(motion.div)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  padding: 0 15px 0 10px;\n  margin-top: 15px;\n  background: ", ";\n  color: #fff;\n  border-radius: 44px 7px 7px 44px;\n  box-shadow: 0 4px 12px 0 rgba(47, 40, 55, 0.16);\n  position: relative;\n"], ["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  padding: 0 15px 0 10px;\n  margin-top: 15px;\n  background: ", ";\n  color: #fff;\n  border-radius: 44px 7px 7px 44px;\n  box-shadow: 0 4px 12px 0 rgba(47, 40, 55, 0.16);\n  position: relative;\n"])), function (p) { return p.theme.gray500; });
Toast.defaultProps = {
    initial: {
        opacity: 0,
        y: 70,
    },
    animate: {
        opacity: 1,
        y: 0,
    },
    exit: {
        opacity: 0,
        y: 70,
    },
    transition: testableTransition({
        type: 'spring',
        stiffness: 450,
        damping: 25,
    }),
};
var Icon = styled('div', { shouldForwardProp: function (p) { return p !== 'type'; } })(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n  svg {\n    display: block;\n  }\n\n  color: ", ";\n"], ["\n  margin-right: ", ";\n  svg {\n    display: block;\n  }\n\n  color: ", ";\n"])), space(0.75), function (p) { return (p.type === 'success' ? p.theme.green300 : p.theme.red300); });
var Message = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var Undo = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: inline-block;\n  color: ", ";\n  padding-left: ", ";\n  margin-left: ", ";\n  border-left: 1px solid ", ";\n  cursor: pointer;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  display: inline-block;\n  color: ", ";\n  padding-left: ", ";\n  margin-left: ", ";\n  border-left: 1px solid ", ";\n  cursor: pointer;\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, space(2), space(2), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; });
var StyledLoadingIndicator = styled(LoadingIndicator)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  .loading-indicator {\n    border-color: ", ";\n    border-left-color: ", ";\n  }\n"], ["\n  .loading-indicator {\n    border-color: ", ";\n    border-left-color: ", ";\n  }\n"])), function (p) { return p.theme.gray500; }, function (p) { return p.theme.purple300; });
function ToastIndicator(_a) {
    var indicator = _a.indicator, onDismiss = _a.onDismiss, className = _a.className, props = __rest(_a, ["indicator", "onDismiss", "className"]);
    var icon;
    var options = indicator.options, message = indicator.message, type = indicator.type;
    var _b = options || {}, undo = _b.undo, disableDismiss = _b.disableDismiss;
    var showUndo = typeof undo === 'function';
    var handleClick = function (e) {
        if (disableDismiss) {
            return;
        }
        if (typeof onDismiss === 'function') {
            onDismiss(indicator, e);
        }
    };
    if (type === 'success') {
        icon = <IconCheckmark size="lg" isCircled/>;
    }
    else if (type === 'error') {
        icon = <IconClose size="lg" isCircled/>;
    }
    // TODO(billy): Remove ref- className after removing usage from getsentry
    return (<Toast onClick={handleClick} data-test-id={type ? "toast-" + type : 'toast'} className={classNames(className, 'ref-toast', "ref-" + type)} {...props}>
      {type === 'loading' ? (<StyledLoadingIndicator mini/>) : (<Icon type={type}>{icon}</Icon>)}
      <Message>{message}</Message>
      {showUndo && <Undo onClick={undo}>{t('Undo')}</Undo>}
    </Toast>);
}
ToastIndicator.propTypes = {
    indicator: PropTypes.shape({
        type: PropTypes.oneOf(['error', 'success', 'loading', 'undo', '']),
        id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        message: PropTypes.node,
        options: PropTypes.object,
    }),
    onDismiss: PropTypes.func,
};
export default ToastIndicator;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=toastIndicator.jsx.map