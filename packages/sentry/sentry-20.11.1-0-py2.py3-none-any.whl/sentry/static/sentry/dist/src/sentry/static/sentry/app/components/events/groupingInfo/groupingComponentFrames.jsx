import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { tct } from 'app/locale';
import Button from 'app/components/button';
import { IconAdd, IconSubtract } from 'app/icons';
import { GroupingComponentListItem } from './groupingComponent';
var GroupingComponentFrames = /** @class */ (function (_super) {
    __extends(GroupingComponentFrames, _super);
    function GroupingComponentFrames() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: true,
        };
        return _this;
    }
    GroupingComponentFrames.prototype.render = function () {
        var _this = this;
        var _a = this.props, items = _a.items, maxVisibleItems = _a.maxVisibleItems;
        var collapsed = this.state.collapsed;
        var isCollapsable = items.length > maxVisibleItems;
        return (<React.Fragment>
        {items.map(function (item, index) {
            if (!collapsed || index < maxVisibleItems) {
                return (<GroupingComponentListItem isCollapsable={isCollapsable} key={index}>
                {item}
              </GroupingComponentListItem>);
            }
            if (index === maxVisibleItems) {
                return (<GroupingComponentListItem key={index}>
                <ToggleCollapse size="small" priority="link" icon={<IconAdd size="8px"/>} onClick={function () { return _this.setState({ collapsed: false }); }}>
                  {tct('show [numberOfFrames] similiar', {
                    numberOfFrames: items.length - maxVisibleItems,
                })}
                </ToggleCollapse>
              </GroupingComponentListItem>);
            }
            return null;
        })}

        {!collapsed && items.length > maxVisibleItems && (<GroupingComponentListItem>
            <ToggleCollapse size="small" priority="link" icon={<IconSubtract size="8px"/>} onClick={function () { return _this.setState({ collapsed: true }); }}>
              {tct('collapse [numberOfFrames] similiar', {
            numberOfFrames: items.length - maxVisibleItems,
        })}
            </ToggleCollapse>
          </GroupingComponentListItem>)}
      </React.Fragment>);
    };
    GroupingComponentFrames.defaultProps = {
        maxVisibleItems: 2,
    };
    return GroupingComponentFrames;
}(React.Component));
var ToggleCollapse = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space(0.5));
export default GroupingComponentFrames;
var templateObject_1;
//# sourceMappingURL=groupingComponentFrames.jsx.map