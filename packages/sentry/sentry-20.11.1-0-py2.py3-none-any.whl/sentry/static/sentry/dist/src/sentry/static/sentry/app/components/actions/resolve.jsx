import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { IconCheckmark } from 'app/icons';
import CustomResolutionModal from 'app/components/customResolutionModal';
import MenuItem from 'app/components/menuItem';
import DropdownLink from 'app/components/dropdownLink';
import ActionLink from 'app/components/actions/actionLink';
import Tooltip from 'app/components/tooltip';
import { formatVersion } from 'app/utils/formatters';
import space from 'app/styles/space';
import { ResolutionStatus, } from 'app/types';
var defaultProps = {
    isResolved: false,
    isAutoResolved: false,
    confirmLabel: t('Resolve'),
};
var ResolveActions = /** @class */ (function (_super) {
    __extends(ResolveActions, _super);
    function ResolveActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { modal: false };
        return _this;
    }
    ResolveActions.prototype.onCustomResolution = function (statusDetails) {
        this.setState({
            modal: false,
        });
        this.props.onUpdate({
            status: ResolutionStatus.RESOLVED,
            statusDetails: statusDetails,
        });
    };
    ResolveActions.prototype.getButtonClass = function (otherClasses) {
        return classNames('btn btn-default btn-sm', otherClasses);
    };
    ResolveActions.prototype.renderResolved = function () {
        var _a = this.props, isAutoResolved = _a.isAutoResolved, onUpdate = _a.onUpdate;
        if (isAutoResolved) {
            return (<div className="btn-group">
          <Tooltip title={t('This event is resolved due to the Auto Resolve configuration for this project')}>
            <a className={this.getButtonClass('active')}>
              <IconCheckmark size="xs"/>
            </a>
          </Tooltip>
        </div>);
        }
        else {
            return (<div className="btn-group">
          <Tooltip title={t('Unresolve')}>
            <a data-test-id="button-unresolve" className={this.getButtonClass('active')} onClick={function () { return onUpdate({ status: ResolutionStatus.UNRESOLVED }); }}>
              <IconCheckmark size="xs"/>
            </a>
          </Tooltip>
        </div>);
        }
    };
    ResolveActions.prototype.render = function () {
        var _this = this;
        var _a = this.props, isResolved = _a.isResolved, hasRelease = _a.hasRelease, latestRelease = _a.latestRelease, onUpdate = _a.onUpdate, orgId = _a.orgId, projectId = _a.projectId, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, disableDropdown = _a.disableDropdown, projectFetchError = _a.projectFetchError;
        var buttonClass = this.getButtonClass();
        if (isResolved) {
            return this.renderResolved();
        }
        var actionTitle = !hasRelease
            ? t('Set up release tracking in order to use this feature.')
            : '';
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled,
        };
        return (<div style={{ display: 'inline-block' }}>
        <CustomResolutionModal show={this.state.modal} onSelected={function (statusDetails) {
            return _this.onCustomResolution(statusDetails);
        }} onCanceled={function () { return _this.setState({ modal: false }); }} orgId={orgId} projectId={projectId}/>
        <Tooltip disabled={!projectFetchError} title={t('Error fetching project')}>
          <div className="btn-group">
            <StyledActionLink {...actionLinkProps} title={t('Resolve')} className={buttonClass} onAction={function () { return onUpdate({ status: ResolutionStatus.RESOLVED }); }}>
              <StyledIconCheckmark size="xs"/>
              {t('Resolve')}
            </StyledActionLink>

            <StyledDropdownLink key="resolve-dropdown" caret className={buttonClass} title="" alwaysRenderMenu disabled={disableDropdown || disabled}>
              <MenuItem header>{t('Resolved In')}</MenuItem>
              <MenuItem noAnchor>
                <Tooltip title={actionTitle} containerDisplayMode="block">
                  <ActionLink {...actionLinkProps} title={t('The next release')} onAction={function () {
            return hasRelease &&
                onUpdate({
                    status: ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inNextRelease: true,
                    },
                });
        }}>
                    {t('The next release')}
                  </ActionLink>
                </Tooltip>
                <Tooltip title={actionTitle} containerDisplayMode="block">
                  <ActionLink {...actionLinkProps} title={t('The current release')} onAction={function () {
            return hasRelease &&
                onUpdate({
                    status: ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inRelease: latestRelease ? latestRelease.version : 'latest',
                    },
                });
        }}>
                    {latestRelease
            ? t('The current release (%s)', formatVersion(latestRelease.version))
            : t('The current release')}
                  </ActionLink>
                </Tooltip>
                <Tooltip title={actionTitle} containerDisplayMode="block">
                  <ActionLink {...actionLinkProps} title={t('Another version')} onAction={function () { return hasRelease && _this.setState({ modal: true }); }} shouldConfirm={false}>
                    {t('Another version\u2026')}
                  </ActionLink>
                </Tooltip>
              </MenuItem>
            </StyledDropdownLink>
          </div>
        </Tooltip>
      </div>);
    };
    ResolveActions.propTypes = {
        hasRelease: PropTypes.bool.isRequired,
        latestRelease: PropTypes.object,
        onUpdate: PropTypes.func.isRequired,
        orgId: PropTypes.string.isRequired,
        projectId: PropTypes.string,
        shouldConfirm: PropTypes.bool,
        confirmMessage: PropTypes.node,
        disabled: PropTypes.bool,
        disableDropdown: PropTypes.bool,
        isResolved: PropTypes.bool,
        isAutoResolved: PropTypes.bool,
        confirmLabel: PropTypes.string,
        projectFetchError: PropTypes.bool,
    };
    ResolveActions.defaultProps = defaultProps;
    return ResolveActions;
}(React.Component));
var StyledIconCheckmark = styled(IconCheckmark)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  margin-right: ", ";\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), space(0.5), function (p) { return p.theme.breakpoints[0]; });
var StyledActionLink = styled(ActionLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n"])));
var StyledDropdownLink = styled(DropdownLink)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  transition: none;\n"], ["\n  transition: none;\n"])));
export default ResolveActions;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=resolve.jsx.map