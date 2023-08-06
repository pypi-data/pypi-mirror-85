import { __extends, __makeTemplateObject } from "tslib";
import { ClassNames } from '@emotion/core';
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import capitalize from 'lodash/capitalize';
import { IconAdd, IconClose } from 'app/icons';
import space from 'app/styles/space';
import Hovercard from 'app/components/hovercard';
import { callIfFunction } from 'app/utils/callIfFunction';
import { getIntegrationIcon } from 'app/utils/integrationUtil';
var IssueSyncListElement = /** @class */ (function (_super) {
    __extends(IssueSyncListElement, _super);
    function IssueSyncListElement() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hoverCardRef = React.createRef();
        _this.handleDelete = function () {
            callIfFunction(_this.props.onClose, _this.props.externalIssueId);
        };
        _this.handleIconClick = function () {
            if (_this.isLinked()) {
                _this.handleDelete();
            }
            else if (_this.props.onOpen) {
                _this.props.onOpen();
            }
        };
        return _this;
    }
    IssueSyncListElement.prototype.componentDidUpdate = function (nextProps) {
        if (this.props.showHoverCard !== nextProps.showHoverCard &&
            nextProps.showHoverCard === undefined) {
            this.hoverCardRef.current && this.hoverCardRef.current.handleToggleOff();
        }
    };
    IssueSyncListElement.prototype.isLinked = function () {
        return !!(this.props.externalIssueLink && this.props.externalIssueId);
    };
    IssueSyncListElement.prototype.getIcon = function () {
        return getIntegrationIcon(this.props.integrationType);
    };
    IssueSyncListElement.prototype.getPrettyName = function () {
        var type = this.props.integrationType;
        switch (type) {
            case 'gitlab':
                return 'GitLab';
            case 'github':
                return 'GitHub';
            case 'github_enterprise':
                return 'GitHub Enterprise';
            case 'vsts':
                return 'Azure DevOps';
            case 'jira_server':
                return 'Jira Server';
            default:
                return capitalize(type);
        }
    };
    IssueSyncListElement.prototype.getLink = function () {
        return (<IntegrationLink href={this.props.externalIssueLink || undefined} onClick={!this.isLinked() ? this.props.onOpen : undefined}>
        {this.getText()}
      </IntegrationLink>);
    };
    IssueSyncListElement.prototype.getText = function () {
        if (this.props.children) {
            return this.props.children;
        }
        if (this.props.externalIssueDisplayName) {
            return this.props.externalIssueDisplayName;
        }
        if (this.props.externalIssueKey) {
            return this.props.externalIssueKey;
        }
        return "Link " + this.getPrettyName() + " Issue";
    };
    IssueSyncListElement.prototype.render = function () {
        var _this = this;
        return (<IssueSyncListElementContainer>
        <ClassNames>
          {function (_a) {
            var css = _a.css;
            return (<Hovercard ref={_this.hoverCardRef} containerClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                display: flex;\n                align-items: center;\n                min-width: 0; /* flex-box overflow workaround */\n              "], ["\n                display: flex;\n                align-items: center;\n                min-width: 0; /* flex-box overflow workaround */\n              "])))} header={_this.props.hoverCardHeader} body={_this.props.hoverCardBody} bodyClassName="issue-list-body" show={_this.props.showHoverCard}>
              {_this.getIcon()}
              {_this.getLink()}
            </Hovercard>);
        }}
        </ClassNames>
        {(this.props.onClose || this.props.onOpen) && (<StyledIcon onClick={this.handleIconClick}>
            {this.isLinked() ? <IconClose /> : this.props.onOpen ? <IconAdd /> : null}
          </StyledIcon>)}
      </IssueSyncListElementContainer>);
    };
    IssueSyncListElement.propTypes = {
        externalIssueLink: PropTypes.string,
        externalIssueId: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
        externalIssueKey: PropTypes.string,
        externalIssueDisplayName: PropTypes.string,
        onOpen: PropTypes.func,
        onClose: PropTypes.func,
        integrationType: PropTypes.string,
        hoverCardHeader: PropTypes.node,
        hoverCardBody: PropTypes.node,
    };
    return IssueSyncListElement;
}(React.Component));
export var IssueSyncListElementContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"], ["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n\n  &:not(:last-child) {\n    margin-bottom: ", ";\n  }\n"])), space(2));
export var IntegrationLink = styled('a')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-decoration: none;\n  padding-bottom: ", ";\n  margin-left: ", ";\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  cursor: pointer;\n  line-height: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n\n  &,\n  &:hover {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  text-decoration: none;\n  padding-bottom: ", ";\n  margin-left: ", ";\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  cursor: pointer;\n  line-height: 1;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n\n  &,\n  &:hover {\n    border-bottom: 1px solid ", ";\n  }\n"])), space(0.25), space(1), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.blue300; });
var StyledIcon = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n"], ["\n  color: ", ";\n  cursor: pointer;\n"])), function (p) { return p.theme.textColor; });
export default IssueSyncListElement;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=issueSyncListElement.jsx.map