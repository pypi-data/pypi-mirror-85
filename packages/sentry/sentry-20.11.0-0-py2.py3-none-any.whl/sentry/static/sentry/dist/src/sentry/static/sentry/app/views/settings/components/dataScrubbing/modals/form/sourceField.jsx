import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t } from 'app/locale';
import InputField from 'app/views/settings/components/forms/inputField';
import TextOverflow from 'app/components/textOverflow';
import { defined } from 'app/utils';
import { unarySuggestions, binarySuggestions } from '../../utils';
import SourceSuggestionExamples from './sourceSuggestionExamples';
import { SourceSuggestionType } from '../../types';
var defaultHelp = t('Where to look. In the simplest case this can be an attribute name.');
var SourceField = /** @class */ (function (_super) {
    __extends(SourceField, _super);
    function SourceField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            suggestions: [],
            fieldValues: [],
            activeSuggestion: 0,
            showSuggestions: false,
            hideCaret: false,
            help: defaultHelp,
        };
        _this.selectorField = React.createRef();
        _this.suggestionList = React.createRef();
        _this.handleChange = function (value) {
            _this.loadFieldValues(value);
            _this.props.onChange(value);
        };
        _this.handleClickOutside = function () {
            _this.setState({
                showSuggestions: false,
                hideCaret: false,
            });
        };
        _this.handleClickSuggestionItem = function (suggestion) { return function () {
            var fieldValues = _this.getNewFieldValues(suggestion);
            _this.setState({
                fieldValues: fieldValues,
                activeSuggestion: 0,
                showSuggestions: false,
                hideCaret: false,
            }, _this.changeParentValue);
        }; };
        _this.handleKeyDown = function (_value, event) {
            event.persist();
            var keyCode = event.keyCode;
            var _a = _this.state, activeSuggestion = _a.activeSuggestion, suggestions = _a.suggestions;
            if (keyCode === 8 || keyCode === 32) {
                _this.toggleSuggestions(true);
                return;
            }
            if (keyCode === 13) {
                _this.handleClickSuggestionItem(suggestions[activeSuggestion])();
                return;
            }
            if (keyCode === 38) {
                if (activeSuggestion === 0) {
                    return;
                }
                _this.setState({ activeSuggestion: activeSuggestion - 1 }, function () {
                    _this.scrollToSuggestion();
                });
                return;
            }
            if (keyCode === 40) {
                if (activeSuggestion === suggestions.length - 1) {
                    return;
                }
                _this.setState({ activeSuggestion: activeSuggestion + 1 }, function () {
                    _this.scrollToSuggestion();
                });
                return;
            }
        };
        _this.handleFocus = function () {
            _this.toggleSuggestions(true);
        };
        return _this;
    }
    SourceField.prototype.componentDidMount = function () {
        this.loadFieldValues(this.props.value);
        this.toggleSuggestions(false);
    };
    SourceField.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.suggestions !== this.props.suggestions) {
            this.loadFieldValues(this.props.value);
            this.toggleSuggestions(false);
        }
        if (prevProps.isRegExMatchesSelected !== this.props.isRegExMatchesSelected ||
            prevProps.value !== this.props.value) {
            this.checkPossiblyRegExMatchExpression(this.props.value);
        }
    };
    SourceField.prototype.getAllSuggestions = function () {
        return __spread(this.getValueSuggestions(), unarySuggestions, binarySuggestions);
    };
    SourceField.prototype.getValueSuggestions = function () {
        return this.props.suggestions || [];
    };
    SourceField.prototype.getFilteredSuggestions = function (value, type) {
        var valuesToBeFiltered = [];
        switch (type) {
            case SourceSuggestionType.BINARY: {
                valuesToBeFiltered = binarySuggestions;
                break;
            }
            case SourceSuggestionType.VALUE: {
                valuesToBeFiltered = this.getValueSuggestions();
                break;
            }
            case SourceSuggestionType.UNARY: {
                valuesToBeFiltered = unarySuggestions;
                break;
            }
            default: {
                valuesToBeFiltered = __spread(this.getValueSuggestions(), unarySuggestions);
            }
        }
        var filteredSuggestions = valuesToBeFiltered.filter(function (s) { return s.value.toLowerCase().indexOf(value.toLowerCase()) > -1; });
        return filteredSuggestions;
    };
    SourceField.prototype.getNewSuggestions = function (fieldValues) {
        var lastFieldValue = fieldValues[fieldValues.length - 1];
        var penultimateFieldValue = fieldValues[fieldValues.length - 2];
        if (Array.isArray(lastFieldValue)) {
            // recursion
            return this.getNewSuggestions(lastFieldValue);
        }
        if (Array.isArray(penultimateFieldValue)) {
            if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'binary') {
                // returns filtered values
                return this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, SourceSuggestionType.VALUE);
            }
            // returns all binaries without any filter
            return this.getFilteredSuggestions('', SourceSuggestionType.BINARY);
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'value' && (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'unary') {
            // returns filtered values
            return this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, SourceSuggestionType.VALUE);
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'unary') {
            // returns all values without any filter
            return this.getFilteredSuggestions('', SourceSuggestionType.VALUE);
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string' && (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'value') {
            // returns all binaries without any filter
            return this.getFilteredSuggestions('', SourceSuggestionType.BINARY);
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string' &&
            (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'string' &&
            !(penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.value)) {
            // returns all values without any filter
            return this.getFilteredSuggestions('', SourceSuggestionType.STRING);
        }
        if (((penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'string' && !(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value)) ||
            ((penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'value' && !(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value)) ||
            (lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'binary') {
            // returns filtered binaries
            return this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, SourceSuggestionType.BINARY);
        }
        return this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type);
    };
    SourceField.prototype.loadFieldValues = function (newValue) {
        var fieldValues = [];
        var splittedValue = newValue.split(' ');
        var _loop_1 = function (splittedValueIndex) {
            var value = splittedValue[splittedValueIndex];
            var lastFieldValue = fieldValues[fieldValues.length - 1];
            if (lastFieldValue &&
                !Array.isArray(lastFieldValue) &&
                !lastFieldValue.value &&
                !value) {
                return "continue";
            }
            if (value.includes('!') && !!value.split('!')[1]) {
                var valueAfterUnaryOperator_1 = value.split('!')[1];
                var selector_1 = this_1.getAllSuggestions().find(function (s) { return s.value === valueAfterUnaryOperator_1; });
                if (!selector_1) {
                    fieldValues.push([
                        unarySuggestions[0],
                        { type: SourceSuggestionType.STRING, value: valueAfterUnaryOperator_1 },
                    ]);
                    return "continue";
                }
                fieldValues.push([unarySuggestions[0], selector_1]);
                return "continue";
            }
            var selector = this_1.getAllSuggestions().find(function (s) { return s.value === value; });
            if (selector) {
                fieldValues.push(selector);
                return "continue";
            }
            fieldValues.push({ type: SourceSuggestionType.STRING, value: value });
        };
        var this_1 = this;
        for (var splittedValueIndex in splittedValue) {
            _loop_1(splittedValueIndex);
        }
        var filteredSuggestions = this.getNewSuggestions(fieldValues);
        this.setState({
            fieldValues: fieldValues,
            activeSuggestion: 0,
            suggestions: filteredSuggestions,
        });
    };
    SourceField.prototype.scrollToSuggestion = function () {
        var _a, _b;
        var _c = this.state, activeSuggestion = _c.activeSuggestion, hideCaret = _c.hideCaret;
        (_b = (_a = this.suggestionList) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.children[activeSuggestion].scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'start',
        });
        if (!hideCaret) {
            this.setState({
                hideCaret: true,
            });
        }
    };
    SourceField.prototype.changeParentValue = function () {
        var _a, _b, _c, _d, _e, _f;
        var onChange = this.props.onChange;
        var fieldValues = this.state.fieldValues;
        var newValue = [];
        for (var index in fieldValues) {
            var fieldValue = fieldValues[index];
            if (Array.isArray(fieldValue)) {
                if (((_a = fieldValue[0]) === null || _a === void 0 ? void 0 : _a.value) || ((_b = fieldValue[1]) === null || _b === void 0 ? void 0 : _b.value)) {
                    newValue.push("" + ((_d = (_c = fieldValue[0]) === null || _c === void 0 ? void 0 : _c.value) !== null && _d !== void 0 ? _d : '') + ((_f = (_e = fieldValue[1]) === null || _e === void 0 ? void 0 : _e.value) !== null && _f !== void 0 ? _f : ''));
                }
                continue;
            }
            newValue.push(fieldValue.value);
        }
        onChange(newValue.join(' '));
    };
    SourceField.prototype.getNewFieldValues = function (suggestion) {
        var fieldValues = __spread(this.state.fieldValues);
        var lastFieldValue = fieldValues[fieldValues.length - 1];
        if (!defined(lastFieldValue)) {
            return [suggestion];
        }
        if (Array.isArray(lastFieldValue)) {
            fieldValues[fieldValues.length - 1] = [lastFieldValue[0], suggestion];
            return fieldValues;
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'unary') {
            fieldValues[fieldValues.length - 1] = [lastFieldValue, suggestion];
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string' && !(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value)) {
            fieldValues[fieldValues.length - 1] = suggestion;
        }
        return fieldValues;
    };
    SourceField.prototype.checkPossiblyRegExMatchExpression = function (value) {
        var isRegExMatchesSelected = this.props.isRegExMatchesSelected;
        var help = this.state.help;
        if (isRegExMatchesSelected) {
            if (help) {
                this.setState({ help: '' });
            }
            return;
        }
        var isMaybeRegExp = RegExp('^/.*/g?$').test(value);
        if (help) {
            if (!isMaybeRegExp) {
                this.setState({
                    help: defaultHelp,
                });
            }
            return;
        }
        if (isMaybeRegExp) {
            this.setState({
                help: t("You might want to change Data Type's value to 'Regex matches'"),
            });
        }
    };
    SourceField.prototype.toggleSuggestions = function (showSuggestions) {
        this.setState({ showSuggestions: showSuggestions });
    };
    SourceField.prototype.render = function () {
        var _this = this;
        var _a = this.props, error = _a.error, value = _a.value, onBlur = _a.onBlur;
        var _b = this.state, showSuggestions = _b.showSuggestions, suggestions = _b.suggestions, activeSuggestion = _b.activeSuggestion, hideCaret = _b.hideCaret, help = _b.help;
        return (<Wrapper ref={this.selectorField} hideCaret={hideCaret}>
        <StyledInput data-test-id="source-field" type="text" label={t('Source')} name="source" placeholder={t('Enter a custom attribute, variable or header name')} onChange={this.handleChange} autoComplete="off" value={value} error={error} help={help} onKeyDown={this.handleKeyDown} onBlur={onBlur} onFocus={this.handleFocus} inline={false} flexibleControlStateSize stacked required showHelpInTooltip/>
        {showSuggestions && suggestions.length > 0 && (<React.Fragment>
            <Suggestions ref={this.suggestionList} error={error} data-test-id="source-suggestions">
              {suggestions.slice(0, 50).map(function (suggestion, index) { return (<Suggestion key={suggestion.value} onClick={_this.handleClickSuggestionItem(suggestion)} active={index === activeSuggestion} tabIndex={-1}>
                  <TextOverflow>{suggestion.value}</TextOverflow>
                  {suggestion.description && (<SuggestionDescription>
                      (<TextOverflow>{suggestion.description}</TextOverflow>)
                    </SuggestionDescription>)}
                  {suggestion.examples && suggestion.examples.length > 0 && (<SourceSuggestionExamples examples={suggestion.examples} sourceName={suggestion.value}/>)}
                </Suggestion>); })}
            </Suggestions>
            <SuggestionsOverlay onClick={this.handleClickOutside}/>
          </React.Fragment>)}
      </Wrapper>);
    };
    return SourceField;
}(React.Component));
export default SourceField;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  width: 100%;\n  ", "\n"], ["\n  position: relative;\n  width: 100%;\n  ", "\n"])), function (p) { return p.hideCaret && "caret-color: transparent;"; });
var StyledInput = styled(InputField)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  z-index: 1002;\n  :focus {\n    outline: none;\n  }\n"], ["\n  z-index: 1002;\n  :focus {\n    outline: none;\n  }\n"])));
var Suggestions = styled('ul')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  width: ", ";\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n  box-shadow: 0 2px 0 rgba(37, 11, 54, 0.04);\n  border: 1px solid ", ";\n  border-radius: 0 0 ", " ", ";\n  background: ", ";\n  top: 63px;\n  left: 0;\n  z-index: 1002;\n  overflow: hidden;\n  max-height: 200px;\n  overflow-y: auto;\n"], ["\n  position: absolute;\n  width: ", ";\n  padding-left: 0;\n  list-style: none;\n  margin-bottom: 0;\n  box-shadow: 0 2px 0 rgba(37, 11, 54, 0.04);\n  border: 1px solid ", ";\n  border-radius: 0 0 ", " ", ";\n  background: ", ";\n  top: 63px;\n  left: 0;\n  z-index: 1002;\n  overflow: hidden;\n  max-height: 200px;\n  overflow-y: auto;\n"])), function (p) { return (p.error ? 'calc(100% - 34px)' : '100%'); }, function (p) { return p.theme.border; }, space(0.5), space(0.5), function (p) { return p.theme.background; });
var Suggestion = styled('li')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr max-content;\n  grid-gap: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  font-size: ", ";\n  cursor: pointer;\n  background: ", ";\n  :hover {\n    background: ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr max-content;\n  grid-gap: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  font-size: ", ";\n  cursor: pointer;\n  background: ", ";\n  :hover {\n    background: ",
    ";\n  }\n"])), space(1), function (p) { return p.theme.border; }, space(1), space(2), function (p) { return p.theme.fontSizeMedium; }, function (p) { return (p.active ? p.theme.backgroundSecondary : p.theme.background); }, function (p) {
    return p.active ? p.theme.backgroundSecondary : p.theme.backgroundSecondary;
});
var SuggestionDescription = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  overflow: hidden;\n  color: ", ";\n"], ["\n  display: flex;\n  overflow: hidden;\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var SuggestionsOverlay = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: fixed;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  z-index: 1001;\n"], ["\n  position: fixed;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  z-index: 1001;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=sourceField.jsx.map