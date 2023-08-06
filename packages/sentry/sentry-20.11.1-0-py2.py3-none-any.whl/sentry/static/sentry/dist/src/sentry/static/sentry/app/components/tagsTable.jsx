import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import Link from 'app/components/links/link';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import Version from 'app/components/version';
var TagsTable = function (_a) {
    var event = _a.event, query = _a.query, generateUrl = _a.generateUrl, _b = _a.title, title = _b === void 0 ? t('Event Tag Details') : _b;
    var tags = event.tags;
    return (<StyledTagsTable>
      <SectionHeading>{title}</SectionHeading>
      <StyledTable>
        <tbody>
          {tags.map(function (tag) {
        var tagInQuery = query.includes(tag.key + ":");
        var target = tagInQuery ? undefined : generateUrl(tag);
        var renderTagValue = function () {
            switch (tag.key) {
                case 'release':
                    return <Version version={tag.value} anchor={false} withPackage/>;
                default:
                    return tag.value;
            }
        };
        return (<StyledTr key={tag.key}>
                <TagKey>{tag.key}</TagKey>
                <TagValue>
                  {tagInQuery ? (<Tooltip title={t('This tag is in the current filter conditions')}>
                      <span>{renderTagValue()}</span>
                    </Tooltip>) : (<Link to={target || ''}>{renderTagValue()}</Link>)}
                </TagValue>
              </StyledTr>);
    })}
        </tbody>
      </StyledTable>
    </StyledTagsTable>);
};
var StyledTagsTable = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var StyledTable = styled('table')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  table-layout: fixed;\n  width: 100%;\n  max-width: 100%;\n"], ["\n  table-layout: fixed;\n  width: 100%;\n  max-width: 100%;\n"])));
var StyledTr = styled('tr')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  &:nth-child(2n + 1) td {\n    background-color: ", ";\n  }\n"], ["\n  &:nth-child(2n + 1) td {\n    background-color: ", ";\n  }\n"])), function (p) { return p.theme.backgroundSecondary; });
var TagKey = styled('td')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", " ", ";\n  font-size: ", ";\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  padding: ", " ", ";\n  font-size: ", ";\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), space(0.5), space(1), function (p) { return p.theme.fontSizeMedium; });
var TagValue = styled(TagKey)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  text-align: right;\n  ", ";\n"], ["\n  text-align: right;\n  ", ";\n"])), overflowEllipsis);
export default TagsTable;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=tagsTable.jsx.map