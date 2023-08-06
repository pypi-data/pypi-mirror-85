import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import Confirm from 'app/components/confirm';
var ActionLink = /** @class */ (function (_super) {
    __extends(ActionLink, _super);
    function ActionLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ActionLink.prototype.render = function () {
        var _a = this.props, shouldConfirm = _a.shouldConfirm, message = _a.message, className = _a.className, title = _a.title, onAction = _a.onAction, confirmLabel = _a.confirmLabel, disabled = _a.disabled, children = _a.children;
        var testId = title
            ? 'action-link-' + title.toLowerCase().replace(/ /g, '-')
            : 'action-link';
        if (shouldConfirm && !disabled) {
            return (<Confirm message={message} confirmText={confirmLabel} onConfirm={onAction}>
          <a className={className} title={title} aria-label={title}>
            {' '}
            {children}
          </a>
        </Confirm>);
        }
        else {
            return (<ActionLinkAnchor data-test-id={testId} aria-label={title} className={classNames(className, { disabled: disabled })} onClick={disabled ? undefined : onAction} disabled={disabled}>
          {children}
        </ActionLinkAnchor>);
        }
    };
    ActionLink.propTypes = {
        className: PropTypes.any,
        title: PropTypes.string,
        message: PropTypes.node,
        disabled: PropTypes.bool,
        onAction: PropTypes.func.isRequired,
        shouldConfirm: PropTypes.bool,
        confirmLabel: PropTypes.string,
    };
    ActionLink.defaultProps = {
        shouldConfirm: false,
        disabled: false,
    };
    return ActionLink;
}(React.Component));
export default ActionLink;
var ActionLinkAnchor = styled('a')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  pointer-events: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  pointer-events: ", ";\n"])), function (p) { return (p.disabled ? 'none' : 'auto'); });
var templateObject_1;
//# sourceMappingURL=actionLink.jsx.map