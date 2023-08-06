import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownButton from 'app/components/dropdownButton';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import { GroupingConfigItem } from '.';
var GroupingConfigSelect = /** @class */ (function (_super) {
    __extends(GroupingConfigSelect, _super);
    function GroupingConfigSelect() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GroupingConfigSelect.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { configs: [] });
    };
    GroupingConfigSelect.prototype.getEndpoints = function () {
        return [['configs', '/grouping-configs/']];
    };
    GroupingConfigSelect.prototype.renderLoading = function () {
        return this.renderBody();
    };
    GroupingConfigSelect.prototype.renderBody = function () {
        var _a = this.props, configId = _a.configId, eventConfigId = _a.eventConfigId, onSelect = _a.onSelect;
        var configs = this.state.configs;
        var options = configs.map(function (_a) {
            var id = _a.id, hidden = _a.hidden;
            return ({
                value: id,
                label: (<GroupingConfigItem isHidden={hidden} isActive={id === eventConfigId}>
          {id}
        </GroupingConfigItem>),
            });
        });
        return (<DropdownAutoComplete onSelect={onSelect} items={options}>
        {function (_a) {
            var isOpen = _a.isOpen;
            return (<Tooltip title={t('Click here to experiment with other grouping configs')}>
            <StyledDropdownButton isOpen={isOpen} size="small">
              <GroupingConfigItem isActive={eventConfigId === configId}>
                {configId}
              </GroupingConfigItem>
            </StyledDropdownButton>
          </Tooltip>);
        }}
      </DropdownAutoComplete>);
    };
    return GroupingConfigSelect;
}(AsyncComponent));
var StyledDropdownButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-weight: inherit;\n"], ["\n  font-weight: inherit;\n"])));
export default GroupingConfigSelect;
var templateObject_1;
//# sourceMappingURL=groupingConfigSelect.jsx.map