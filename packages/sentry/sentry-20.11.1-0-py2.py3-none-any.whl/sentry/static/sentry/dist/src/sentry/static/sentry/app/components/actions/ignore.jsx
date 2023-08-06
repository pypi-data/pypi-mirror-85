import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import styled from '@emotion/styled';
import { IconNot } from 'app/icons';
import { ResolutionStatus, } from 'app/types';
import { t, tn } from 'app/locale';
import MenuItem from 'app/components/menuItem';
import DropdownLink from 'app/components/dropdownLink';
import Duration from 'app/components/duration';
import CustomIgnoreCountModal from 'app/components/customIgnoreCountModal';
import CustomIgnoreDurationModal from 'app/components/customIgnoreDurationModal';
import ActionLink from 'app/components/actions/actionLink';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
var ModalStates;
(function (ModalStates) {
    ModalStates[ModalStates["COUNT"] = 0] = "COUNT";
    ModalStates[ModalStates["DURATION"] = 1] = "DURATION";
    ModalStates[ModalStates["USERS"] = 2] = "USERS";
})(ModalStates || (ModalStates = {}));
var IGNORE_DURATIONS = [30, 120, 360, 60 * 24, 60 * 24 * 7];
var IGNORE_COUNTS = [1, 10, 100, 1000, 10000, 100000];
var IGNORE_WINDOWS = [
    [60, t('per hour')],
    [24 * 60, t('per day')],
    [24 * 7 * 60, t('per week')],
];
var defaultProps = {
    isIgnored: false,
    confirmLabel: t('Ignore'),
};
var IgnoreActions = /** @class */ (function (_super) {
    __extends(IgnoreActions, _super);
    function IgnoreActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            modal: null,
        };
        return _this;
    }
    IgnoreActions.prototype.onCustomIgnore = function (statusDetails) {
        this.setState({
            modal: null,
        });
        this.onIgnore(statusDetails);
    };
    IgnoreActions.prototype.onIgnore = function (statusDetails) {
        return this.props.onUpdate({
            status: ResolutionStatus.IGNORED,
            statusDetails: statusDetails || {},
        });
    };
    IgnoreActions.prototype.render = function () {
        var _this = this;
        var _a = this.props, isIgnored = _a.isIgnored, onUpdate = _a.onUpdate, disabled = _a.disabled, shouldConfirm = _a.shouldConfirm, confirmMessage = _a.confirmMessage, confirmLabel = _a.confirmLabel;
        var linkClassName = classNames('btn btn-default btn-sm', {
            active: isIgnored,
        });
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            title: t('Ignore'),
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled,
        };
        if (isIgnored) {
            return (<div className="btn-group">
          <Tooltip title={t('Change status to unresolved')}>
            <a className={linkClassName} data-test-id="button-unresolve" onClick={function () { return onUpdate({ status: ResolutionStatus.UNRESOLVED }); }}>
              <SoloIconNot size="xs"/>
            </a>
          </Tooltip>
        </div>);
        }
        return (<div style={{ display: 'inline-block' }}>
        <CustomIgnoreDurationModal show={this.state.modal === ModalStates.DURATION} onSelected={function (details) { return _this.onCustomIgnore(details); }} onCanceled={function () { return _this.setState({ modal: null }); }}/>
        <CustomIgnoreCountModal show={this.state.modal === ModalStates.COUNT} onSelected={function (details) { return _this.onCustomIgnore(details); }} onCanceled={function () { return _this.setState({ modal: null }); }} label={t('Ignore this issue until it occurs again\u2026')} countLabel={t('Number of times')} countName="ignoreCount" windowName="ignoreWindow" windowChoices={IGNORE_WINDOWS}/>
        <CustomIgnoreCountModal show={this.state.modal === ModalStates.USERS} onSelected={function (details) { return _this.onCustomIgnore(details); }} onCanceled={function () { return _this.setState({ modal: null }); }} label={t('Ignore this issue until it affects an additional\u2026')} countLabel={t('Number of users')} countName="ignoreUserCount" windowName="ignoreUserWindow" windowChoices={IGNORE_WINDOWS}/>
        <div className="btn-group">
          <StyledActionLink {...actionLinkProps} title={t('Ignore')} className={linkClassName} onAction={function () { return onUpdate({ status: ResolutionStatus.IGNORED }); }}>
            <StyledIconNot size="xs"/>
            {t('Ignore')}
          </StyledActionLink>

          <StyledDropdownLink caret className={linkClassName} title="" alwaysRenderMenu disabled={disabled}>
            <MenuItem header>Ignore</MenuItem>
            <li className="dropdown-submenu">
              <DropdownLink title={t('For\u2026')} caret={false} isNestedDropdown alwaysRenderMenu>
                {IGNORE_DURATIONS.map(function (duration) { return (<MenuItem noAnchor key={duration}>
                    <ActionLink {...actionLinkProps} onAction={function () { return _this.onIgnore({ ignoreDuration: duration }); }}>
                      <Duration seconds={duration * 60}/>
                    </ActionLink>
                  </MenuItem>); })}
                <MenuItem divider/>
                <MenuItem noAnchor>
                  <a onClick={function () { return _this.setState({ modal: ModalStates.DURATION }); }}>
                    {t('Custom')}
                  </a>
                </MenuItem>
              </DropdownLink>
            </li>
            <li className="dropdown-submenu">
              <DropdownLink title={t('Until this occurs again\u2026')} caret={false} isNestedDropdown alwaysRenderMenu>
                {IGNORE_COUNTS.map(function (count) { return (<li className="dropdown-submenu" key={count}>
                    <DropdownLink title={count === 1
            ? t('one time\u2026') // This is intentional as unbalanced string formatters are problematic
            : tn('%s time\u2026', '%s times\u2026', count)} caret={false} isNestedDropdown alwaysRenderMenu>
                      <MenuItem noAnchor>
                        <ActionLink {...actionLinkProps} onAction={function () { return _this.onIgnore({ ignoreCount: count }); }}>
                          {t('from now')}
                        </ActionLink>
                      </MenuItem>
                      {IGNORE_WINDOWS.map(function (_a) {
            var _b = __read(_a, 2), hours = _b[0], label = _b[1];
            return (<MenuItem noAnchor key={hours}>
                          <ActionLink {...actionLinkProps} onAction={function () {
                return _this.onIgnore({
                    ignoreCount: count,
                    ignoreWindow: hours,
                });
            }}>
                            {label}
                          </ActionLink>
                        </MenuItem>);
        })}
                    </DropdownLink>
                  </li>); })}
                <MenuItem divider/>
                <MenuItem noAnchor>
                  <a onClick={function () { return _this.setState({ modal: ModalStates.COUNT }); }}>
                    {t('Custom')}
                  </a>
                </MenuItem>
              </DropdownLink>
            </li>
            <li className="dropdown-submenu">
              <DropdownLink title={t('Until this affects an additional\u2026')} caret={false} isNestedDropdown alwaysRenderMenu>
                {IGNORE_COUNTS.map(function (count) { return (<li className="dropdown-submenu" key={count}>
                    <DropdownLink title={tn('one user\u2026', '%s users\u2026', count)} caret={false} isNestedDropdown alwaysRenderMenu>
                      <MenuItem noAnchor>
                        <ActionLink {...actionLinkProps} onAction={function () { return _this.onIgnore({ ignoreUserCount: count }); }}>
                          {t('from now')}
                        </ActionLink>
                      </MenuItem>
                      {IGNORE_WINDOWS.map(function (_a) {
            var _b = __read(_a, 2), hours = _b[0], label = _b[1];
            return (<MenuItem noAnchor key={hours}>
                          <ActionLink {...actionLinkProps} onAction={function () {
                return _this.onIgnore({
                    ignoreUserCount: count,
                    ignoreUserWindow: hours,
                });
            }}>
                            {label}
                          </ActionLink>
                        </MenuItem>);
        })}
                    </DropdownLink>
                  </li>); })}
                <MenuItem divider/>
                <MenuItem noAnchor>
                  <a onClick={function () { return _this.setState({ modal: ModalStates.USERS }); }}>
                    {t('Custom')}
                  </a>
                </MenuItem>
              </DropdownLink>
            </li>
          </StyledDropdownLink>
        </div>
      </div>);
    };
    IgnoreActions.propTypes = {
        isIgnored: PropTypes.bool,
        onUpdate: PropTypes.func.isRequired,
        disabled: PropTypes.bool,
        shouldConfirm: PropTypes.bool,
        confirmMessage: PropTypes.node,
        confirmLabel: PropTypes.string,
    };
    IgnoreActions.defaultProps = defaultProps;
    return IgnoreActions;
}(React.Component));
export default IgnoreActions;
var StyledIconNot = styled(IconNot)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  margin-right: ", ";\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), space(0.5), function (p) { return p.theme.breakpoints[0]; });
// The icon with no text label needs positioning tweaks
// inside the bootstrap button. Hopefully this can be removed
// bootstrap buttons are converted.
var SoloIconNot = styled(IconNot)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var StyledActionLink = styled(ActionLink)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n"])));
var StyledDropdownLink = styled(DropdownLink)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  transition: none;\n"], ["\n  transition: none;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=ignore.jsx.map