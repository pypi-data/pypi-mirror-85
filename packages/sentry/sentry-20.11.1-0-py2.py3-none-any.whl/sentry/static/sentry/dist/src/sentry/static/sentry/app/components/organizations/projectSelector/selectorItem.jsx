import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { t } from 'app/locale';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import { analytics } from 'app/utils/analytics';
import { alertHighlight, pulse } from 'app/styles/animations';
import BookmarkStar from 'app/components/projects/bookmarkStar';
import GlobalSelectionHeaderRow from 'app/components/globalSelectionHeaderRow';
import Highlight from 'app/components/highlight';
import IdBadge from 'app/components/idBadge';
import space from 'app/styles/space';
import { IconSettings } from 'app/icons';
import Link from 'app/components/links/link';
import Hovercard from 'app/components/hovercard';
var defaultProps = {
    multi: false,
    inputValue: '',
    isChecked: false,
};
var ProjectSelectorItem = /** @class */ (function (_super) {
    __extends(ProjectSelectorItem, _super);
    function ProjectSelectorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            bookmarkHasChanged: false,
        };
        _this.handleClick = function (event) {
            var _a = _this.props, project = _a.project, onMultiSelect = _a.onMultiSelect;
            event.stopPropagation();
            if (onMultiSelect) {
                onMultiSelect(project, event);
            }
        };
        _this.handleBookmarkToggle = function (isBookmarked) {
            var organization = _this.props.organization;
            analytics('projectselector.bookmark_toggle', {
                org_id: parseInt(organization.id, 10),
                bookmarked: isBookmarked,
            });
        };
        _this.clearAnimation = function () {
            _this.setState({ bookmarkHasChanged: false });
        };
        return _this;
    }
    ProjectSelectorItem.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.project.isBookmarked !== this.props.project.isBookmarked) {
            this.setBookmarkHasChanged();
        }
    };
    ProjectSelectorItem.prototype.setBookmarkHasChanged = function () {
        this.setState({ bookmarkHasChanged: true });
    };
    ProjectSelectorItem.prototype.renderDisabledCheckbox = function (_a) {
        var children = _a.children, features = _a.features;
        return (<Hovercard body={<FeatureDisabled features={features} hideHelpToggle message={t('Multiple project selection disabled')} featureName={t('Multiple Project Selection')}/>}>
        {children}
      </Hovercard>);
    };
    ProjectSelectorItem.prototype.render = function () {
        var _this = this;
        var _a = this.props, project = _a.project, multi = _a.multi, inputValue = _a.inputValue, isChecked = _a.isChecked, organization = _a.organization;
        var bookmarkHasChanged = this.state.bookmarkHasChanged;
        return (<BadgeAndActionsWrapper bookmarkHasChanged={bookmarkHasChanged} onAnimationEnd={this.clearAnimation}>
        <GlobalSelectionHeaderRow checked={isChecked} onCheckClick={this.handleClick} multi={multi} renderCheckbox={function (_a) {
            var checkbox = _a.checkbox;
            return (<Feature features={['organizations:global-views']} hookName="feature-disabled:project-selector-checkbox" renderDisabled={_this.renderDisabledCheckbox}>
              {checkbox}
            </Feature>);
        }}>
          <BadgeWrapper isMulti={multi}>
            <IdBadge project={project} avatarSize={16} displayName={<Highlight text={inputValue}>{project.slug}</Highlight>} avatarProps={{ consistentWidth: true }}/>
          </BadgeWrapper>
          <StyledBookmarkStar project={project} organization={organization} bookmarkHasChanged={bookmarkHasChanged} onToggle={this.handleBookmarkToggle}/>
          <StyledLink to={"/settings/" + organization.slug + "/" + project.slug + "/"} onClick={function (e) { return e.stopPropagation(); }}>
            <IconSettings />
          </StyledLink>
        </GlobalSelectionHeaderRow>
      </BadgeAndActionsWrapper>);
    };
    ProjectSelectorItem.defaultProps = defaultProps;
    return ProjectSelectorItem;
}(React.PureComponent));
export default ProjectSelectorItem;
var StyledBookmarkStar = styled(BookmarkStar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", ";\n  box-sizing: content-box;\n  opacity: ", ";\n  transition: 0.5s opacity ease-out;\n  display: block;\n  width: 14px;\n  height: 14px;\n  margin-top: -", "; /* trivial alignment bump */\n  ", ";\n"], ["\n  padding: ", " ", ";\n  box-sizing: content-box;\n  opacity: ", ";\n  transition: 0.5s opacity ease-out;\n  display: block;\n  width: 14px;\n  height: 14px;\n  margin-top: -", "; /* trivial alignment bump */\n  ",
    ";\n"])), space(1), space(0.5), function (p) { return (p.project.isBookmarked ? 1 : 0.33); }, space(0.25), function (p) {
    return p.bookmarkHasChanged && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      animation: 0.5s ", ";\n    "], ["\n      animation: 0.5s ", ";\n    "])), pulse(1.4));
});
var BadgeWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  ", ";\n  white-space: nowrap;\n  overflow: hidden;\n"], ["\n  display: flex;\n  flex: 1;\n  ", ";\n  white-space: nowrap;\n  overflow: hidden;\n"])), function (p) { return !p.isMulti && 'flex: 1'; });
var StyledLink = styled(Link)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", " ", " ", " ", ";\n  opacity: 0.33;\n  transition: 0.5s opacity ease-out;\n  :hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", " ", " ", " ", ";\n  opacity: 0.33;\n  transition: 0.5s opacity ease-out;\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, space(1), space(0.25), space(1), space(1), function (p) { return p.theme.textColor; });
var BadgeAndActionsWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", ";\n  z-index: ", ";\n  position: relative;\n  border-style: solid;\n  border-width: 1px 0;\n  border-color: transparent;\n  :hover {\n    ", " {\n      opacity: 1;\n    }\n    ", " {\n      opacity: 1;\n    }\n  }\n"], ["\n  ",
    ";\n  z-index: ", ";\n  position: relative;\n  border-style: solid;\n  border-width: 1px 0;\n  border-color: transparent;\n  :hover {\n    ", " {\n      opacity: 1;\n    }\n    ", " {\n      opacity: 1;\n    }\n  }\n"])), function (p) {
    return p.bookmarkHasChanged && css(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n      animation: 1s ", ";\n    "], ["\n      animation: 1s ", ";\n    "])), alertHighlight('info'));
}, function (p) { return (p.bookmarkHasChanged ? 1 : 'inherit'); }, StyledBookmarkStar, StyledLink);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=selectorItem.jsx.map