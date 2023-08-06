import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import MemberListStore from 'app/stores/memberListStore';
import Button from 'app/components/button';
import SelectField from 'app/components/forms/selectField';
import TextOverflow from 'app/components/textOverflow';
import { IconAdd, IconChevron } from 'app/icons';
import Input from 'app/views/settings/components/forms/controls/input';
import { addErrorMessage } from 'app/actionCreators/indicator';
import SelectOwners from 'app/views/settings/project/projectOwnership/selectOwners';
import space from 'app/styles/space';
var initialState = {
    text: '',
    tagName: '',
    type: 'path',
    owners: [],
    isValid: false,
};
function getMatchPlaceholder(type) {
    switch (type) {
        case 'path':
            return 'src/example/*';
        case 'url':
            return 'https://example.com/settings/*';
        case 'tag':
            return 'tag-value';
        default:
            return '';
    }
}
var RuleBuilder = /** @class */ (function (_super) {
    __extends(RuleBuilder, _super);
    function RuleBuilder() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.checkIsValid = function () {
            _this.setState(function (state) { return ({
                isValid: !!state.text && state.owners && !!state.owners.length,
            }); });
        };
        _this.handleTypeChange = function (val) {
            _this.setState({ type: val });
            _this.checkIsValid();
        };
        _this.handleTagNameChangeValue = function (e) {
            _this.setState({ tagName: e.target.value }, _this.checkIsValid);
        };
        _this.handleChangeValue = function (e) {
            _this.setState({ text: e.target.value });
            _this.checkIsValid();
        };
        _this.handleChangeOwners = function (owners) {
            _this.setState({ owners: owners });
            _this.checkIsValid();
        };
        _this.handleAddRule = function () {
            var _a = _this.state, type = _a.type, text = _a.text, tagName = _a.tagName, owners = _a.owners, isValid = _a.isValid;
            if (!isValid) {
                addErrorMessage('A rule needs a type, a value, and one or more issue owners.');
                return;
            }
            var ownerText = owners
                .map(function (owner) {
                var _a;
                return owner.actor.type === 'team'
                    ? "#" + owner.actor.name
                    : (_a = MemberListStore.getById(owner.actor.id)) === null || _a === void 0 ? void 0 : _a.email;
            })
                .join(' ');
            var quotedText = text.match(/\s/) ? "\"" + text + "\"" : text;
            var rule = (type === 'tag' ? "tags." + tagName : type) + ":" + quotedText + " " + ownerText;
            _this.props.onAddRule(rule);
            _this.setState(initialState);
        };
        _this.handleSelectCandidate = function (text, type) {
            _this.setState({ text: text, type: type });
            _this.checkIsValid();
        };
        return _this;
    }
    RuleBuilder.prototype.render = function () {
        var _this = this;
        var _a = this.props, urls = _a.urls, paths = _a.paths, disabled = _a.disabled, project = _a.project, organization = _a.organization;
        var _b = this.state, type = _b.type, text = _b.text, tagName = _b.tagName, owners = _b.owners, isValid = _b.isValid;
        return (<React.Fragment>
        {(paths || urls) && (<Candidates>
            {paths &&
            paths.map(function (v) { return (<RuleCandidate key={v} onClick={function () { return _this.handleSelectCandidate(v, 'path'); }}>
                  <StyledIconAdd isCircled/>
                  <StyledTextOverflow>{v}</StyledTextOverflow>
                  <TypeHint>[PATH]</TypeHint>
                </RuleCandidate>); })}
            {urls &&
            urls.map(function (v) { return (<RuleCandidate key={v} onClick={function () { return _this.handleSelectCandidate(v, 'url'); }}>
                  <StyledIconAdd isCircled/>
                  <StyledTextOverflow>{v}</StyledTextOverflow>
                  <TypeHint>[URL]</TypeHint>
                </RuleCandidate>); })}
          </Candidates>)}
        <BuilderBar>
          <BuilderSelect deprecatedSelectControl name="select-type" value={type} onChange={this.handleTypeChange} options={[
            { value: 'path', label: t('Path') },
            { value: 'tag', label: t('Tag') },
            { value: 'url', label: t('URL') },
        ]} style={{ width: 140 }} clearable={false} disabled={disabled}/>
          {type === 'tag' && (<BuilderTagNameInput value={tagName} onChange={this.handleTagNameChangeValue} disabled={disabled} placeholder="tag-name"/>)}
          <BuilderInput value={text} onChange={this.handleChangeValue} disabled={disabled} placeholder={getMatchPlaceholder(type)}/>
          <Divider direction="right"/>
          <SelectOwnersWrapper>
            <SelectOwners organization={organization} project={project} value={owners} onChange={this.handleChangeOwners} disabled={disabled}/>
          </SelectOwnersWrapper>

          <AddButton priority="primary" disabled={!isValid} onClick={this.handleAddRule} icon={<IconAdd isCircled/>} size="small"/>
        </BuilderBar>
      </React.Fragment>);
    };
    return RuleBuilder;
}(React.Component));
var Candidates = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 10px;\n"], ["\n  margin-bottom: 10px;\n"])));
var TypeHint = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.border; });
var StyledTextOverflow = styled(TextOverflow)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var RuleCandidate = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-family: ", ";\n  border: 1px solid ", ";\n  background-color: #f8fafd;\n  padding-left: 5px;\n  margin-bottom: 3px;\n  cursor: pointer;\n  overflow: hidden;\n  display: flex;\n  align-items: center;\n"], ["\n  font-family: ", ";\n  border: 1px solid ", ";\n  background-color: #f8fafd;\n  padding-left: 5px;\n  margin-bottom: 3px;\n  cursor: pointer;\n  overflow: hidden;\n  display: flex;\n  align-items: center;\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.border; });
var StyledIconAdd = styled(IconAdd)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  margin-right: 5px;\n  flex-shrink: 0;\n"], ["\n  color: ", ";\n  margin-right: 5px;\n  flex-shrink: 0;\n"])), function (p) { return p.theme.border; });
var BuilderBar = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  height: 40px;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  height: 40px;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(2));
var BuilderSelect = styled(SelectField)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-right: ", ";\n  width: 50px;\n  flex-shrink: 0;\n"], ["\n  margin-right: ", ";\n  width: 50px;\n  flex-shrink: 0;\n"])), space(1.5));
var BuilderInput = styled(Input)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  padding: ", ";\n  line-height: 19px;\n  margin-right: ", ";\n"], ["\n  padding: ", ";\n  line-height: 19px;\n  margin-right: ", ";\n"])), space(1), space(0.5));
var BuilderTagNameInput = styled(Input)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  padding: ", ";\n  line-height: 19px;\n  margin-right: ", ";\n  width: 200px;\n"], ["\n  padding: ", ";\n  line-height: 19px;\n  margin-right: ", ";\n  width: 200px;\n"])), space(1), space(0.5));
var Divider = styled(IconChevron)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  color: ", ";\n  flex-shrink: 0;\n  margin-right: 5px;\n"], ["\n  color: ", ";\n  flex-shrink: 0;\n  margin-right: 5px;\n"])), function (p) { return p.theme.border; });
var SelectOwnersWrapper = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-right: ", ";\n"])), space(1));
var AddButton = styled(Button)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  padding: ", "; /* this sizes the button up to align with the inputs */\n"], ["\n  padding: ", "; /* this sizes the button up to align with the inputs */\n"])), space(0.5));
export default RuleBuilder;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=ruleBuilder.jsx.map