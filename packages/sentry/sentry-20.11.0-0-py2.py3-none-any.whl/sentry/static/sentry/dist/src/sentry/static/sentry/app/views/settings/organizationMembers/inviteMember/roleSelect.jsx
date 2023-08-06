import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { t } from 'app/locale';
import Radio from 'app/components/radio';
import TextBlock from 'app/views/settings/components/text/textBlock';
var Label = styled('label')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  margin-bottom: 0;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  margin-bottom: 0;\n"])));
var RoleSelect = /** @class */ (function (_super) {
    __extends(RoleSelect, _super);
    function RoleSelect() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RoleSelect.prototype.render = function () {
        var _this = this;
        var _a = this.props, disabled = _a.disabled, enforceAllowed = _a.enforceAllowed, roleList = _a.roleList, selectedRole = _a.selectedRole;
        return (<Panel>
        <PanelHeader>{t('Role')}</PanelHeader>

        <PanelBody>
          {roleList.map(function (role) {
            var desc = role.desc, name = role.name, id = role.id, allowed = role.allowed;
            var isDisabled = disabled || (enforceAllowed && !allowed);
            return (<PanelItem key={id} onClick={function () { return !isDisabled && _this.props.setRole(id); }} css={!isDisabled ? {} : { color: 'grey', cursor: 'default' }}>
                <Label>
                  <Radio id={id} value={name} checked={id === selectedRole} readOnly/>
                  <div style={{ flex: 1, padding: '0 16px' }}>
                    {name}
                    <TextBlock noMargin>
                      <div className="help-block">{desc}</div>
                    </TextBlock>
                  </div>
                </Label>
              </PanelItem>);
        })}
        </PanelBody>
      </Panel>);
    };
    RoleSelect.propTypes = {
        /**
         * Whether to disable or not using `allowed` prop from API request
         */
        enforceAllowed: PropTypes.bool,
        disabled: PropTypes.bool,
        selectedRole: PropTypes.string,
        roleList: PropTypes.array,
        setRole: PropTypes.func,
    };
    return RoleSelect;
}(React.Component));
export default RoleSelect;
var templateObject_1;
//# sourceMappingURL=roleSelect.jsx.map