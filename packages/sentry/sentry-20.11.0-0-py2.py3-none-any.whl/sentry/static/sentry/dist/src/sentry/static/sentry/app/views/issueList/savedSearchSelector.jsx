import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl from 'app/components/dropdownControl';
import Tooltip from 'app/components/tooltip';
import { IconDelete } from 'app/icons';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
var SavedSearchSelector = /** @class */ (function (_super) {
    __extends(SavedSearchSelector, _super);
    function SavedSearchSelector() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SavedSearchSelector.prototype.getTitle = function () {
        var _a = this.props, searchId = _a.searchId, query = _a.query, savedSearchList = _a.savedSearchList;
        var result;
        if (searchId) {
            result = savedSearchList.find(function (search) { return searchId === search.id; });
        }
        else {
            result = savedSearchList.find(function (search) { return query === search.query; });
        }
        return result ? result.name : t('Custom Search');
    };
    SavedSearchSelector.prototype.renderList = function () {
        var _a = this.props, savedSearchList = _a.savedSearchList, onSavedSearchDelete = _a.onSavedSearchDelete, onSavedSearchSelect = _a.onSavedSearchSelect, organization = _a.organization;
        if (savedSearchList.length === 0) {
            return <EmptyItem>{t("There don't seem to be any saved searches yet.")}</EmptyItem>;
        }
        return savedSearchList.map(function (search, index) { return (<Tooltip title={<span>
            {search.name + " \u2022 "}
            <TooltipSearchQuery>{search.query}</TooltipSearchQuery>
          </span>} containerDisplayMode="block" delay={1000} key={search.id}>
        <MenuItem last={index === savedSearchList.length - 1}>
          <MenuItemLink tabIndex={-1} onClick={function () { return onSavedSearchSelect(search); }}>
            <SearchTitle>{search.name}</SearchTitle>
            <SearchQuery>{search.query}</SearchQuery>
          </MenuItemLink>
          {search.isGlobal === false && search.isPinned === false && (<Access organization={organization} access={['org:write']} renderNoAccessMessage={false}>
              <Confirm onConfirm={function () { return onSavedSearchDelete(search); }} message={t('Are you sure you want to delete this saved search?')} stopPropagation>
                <DeleteButton borderless title={t('Delete this saved search')} icon={<IconDelete />} label={t('delete')} size="zero"/>
              </Confirm>
            </Access>)}
        </MenuItem>
      </Tooltip>); });
    };
    SavedSearchSelector.prototype.render = function () {
        var _this = this;
        return (<DropdownControl menuWidth="35vw" blendWithActor button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen}>
            <ButtonTitle>{_this.getTitle()}</ButtonTitle>
          </StyledDropdownButton>);
        }}>
        {this.renderList()}
      </DropdownControl>);
    };
    SavedSearchSelector.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        savedSearchList: PropTypes.array.isRequired,
        onSavedSearchSelect: PropTypes.func.isRequired,
        onSavedSearchDelete: PropTypes.func.isRequired,
        searchId: PropTypes.string,
        query: PropTypes.string,
    };
    return SavedSearchSelector;
}(React.Component));
export default SavedSearchSelector;
var StyledDropdownButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  background-color: ", ";\n  border-right: 0;\n  z-index: ", ";\n  border-radius: ", ";\n  white-space: nowrap;\n  max-width: 200px;\n  margin-right: 0;\n\n  &:hover,\n  &:active {\n    border-right: 0;\n  }\n"], ["\n  color: ", ";\n  background-color: ", ";\n  border-right: 0;\n  z-index: ", ";\n  border-radius: ",
    ";\n  white-space: nowrap;\n  max-width: 200px;\n  margin-right: 0;\n\n  &:hover,\n  &:active {\n    border-right: 0;\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.background; }, function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; }, function (p) {
    return p.isOpen
        ? p.theme.borderRadius + " 0 0 0"
        : p.theme.borderRadius + " 0 0 " + p.theme.borderRadius;
});
var ButtonTitle = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var SearchTitle = styled('strong')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  padding: 0;\n  background: inherit;\n\n  &:after {\n    content: ' \u2022 ';\n  }\n"], ["\n  color: ", ";\n  padding: 0;\n  background: inherit;\n\n  &:after {\n    content: ' \\u2022 ';\n  }\n"])), function (p) { return p.theme.textColor; });
var SearchQuery = styled('code')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  padding: 0;\n  background: inherit;\n"], ["\n  color: ", ";\n  padding: 0;\n  background: inherit;\n"])), function (p) { return p.theme.textColor; });
var TooltipSearchQuery = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n  font-family: ", ";\n"], ["\n  color: ", ";\n  font-weight: normal;\n  font-family: ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.text.familyMono; });
var DeleteButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  background: transparent;\n  flex-shrink: 0;\n  padding: ", " ", " ", " 0;\n\n  &:hover {\n    background: transparent;\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  background: transparent;\n  flex-shrink: 0;\n  padding: ", " ", " ", " 0;\n\n  &:hover {\n    background: transparent;\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, space(1.5), space(1.5), space(1), function (p) { return p.theme.blue300; });
var MenuItem = styled('li')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  background-color: ", ";\n\n  position: relative;\n  border-bottom: ", ";\n  font-size: ", ";\n  padding: 0;\n\n  & :hover {\n    background: ", ";\n  }\n"], ["\n  display: flex;\n  background-color: ", ";\n\n  position: relative;\n  border-bottom: ", ";\n  font-size: ", ";\n  padding: 0;\n\n  & :hover {\n    background: ", ";\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return (!p.last ? "1px solid " + p.theme.innerBorder : null); }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.backgroundSecondary; });
var MenuItemLink = styled('a')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: block;\n  flex-grow: 1;\n  padding: ", " ", ";\n\n  ", "\n"], ["\n  display: block;\n  flex-grow: 1;\n  padding: ", " ", ";\n\n  ", "\n"])), space(1), space(1.5), overflowEllipsis);
var EmptyItem = styled('li')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  padding: 8px 10px 5px;\n  font-style: italic;\n"], ["\n  padding: 8px 10px 5px;\n  font-style: italic;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=savedSearchSelector.jsx.map