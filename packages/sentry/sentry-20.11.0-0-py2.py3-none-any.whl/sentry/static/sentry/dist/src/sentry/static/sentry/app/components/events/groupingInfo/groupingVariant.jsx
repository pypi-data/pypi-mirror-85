import { __extends, __makeTemplateObject, __read, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import capitalize from 'lodash/capitalize';
import { t } from 'app/locale';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueList';
import { EventGroupVariantType } from 'app/types';
import ButtonBar from 'app/components/buttonBar';
import Button from 'app/components/button';
import { IconCheckmark, IconClose } from 'app/icons';
import space from 'app/styles/space';
import Tooltip from 'app/components/tooltip';
import QuestionTooltip from 'app/components/questionTooltip';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import { hasNonContributingComponent } from './utils';
import GroupingComponent from './groupingComponent';
var GroupVariant = /** @class */ (function (_super) {
    __extends(GroupVariant, _super);
    function GroupVariant() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showNonContributing: false,
        };
        _this.handleShowNonContributing = function () {
            _this.setState({ showNonContributing: true });
        };
        _this.handleHideNonContributing = function () {
            _this.setState({ showNonContributing: false });
        };
        return _this;
    }
    GroupVariant.prototype.getVariantData = function () {
        var _a, _b;
        var _c = this.props, variant = _c.variant, showGroupingConfig = _c.showGroupingConfig;
        var data = [];
        var component;
        if (!this.state.showNonContributing && variant.hash === null) {
            return [data, component];
        }
        if (variant.hash !== null) {
            data.push([
                t('Hash'),
                <TextWithQuestionTooltip key="hash">
          <Hash>{variant.hash}</Hash>
          <QuestionTooltip size="xs" position="top" title={t('Events with the same hash are grouped together')}/>
        </TextWithQuestionTooltip>,
            ]);
        }
        if (variant.hashMismatch) {
            data.push([
                t('Hash mismatch'),
                t('hashing algorithm produced a hash that does not match the event'),
            ]);
        }
        switch (variant.type) {
            case EventGroupVariantType.COMPONENT:
                component = variant.component;
                data.push([
                    t('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <QuestionTooltip size="xs" position="top" title={t('Uses a complex grouping algorithm taking event data into account')}/>
          </TextWithQuestionTooltip>,
                ]);
                if (showGroupingConfig && ((_a = variant.config) === null || _a === void 0 ? void 0 : _a.id)) {
                    data.push([t('Grouping Config'), variant.config.id]);
                }
                break;
            case EventGroupVariantType.CUSTOM_FINGERPRINT:
                data.push([
                    t('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <QuestionTooltip size="xs" position="top" title={t('Overrides the default grouping by a custom fingerprinting rule')}/>
          </TextWithQuestionTooltip>,
                ]);
                if (variant.values) {
                    data.push([t('Fingerprint values'), variant.values]);
                }
                break;
            case EventGroupVariantType.SALTED_COMPONENT:
                component = variant.component;
                data.push([
                    t('Type'),
                    <TextWithQuestionTooltip key="type">
            {variant.type}
            <QuestionTooltip size="xs" position="top" title={t('Uses a complex grouping algorithm taking event data and a fingerprint into account')}/>
          </TextWithQuestionTooltip>,
                ]);
                if (variant.values) {
                    data.push([t('Fingerprint values'), variant.values]);
                }
                if (showGroupingConfig && ((_b = variant.config) === null || _b === void 0 ? void 0 : _b.id)) {
                    data.push([t('Grouping Config'), variant.config.id]);
                }
                break;
            default:
                break;
        }
        if (component) {
            data.push([
                t('Grouping'),
                <GroupingTree key={component.id}>
          <GroupingComponent component={component} showNonContributing={this.state.showNonContributing}/>
        </GroupingTree>,
            ]);
        }
        return [data, component];
    };
    GroupVariant.prototype.renderTitle = function () {
        var _a, _b, _c;
        var variant = this.props.variant;
        var isContributing = variant.hash !== null;
        var title;
        if (isContributing) {
            title = t('Contributing variant');
        }
        else {
            var hint = (_a = variant.component) === null || _a === void 0 ? void 0 : _a.hint;
            if (hint) {
                title = t('Non-contributing variant: %s', hint);
            }
            else {
                title = t('Non-contributing variant');
            }
        }
        return (<Tooltip title={title}>
        <VariantTitle>
          <ContributionIcon isContributing={isContributing}/>
          {t('By')}{' '}
          {(_c = (_b = variant.description) === null || _b === void 0 ? void 0 : _b.split(' ').map(function (i) { return capitalize(i); }).join(' ')) !== null && _c !== void 0 ? _c : t('Nothing')}
        </VariantTitle>
      </Tooltip>);
    };
    GroupVariant.prototype.renderContributionToggle = function () {
        var showNonContributing = this.state.showNonContributing;
        return (<ContributingToggle merged active={showNonContributing ? 'all' : 'relevant'}>
        <Button barId="relevant" size="xsmall" onClick={this.handleHideNonContributing}>
          {t('Contributing values')}
        </Button>
        <Button barId="all" size="xsmall" onClick={this.handleShowNonContributing}>
          {t('All values')}
        </Button>
      </ContributingToggle>);
    };
    GroupVariant.prototype.render = function () {
        var _a = __read(this.getVariantData(), 2), data = _a[0], component = _a[1];
        return (<VariantWrapper>
        <Header>
          {this.renderTitle()}
          {hasNonContributingComponent(component) && this.renderContributionToggle()}
        </Header>

        <KeyValueList data={data} isContextData isSorted={false}/>
      </VariantWrapper>);
    };
    return GroupVariant;
}(React.Component));
var VariantWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
var VariantTitle = styled('h5')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  margin: 0;\n  display: flex;\n  align-items: center;\n"], ["\n  font-size: ", ";\n  margin: 0;\n  display: flex;\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeMedium; });
var ContributionIcon = styled(function (_a) {
    var isContributing = _a.isContributing, p = __rest(_a, ["isContributing"]);
    return isContributing ? (<IconCheckmark size="sm" isCircled color="green300" {...p}/>) : (<IconClose size="sm" isCircled color="red" {...p}/>);
})(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var ContributingToggle = styled(ButtonBar)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  justify-content: flex-end;\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  justify-content: flex-end;\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(0.5));
var GroupingTree = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: #2f2936;\n"], ["\n  color: #2f2936;\n"])));
var TextWithQuestionTooltip = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: max-content min-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: max-content min-content;\n  grid-gap: ", ";\n"])), space(0.5));
var Hash = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    ", ";\n    width: 210px;\n  }\n"], ["\n  @media (max-width: ", ") {\n    ", ";\n    width: 210px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, overflowEllipsis);
export default GroupVariant;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=groupingVariant.jsx.map