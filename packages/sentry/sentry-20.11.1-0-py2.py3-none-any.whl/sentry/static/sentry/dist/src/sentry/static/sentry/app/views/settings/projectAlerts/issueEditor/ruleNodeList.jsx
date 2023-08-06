import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
import RuleNode from './ruleNode';
var RuleNodeList = /** @class */ (function (_super) {
    __extends(RuleNodeList, _super);
    function RuleNodeList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getNode = function (id) {
            var nodes = _this.props.nodes;
            return nodes ? nodes.find(function (node) { return node.id === id; }) : null;
        };
        return _this;
    }
    RuleNodeList.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var _c = this.props, onAddRow = _c.onAddRow, onDeleteRow = _c.onDeleteRow, onPropertyChange = _c.onPropertyChange, nodes = _c.nodes, placeholder = _c.placeholder, items = _c.items, organization = _c.organization, project = _c.project, disabled = _c.disabled, error = _c.error;
        var shouldUsePrompt = (_b = (_a = project.features) === null || _a === void 0 ? void 0 : _a.includes) === null || _b === void 0 ? void 0 : _b.call(_a, 'issue-alerts-targeting');
        var options = nodes
            ? nodes
                .filter(function (_a) {
                var enabled = _a.enabled;
                return enabled;
            })
                .map(function (node) {
                var _a;
                return ({
                    value: node.id,
                    label: shouldUsePrompt && ((_a = node.prompt) === null || _a === void 0 ? void 0 : _a.length) > 0 ? node.prompt : node.label,
                });
            })
            : [];
        return (<React.Fragment>
        <RuleNodes>
          {error}
          {items.map(function (item, idx) { return (<RuleNode key={idx} index={idx} node={_this.getNode(item.id)} onDelete={onDeleteRow} data={item} onPropertyChange={onPropertyChange} organization={organization} project={project} disabled={disabled}/>); })}
        </RuleNodes>
        <StyledSelectControl placeholder={placeholder} value={null} onChange={function (obj) { return onAddRow(obj ? obj.value : obj); }} options={options} disabled={disabled}/>
      </React.Fragment>);
    };
    return RuleNodeList;
}(React.Component));
export default RuleNodeList;
var StyledSelectControl = styled(SelectControl)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
var RuleNodes = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  margin-bottom: ", ";\n  grid-gap: ", ";\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n  }\n"], ["\n  display: grid;\n  margin-bottom: ", ";\n  grid-gap: ", ";\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n  }\n"])), space(1), space(1), function (p) { return p.theme.breakpoints[1]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=ruleNodeList.jsx.map