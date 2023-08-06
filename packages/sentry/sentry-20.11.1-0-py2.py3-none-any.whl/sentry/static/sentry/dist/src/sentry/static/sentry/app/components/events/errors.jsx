import { __extends, __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import uniqWith from 'lodash/uniqWith';
import isEqual from 'lodash/isEqual';
import { css } from '@emotion/core';
import Button from 'app/components/button';
import EventErrorItem from 'app/components/events/errorItem';
import { IconWarning } from 'app/icons';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import { BannerContainer, BannerSummary } from './styles';
var MAX_ERRORS = 100;
var EventErrors = /** @class */ (function (_super) {
    __extends(EventErrors, _super);
    function EventErrors() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.toggle = function () {
            _this.setState(function (state) { return ({ isOpen: !state.isOpen }); });
        };
        _this.uniqueErrors = function (errors) { return uniqWith(errors, isEqual); };
        return _this;
    }
    EventErrors.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (this.state.isOpen !== nextState.isOpen) {
            return true;
        }
        return this.props.event.id !== nextProps.event.id;
    };
    EventErrors.prototype.render = function () {
        var event = this.props.event;
        // XXX: uniqueErrors is not performant with large datasets
        var errors = event.errors.length > MAX_ERRORS ? event.errors : this.uniqueErrors(event.errors);
        var numErrors = errors.length;
        var isOpen = this.state.isOpen;
        return (<StyledBanner priority="danger">
        <BannerSummary>
          <StyledIconWarning />
          <span>
            {tn('There was %s error encountered while processing this event', 'There were %s errors encountered while processing this event', numErrors)}
          </span>
          <StyledButton data-test-id="event-error-toggle" priority="link" onClick={this.toggle}>
            {isOpen ? t('Hide') : t('Show')}
          </StyledButton>
        </BannerSummary>
        <ErrorList data-test-id="event-error-details" style={{ display: isOpen ? 'block' : 'none' }}>
          {errors.map(function (error, errorIdx) { return (<EventErrorItem key={errorIdx} error={error}/>); })}
        </ErrorList>
      </StyledBanner>);
    };
    EventErrors.propTypes = {
        event: PropTypes.object.isRequired,
    };
    return EventErrors;
}(React.Component));
var linkStyle = function (_a) {
    var theme = _a.theme;
    return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  font-weight: bold;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), theme.subText, theme.textColor);
};
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), linkStyle);
var StyledBanner = styled(BannerContainer)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: -1px;\n  a {\n    ", "\n  }\n"], ["\n  margin-top: -1px;\n  a {\n    ", "\n  }\n"])), linkStyle);
var StyledIconWarning = styled(IconWarning)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.red300; });
// TODO(theme) don't use a custom pink
var customPink = '#e7c0bc';
var ErrorList = styled('ul')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  margin: 0 ", " 0 ", ";\n  padding: ", " 0 ", " ", ";\n\n  li {\n    margin-bottom: ", ";\n    word-break: break-word;\n  }\n\n  pre {\n    background: #f9eded;\n    color: #381618;\n    margin: ", " 0 0;\n  }\n"], ["\n  border-top: 1px solid ", ";\n  margin: 0 ", " 0 ", ";\n  padding: ", " 0 ", " ", ";\n\n  li {\n    margin-bottom: ", ";\n    word-break: break-word;\n  }\n\n  pre {\n    background: #f9eded;\n    color: #381618;\n    margin: ", " 0 0;\n  }\n"])), customPink, space(3), space(4), space(1), space(0.5), space(4), space(0.75), space(0.5));
export default EventErrors;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=errors.jsx.map