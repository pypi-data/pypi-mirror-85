import { __extends, __makeTemplateObject } from "tslib";
import debounce from 'lodash/debounce';
import React from 'react';
import styled from '@emotion/styled';
import { Client } from 'app/api';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { t, tct } from 'app/locale';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
var defaultProps = {
    value: '',
};
var IssueListTagFilter = /** @class */ (function (_super) {
    __extends(IssueListTagFilter, _super);
    function IssueListTagFilter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            query: '',
            isLoading: false,
            value: _this.props.value,
            textValue: _this.props.value,
        };
        _this.api = new Client();
        _this.handleLoadOptions = function () {
            var _a = _this.props, tag = _a.tag, tagValueLoader = _a.tagValueLoader;
            var textValue = _this.state.textValue;
            if (tag.isInput || tag.predefined) {
                return;
            }
            if (!_this.api) {
                return;
            }
            _this.setState({
                isLoading: true,
            });
            tagValueLoader(tag.key, textValue)
                .then(function (resp) {
                _this.setState({
                    isLoading: false,
                    options: Object.values(resp).map(function (_a) {
                        var value = _a.value;
                        return ({
                            value: value,
                            label: value,
                        });
                    }),
                });
            })
                .catch(function () {
                // TODO(billy): This endpoint seems to timeout a lot,
                // should we log these errors into datadog?
                addErrorMessage(tct('Unable to retrieve values for tag [tagName]', {
                    tagName: textValue,
                }));
            });
        };
        _this.handleChangeInput = function (e) {
            var value = e.target.value;
            _this.setState({
                textValue: value,
            });
            _this.debouncedTextChange(value);
        };
        _this.debouncedTextChange = debounce(function (text) {
            _this.handleChange(text);
        }, 150);
        _this.handleOpenMenu = function () {
            if (_this.props.tag.predefined) {
                return;
            }
            _this.setState({
                isLoading: true,
            }, _this.handleLoadOptions);
        };
        _this.handleChangeSelect = function (valueObj) {
            var value = valueObj ? valueObj.value : null;
            _this.handleChange(value);
        };
        _this.handleChangeSelectInput = function (value) {
            _this.setState({
                textValue: value,
            }, _this.handleLoadOptions);
        };
        _this.handleChange = function (value) {
            var _a = _this.props, onSelect = _a.onSelect, tag = _a.tag;
            _this.setState({
                value: value,
            }, function () {
                onSelect && onSelect(tag, value);
            });
        };
        return _this;
    }
    IssueListTagFilter.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (nextProps.value !== this.state.value) {
            this.setState({
                value: nextProps.value,
                textValue: nextProps.value,
            });
        }
    };
    IssueListTagFilter.prototype.componentWillUnmount = function () {
        if (!this.api) {
            return;
        }
        this.api.clear();
    };
    IssueListTagFilter.prototype.render = function () {
        var tag = this.props.tag;
        return (<StreamTagFilter>
        <StyledHeader>{tag.key}</StyledHeader>

        {!!tag.isInput && (<input className="form-control" type="text" value={this.state.textValue} onChange={this.handleChangeInput}/>)}

        {!tag.isInput && (<SelectControl deprecatedSelectControl clearable filterOptions={function (options) { return options; }} placeholder="--" value={this.state.value} onChange={this.handleChangeSelect} isLoading={this.state.isLoading} onInputChange={this.handleChangeSelectInput} onOpen={this.handleOpenMenu} autoload={false} noResultsText={this.state.isLoading ? t('Loading...') : t('No results found')} options={tag.predefined
            ? tag.values &&
                tag.values.map(function (value) { return ({
                    value: value,
                    label: value,
                }); })
            : this.state.options}/>)}
      </StreamTagFilter>);
    };
    IssueListTagFilter.defaultProps = defaultProps;
    return IssueListTagFilter;
}(React.Component));
export default IssueListTagFilter;
var StreamTagFilter = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var StyledHeader = styled('h6')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=tagFilter.jsx.map