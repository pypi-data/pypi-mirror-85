import { __extends, __rest } from "tslib";
import React from 'react';
import { components } from 'react-select';
import { t } from 'app/locale';
import InputField from 'app/views/settings/components/forms/inputField';
import IdBadge from 'app/components/idBadge';
import SelectControl from 'app/components/forms/selectControl';
var defaultProps = {
    avatarSize: 20,
    placeholder: t('Choose Sentry project'),
};
var RenderField = /** @class */ (function (_super) {
    __extends(RenderField, _super);
    function RenderField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        //need to map the option object to the value
        _this.handleChange = function (onBlur, onChange, optionObj, event) {
            var value = optionObj.value;
            onChange === null || onChange === void 0 ? void 0 : onChange(value, event);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(value, event);
        };
        return _this;
    }
    RenderField.prototype.render = function () {
        var _a = this.props, projects = _a.projects, avatarSize = _a.avatarSize, onChange = _a.onChange, onBlur = _a.onBlur, rest = __rest(_a, ["projects", "avatarSize", "onChange", "onBlur"]);
        var projectOptions = projects.map(function (_a) {
            var slug = _a.slug, id = _a.id;
            return ({ value: id, label: slug });
        });
        var customOptionProject = function (projectProps) {
            var project = projects.find(function (proj) { return proj.id === projectProps.value; });
            //shouldn't happen but need to account for it
            if (!project) {
                return <components.Option {...projectProps}/>;
            }
            return (<components.Option {...projectProps}>
          <IdBadge project={project} avatarSize={avatarSize} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </components.Option>);
        };
        var customValueContainer = function (containerProps) {
            var selectedValue = containerProps.getValue()[0];
            var project = projects.find(function (proj) { return proj.id === (selectedValue === null || selectedValue === void 0 ? void 0 : selectedValue.value); });
            //shouldn't happen but need to account for it
            if (!project) {
                return <components.ValueContainer {...containerProps}/>;
            }
            return (<components.ValueContainer {...containerProps}>
          <IdBadge project={project} avatarSize={avatarSize} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </components.ValueContainer>);
        };
        return (<SelectControl options={projectOptions} components={{
            Option: customOptionProject,
            ValueContainer: customValueContainer,
        }} {...rest} onChange={this.handleChange.bind(this, onBlur, onChange)}/>);
    };
    RenderField.defaultProps = defaultProps;
    return RenderField;
}(React.Component));
var SentryProjectSelectorField = function (props) { return (<InputField {...props} field={function (renderProps) { return <RenderField {...renderProps}/>; }}/>); };
export default SentryProjectSelectorField;
//# sourceMappingURL=sentryProjectSelectorField.jsx.map