import { __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Checkbox from 'app/components/checkbox';
import Switch from 'app/components/switch';
import { tokenizeSearch, stringifyQueryObject } from 'app/utils/tokenizeSearch';
var getBoolean = function (list) {
    return Array.isArray(list) ? list && list.map(function (v) { return v.toLowerCase(); }).includes('true') : null;
};
var MembersFilter = function (_a) {
    var className = _a.className, roles = _a.roles, query = _a.query, onChange = _a.onChange;
    var search = tokenizeSearch(query);
    var filters = {
        roles: search.getTagValues('role') || [],
        isInvited: getBoolean(search.getTagValues('isInvited')),
        ssoLinked: getBoolean(search.getTagValues('ssoLinked')),
        has2fa: getBoolean(search.getTagValues('has2fa')),
    };
    var handleRoleFilter = function (id) { return function () {
        var roleList = new Set(search.getTagValues('role') ? __spread(search.getTagValues('role')) : []);
        if (roleList.has(id)) {
            roleList.delete(id);
        }
        else {
            roleList.add(id);
        }
        var newSearch = search.copy();
        newSearch.setTagValues('role', __spread(roleList));
        onChange(stringifyQueryObject(newSearch));
    }; };
    var handleBoolFilter = function (key) { return function (value) {
        var newQueryObject = search.copy();
        newQueryObject.removeTag(key);
        if (value !== null) {
            newQueryObject.setTagValues(key, [Boolean(value).toString()]);
        }
        onChange(stringifyQueryObject(newQueryObject));
    }; };
    return (<FilterContainer className={className}>
      <FilterHeader>{t('Filter By')}</FilterHeader>

      <FilterLists>
        <Filters>
          <h3>{t('User Role')}</h3>
          {roles.map(function (_a) {
        var id = _a.id, name = _a.name;
        return (<label key={id}>
              <Checkbox data-test-id={"filter-role-" + id} checked={filters.roles.includes(id)} onChange={handleRoleFilter(id)}/>
              {name}
            </label>);
    })}
        </Filters>

        <Filters>
          <h3>{t('Status')}</h3>
          <BooleanFilter data-test-id="filter-isInvited" onChange={handleBoolFilter('isInvited')} value={filters.isInvited}>
            {t('Invited')}
          </BooleanFilter>
          <BooleanFilter data-test-id="filter-has2fa" onChange={handleBoolFilter('has2fa')} value={filters.has2fa}>
            {t('2FA')}
          </BooleanFilter>
          <BooleanFilter data-test-id="filter-ssoLinked" onChange={handleBoolFilter('ssoLinked')} value={filters.ssoLinked}>
            {t('SSO Linked')}
          </BooleanFilter>
        </Filters>
      </FilterLists>
    </FilterContainer>);
};
var BooleanFilter = function (_a) {
    var onChange = _a.onChange, value = _a.value, children = _a.children;
    return (<label>
    <Checkbox checked={value !== null} onChange={function () { return onChange(value === null ? true : null); }}/>
    {children}
    <Switch isDisabled={value === null} isActive={value === true} toggle={function () { return onChange(!value); }}/>
  </label>);
};
MembersFilter.propTypes = {
    roles: PropTypes.arrayOf(PropTypes.object).isRequired,
    query: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
};
BooleanFilter.propTypes = {
    onChange: PropTypes.func.isRequired,
    value: PropTypes.oneOf([null, true, false]),
};
var FilterContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-radius: 4px;\n  background: ", ";\n  box-shadow: ", ";\n  border: 1px solid ", ";\n"], ["\n  border-radius: 4px;\n  background: ", ";\n  box-shadow: ", ";\n  border: 1px solid ", ";\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.border; });
var FilterHeader = styled('h2')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-top-left-radius: 4px;\n  border-top-right-radius: 4px;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  font-size: ", ";\n  padding: ", ";\n  margin: 0;\n"], ["\n  border-top-left-radius: 4px;\n  border-top-right-radius: 4px;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  font-size: ", ";\n  padding: ", ";\n  margin: 0;\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeExtraSmall; }, space(1));
var FilterLists = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 100px max-content;\n  grid-gap: ", ";\n  margin: ", ";\n  margin-top: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 100px max-content;\n  grid-gap: ", ";\n  margin: ", ";\n  margin-top: ", ";\n"])), space(3), space(1.5), space(0.75));
var Filters = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(auto-fit, minmax(0, max-content));\n  grid-gap: ", ";\n  font-size: ", ";\n\n  h3 {\n    color: #000;\n    font-size: ", ";\n    text-transform: uppercase;\n    margin: ", " 0;\n  }\n\n  label {\n    display: grid;\n    grid-template-columns: max-content 1fr max-content;\n    grid-gap: ", ";\n    align-items: center;\n    font-weight: normal;\n    white-space: nowrap;\n    height: ", ";\n  }\n\n  input,\n  label {\n    margin: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-rows: repeat(auto-fit, minmax(0, max-content));\n  grid-gap: ", ";\n  font-size: ", ";\n\n  h3 {\n    color: #000;\n    font-size: ", ";\n    text-transform: uppercase;\n    margin: ", " 0;\n  }\n\n  label {\n    display: grid;\n    grid-template-columns: max-content 1fr max-content;\n    grid-gap: ", ";\n    align-items: center;\n    font-weight: normal;\n    white-space: nowrap;\n    height: ", ";\n  }\n\n  input,\n  label {\n    margin: 0;\n  }\n"])), space(1), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.fontSizeSmall; }, space(1), space(0.75), space(2));
export default MembersFilter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=membersFilter.jsx.map