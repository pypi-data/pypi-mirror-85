import { __extends, __makeTemplateObject, __read } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { css } from '@emotion/core';
import { t } from 'app/locale';
import { callIfFunction } from 'app/utils/callIfFunction';
import { DataSection } from 'app/components/events/styles';
import { IconAnchor } from 'app/icons/iconAnchor';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import space from 'app/styles/space';
var defaultProps = {
    wrapTitle: true,
    raw: false,
    isCentered: false,
    showPermalink: true,
};
var EventDataSection = /** @class */ (function (_super) {
    __extends(EventDataSection, _super);
    function EventDataSection() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventDataSection.prototype.componentDidMount = function () {
        if (location.hash) {
            var _a = __read(location.hash.split('#'), 2), hash = _a[1];
            try {
                var anchorElement = hash && document.querySelector('div#' + hash);
                if (anchorElement) {
                    anchorElement.scrollIntoView();
                }
            }
            catch (_b) {
                // Since we're blindly taking the hash from the url and shoving
                // it into a querySelector, it's possible that this may
                // raise an exception if the input is invalid. So let's just ignore
                // this instead of blowing up.
                // e.g. `document.querySelector('div#=')`
                // > Uncaught DOMException: Failed to execute 'querySelector' on 'Document': 'div#=' is not a valid selector.
            }
        }
    };
    EventDataSection.prototype.render = function () {
        var _a = this.props, children = _a.children, className = _a.className, type = _a.type, title = _a.title, toggleRaw = _a.toggleRaw, raw = _a.raw, wrapTitle = _a.wrapTitle, actions = _a.actions, isCentered = _a.isCentered, showPermalink = _a.showPermalink;
        var titleNode = wrapTitle ? <h3>{title}</h3> : title;
        return (<DataSection className={className || ''}>
        {title && (<SectionHeader id={type} isCentered={isCentered}>
            <Title>
              {showPermalink ? (<Permalink href={'#' + type} className="permalink">
                  <StyledIconAnchor />
                  {titleNode}
                </Permalink>) : (<div>{titleNode}</div>)}
            </Title>
            {type === 'extra' && (<ButtonBar merged active={raw ? 'raw' : 'formatted'}>
                <Button barId="formatted" size="xsmall" onClick={function () { return callIfFunction(toggleRaw, false); }}>
                  {t('Formatted')}
                </Button>
                <Button barId="raw" size="xsmall" onClick={function () { return callIfFunction(toggleRaw, true); }}>
                  {t('Raw')}
                </Button>
              </ButtonBar>)}
            {actions && <ActionContainer>{actions}</ActionContainer>}
          </SectionHeader>)}
        <SectionContents>{children}</SectionContents>
      </DataSection>);
    };
    EventDataSection.propTypes = {
        title: PropTypes.any,
        type: PropTypes.string.isRequired,
        wrapTitle: PropTypes.bool,
        toggleRaw: PropTypes.func,
        raw: PropTypes.bool,
        actions: PropTypes.node,
    };
    EventDataSection.defaultProps = defaultProps;
    return EventDataSection;
}(React.Component));
var Title = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledIconAnchor = styled(IconAnchor)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: none;\n  position: absolute;\n  top: 4px;\n  left: -22px;\n"], ["\n  display: none;\n  position: absolute;\n  top: 4px;\n  left: -22px;\n"])));
var Permalink = styled('a')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  :hover ", " {\n    display: block;\n    color: ", ";\n  }\n"], ["\n  :hover ", " {\n    display: block;\n    color: ", ";\n  }\n"])), StyledIconAnchor, function (p) { return p.theme.gray300; });
var SectionHeader = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  align-items: center;\n  margin-bottom: ", ";\n\n  > * {\n    margin-bottom: ", ";\n  }\n\n  & h3,\n  & h3 a {\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    color: ", ";\n  }\n\n  & h3 {\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    padding: ", " 0;\n    margin-bottom: 0;\n    text-transform: uppercase;\n  }\n\n  & small {\n    color: ", ";\n    font-size: ", ";\n    margin-right: ", ";\n    margin-left: ", ";\n\n    text-transform: none;\n  }\n  & small > span {\n    color: ", ";\n    border-bottom: 1px dotted ", ";\n    font-weight: normal;\n  }\n\n  @media (min-width: ", ") {\n    & > small {\n      margin-left: ", ";\n      display: inline-block;\n    }\n  }\n\n  ", "\n\n  >*:first-child {\n    position: relative;\n    flex-grow: 1;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  align-items: center;\n  margin-bottom: ", ";\n\n  > * {\n    margin-bottom: ", ";\n  }\n\n  & h3,\n  & h3 a {\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    color: ", ";\n  }\n\n  & h3 {\n    font-size: 14px;\n    font-weight: 600;\n    line-height: 1.2;\n    padding: ", " 0;\n    margin-bottom: 0;\n    text-transform: uppercase;\n  }\n\n  & small {\n    color: ", ";\n    font-size: ", ";\n    margin-right: ", ";\n    margin-left: ", ";\n\n    text-transform: none;\n  }\n  & small > span {\n    color: ", ";\n    border-bottom: 1px dotted ", ";\n    font-weight: normal;\n  }\n\n  @media (min-width: ", ") {\n    & > small {\n      margin-left: ", ";\n      display: inline-block;\n    }\n  }\n\n  ",
    "\n\n  >*:first-child {\n    position: relative;\n    flex-grow: 1;\n  }\n"])), space(2), space(0.5), function (p) { return p.theme.gray300; }, space(0.75), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeMedium; }, space(0.5), space(0.5), function (p) { return p.theme.textColor; }, function (p) { return p.theme.border; }, function (props) { return props.theme.breakpoints[2]; }, space(1), function (p) {
    return p.isCentered && css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n      align-items: center;\n      @media (max-width: ", ") {\n        display: block;\n      }\n    "], ["\n      align-items: center;\n      @media (max-width: ", ") {\n        display: block;\n      }\n    "])), p.theme.breakpoints[0]);
});
var SectionContents = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ActionContainer = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex-shrink: 0;\n  max-width: 100%;\n"], ["\n  flex-shrink: 0;\n  max-width: 100%;\n"])));
export default EventDataSection;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=eventDataSection.jsx.map