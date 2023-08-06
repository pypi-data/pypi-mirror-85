import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import DropdownControl from 'app/components/dropdownControl';
import DropDownButton from './dropdownButton';
import OptionsGroup from './optionsGroup';
var Filter = /** @class */ (function (_super) {
    __extends(Filter, _super);
    function Filter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hasTypeOption: false,
            hasLevelOption: false,
            checkedQuantity: _this.props.options.length,
        };
        _this.updateState = function () {
            var options = _this.props.options;
            _this.setState({
                hasTypeOption: options[0].length > 0,
                hasLevelOption: options[1].length > 0,
                checkedQuantity: _this.getCheckedQuantity(),
            });
        };
        _this.getCheckedQuantity = function () {
            var options = _this.props.options;
            var checkedQuantity = 0;
            for (var index in options) {
                for (var option in options[index]) {
                    if (options[index][option].isChecked) {
                        checkedQuantity += 1;
                    }
                }
            }
            return checkedQuantity;
        };
        _this.filterOptionsFirstStep = function (options, filterOption) {
            return options.map(function (option) {
                if (isEqual(option, filterOption)) {
                    return __assign(__assign({}, option), { isChecked: !option.isChecked });
                }
                return option;
            });
        };
        _this.handleClick = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = __read(args, 2), type = _a[0], option = _a[1];
            var _b = _this.props, onFilter = _b.onFilter, options = _b.options;
            if (type === 'type') {
                var filteredTypes = _this.filterOptionsFirstStep(options[0], option);
                onFilter([filteredTypes, options[1]]);
                return;
            }
            var filteredLevels = _this.filterOptionsFirstStep(options[1], option);
            onFilter([options[0], filteredLevels]);
        };
        return _this;
    }
    Filter.prototype.componentDidMount = function () {
        this.updateState();
    };
    Filter.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(prevProps.options, this.props.options)) {
            this.updateState();
        }
    };
    Filter.prototype.render = function () {
        var options = this.props.options;
        var _a = this.state, hasTypeOption = _a.hasTypeOption, hasLevelOption = _a.hasLevelOption, checkedQuantity = _a.checkedQuantity;
        if (!hasTypeOption && !hasLevelOption) {
            return null;
        }
        return (<Wrapper>
        <DropdownControl menuWidth="240px" blendWithActor button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<DropDownButton isOpen={isOpen} getActorProps={getActorProps} checkedQuantity={checkedQuantity}/>);
        }}>
          {hasTypeOption && (<OptionsGroup type="type" onClick={this.handleClick} options={options[0]}/>)}

          {hasLevelOption && (<OptionsGroup type="level" onClick={this.handleClick} options={options[1]}/>)}
        </DropdownControl>
      </Wrapper>);
    };
    return Filter;
}(React.Component));
export default Filter;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n"], ["\n  position: relative;\n  display: flex;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map