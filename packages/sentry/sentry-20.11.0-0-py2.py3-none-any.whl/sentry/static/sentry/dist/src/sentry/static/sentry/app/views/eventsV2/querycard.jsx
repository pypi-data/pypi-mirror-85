import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ActivityAvatar from 'app/components/activity/item/avatar';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import Link from 'app/components/links/link';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { callIfFunction } from 'app/utils/callIfFunction';
import Card from 'app/components/card';
var QueryCard = /** @class */ (function (_super) {
    __extends(QueryCard, _super);
    function QueryCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function () {
            var onEventClick = _this.props.onEventClick;
            callIfFunction(onEventClick);
        };
        return _this;
    }
    QueryCard.prototype.render = function () {
        var _a = this.props, title = _a.title, subtitle = _a.subtitle, queryDetail = _a.queryDetail, renderContextMenu = _a.renderContextMenu, renderGraph = _a.renderGraph, createdBy = _a.createdBy, dateStatus = _a.dateStatus;
        return (<Link data-test-id={"card-" + title} onClick={this.handleClick} to={this.props.to}>
        <StyledQueryCard interactive>
          <QueryCardHeader>
            <QueryCardContent>
              <QueryTitle>{title}</QueryTitle>
              <QueryDetail>{queryDetail}</QueryDetail>
            </QueryCardContent>
            <AvatarWrapper>
              {createdBy ? (<ActivityAvatar type="user" user={createdBy} size={34}/>) : (<ActivityAvatar type="system" size={34}/>)}
            </AvatarWrapper>
          </QueryCardHeader>
          <QueryCardBody>{renderGraph()}</QueryCardBody>
          <QueryCardFooter>
            <DateSelected>
              {subtitle}
              {dateStatus ? (<DateStatus>
                  {t('Edited')} {dateStatus}
                </DateStatus>) : null}
            </DateSelected>
            {renderContextMenu && renderContextMenu()}
          </QueryCardFooter>
        </StyledQueryCard>
      </Link>);
    };
    return QueryCard;
}(React.PureComponent));
var AvatarWrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border: 3px solid ", ";\n  border-radius: 50%;\n  height: min-content;\n"], ["\n  border: 3px solid ", ";\n  border-radius: 50%;\n  height: min-content;\n"])), function (p) { return p.theme.border; });
var QueryCardContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 1;\n  overflow: hidden;\n  margin-right: ", ";\n"], ["\n  flex-grow: 1;\n  overflow: hidden;\n  margin-right: ", ";\n"])), space(1));
var StyledQueryCard = styled(Card)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  justify-content: space-between;\n  height: 100%;\n  &:focus,\n  &:hover {\n    top: -1px;\n  }\n"], ["\n  justify-content: space-between;\n  height: 100%;\n  &:focus,\n  &:hover {\n    top: -1px;\n  }\n"])));
var QueryCardHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  padding: ", " ", ";\n"])), space(1.5), space(2));
var QueryTitle = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis);
var QueryDetail = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  line-height: 1.5;\n  ", ";\n"], ["\n  font-family: ", ";\n  font-size: ", ";\n  color: ", ";\n  line-height: 1.5;\n  ", ";\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, overflowEllipsis);
var QueryCardBody = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  background: ", ";\n  max-height: 100px;\n  height: 100%;\n  overflow: hidden;\n"], ["\n  background: ", ";\n  max-height: 100px;\n  height: 100%;\n  overflow: hidden;\n"])), function (p) { return p.theme.backgroundSecondary; });
var QueryCardFooter = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  padding: ", " ", ";\n"])), space(1), space(2));
var DateSelected = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space(1), overflowEllipsis, function (p) { return p.theme.textColor; });
var DateStatus = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  color: ", ";\n  padding-left: ", ";\n"], ["\n  color: ", ";\n  padding-left: ", ";\n"])), function (p) { return p.theme.purple300; }, space(1));
export default QueryCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=querycard.jsx.map