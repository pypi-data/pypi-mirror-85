import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tn } from 'app/locale';
import Search from 'app/components/search';
import HelpSource from 'app/components/search/sources/helpSource';
import SearchResult from 'app/components/search/searchResult';
import SearchResultWrapper from 'app/components/search/searchResultWrapper';
import space from 'app/styles/space';
import { IconWindow } from 'app/icons';
var renderResult = function (_a) {
    var _b;
    var item = _a.item, matches = _a.matches, itemProps = _a.itemProps, highlighted = _a.highlighted;
    var sectionHeading = item.sectionHeading !== undefined ? (<SectionHeading>
        <IconWindow />
        {t('From %s', item.sectionHeading)}
        <Count>{tn('%s result', '%s results', (_b = item.sectionCount) !== null && _b !== void 0 ? _b : 0)}</Count>
      </SectionHeading>) : null;
    if (item.empty) {
        return (<React.Fragment>
        {sectionHeading}
        <Empty>{t('No results from %s', item.sectionHeading)}</Empty>
      </React.Fragment>);
    }
    return (<React.Fragment>
      {sectionHeading}
      <SearchResultWrapper {...itemProps} highlighted={highlighted}>
        <SearchResult highlighted={highlighted} item={item} matches={matches}/>
      </SearchResultWrapper>
    </React.Fragment>);
};
// TODO(ts): Type based on Search props once that has types
var HelpSearch = function (props) { return (<Search {...props} sources={[HelpSource]} minSearch={3} closeOnSelect={false} renderItem={renderResult}/>); };
var SectionHeading = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  background: ", ";\n  padding: ", " ", ";\n\n  &:not(:first-of-type) {\n    border-top: 1px solid ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  background: ", ";\n  padding: ", " ", ";\n\n  &:not(:first-of-type) {\n    border-top: 1px solid ", ";\n  }\n"])), space(1), function (p) { return p.theme.backgroundSecondary; }, space(1), space(2), function (p) { return p.theme.innerBorder; });
var Count = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; });
var Empty = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  color: ", ";\n  font-size: ", ";\n  border-top: 1px solid ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  color: ", ";\n  font-size: ", ";\n  border-top: 1px solid ", ";\n"])), space(2), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.innerBorder; });
export default HelpSearch;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=helpSearch.jsx.map