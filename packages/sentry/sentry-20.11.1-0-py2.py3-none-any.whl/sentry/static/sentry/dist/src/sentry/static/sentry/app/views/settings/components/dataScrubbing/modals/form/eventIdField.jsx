import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import Input from 'app/views/settings/components/forms/controls/input';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Field from 'app/views/settings/components/forms/field';
import EventIdFieldStatusIcon from './eventIdFieldStatusIcon';
import { EventIdStatus } from '../../types';
import { saveToSourceGroupData } from '../utils';
var EventIdField = /** @class */ (function (_super) {
    __extends(EventIdField, _super);
    function EventIdField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = __assign({}, _this.props.eventId);
        _this.handleChange = function (event) {
            var eventId = event.target.value.replace(/-/g, '').trim();
            if (eventId !== _this.state.value) {
                _this.setState({
                    value: eventId,
                    status: EventIdStatus.UNDEFINED,
                });
            }
        };
        _this.handleBlur = function (event) {
            event.preventDefault();
            if (_this.isEventIdValid()) {
                _this.props.onUpdateEventId(_this.state.value);
            }
        };
        _this.handleKeyDown = function (event) {
            var keyCode = event.keyCode;
            if (keyCode === 13 && _this.isEventIdValid()) {
                _this.props.onUpdateEventId(_this.state.value);
            }
        };
        _this.handleClickIconClose = function () {
            _this.setState({
                value: '',
                status: EventIdStatus.UNDEFINED,
            });
        };
        return _this;
    }
    EventIdField.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(prevProps.eventId, this.props.eventId)) {
            this.loadState();
        }
    };
    EventIdField.prototype.loadState = function () {
        this.setState(__assign({}, this.props.eventId));
    };
    EventIdField.prototype.getErrorMessage = function () {
        var status = this.state.status;
        switch (status) {
            case EventIdStatus.INVALID:
                return t('This event ID is invalid.');
            case EventIdStatus.ERROR:
                return t('An error occurred while fetching the suggestions based on this event ID.');
            case EventIdStatus.NOT_FOUND:
                return t('The chosen event ID was not found in projects you have access to.');
            default:
                return undefined;
        }
    };
    EventIdField.prototype.isEventIdValid = function () {
        var _a = this.state, value = _a.value, status = _a.status;
        if (value && value.length !== 32) {
            if (status !== EventIdStatus.INVALID) {
                saveToSourceGroupData({ value: value, status: status });
                this.setState({ status: EventIdStatus.INVALID });
            }
            return false;
        }
        return true;
    };
    EventIdField.prototype.render = function () {
        var disabled = this.props.disabled;
        var _a = this.state, value = _a.value, status = _a.status;
        return (<Field data-test-id="event-id-field" label={t('Event ID (Optional)')} help={t('Providing an event ID will automatically provide you a list of suggested sources')} inline={false} error={this.getErrorMessage()} flexibleControlStateSize stacked showHelpInTooltip>
        <FieldWrapper>
          <StyledInput type="text" name="eventId" disabled={disabled} value={value} placeholder={t('XXXXXXXXXXXXXX')} onChange={this.handleChange} onKeyDown={this.handleKeyDown} onBlur={this.handleBlur}/>
          <Status>
            <EventIdFieldStatusIcon onClickIconClose={this.handleClickIconClose} status={status}/>
          </Status>
        </FieldWrapper>
      </Field>);
    };
    return EventIdField;
}(React.Component));
export default EventIdField;
var StyledInput = styled(Input)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  font-weight: 400;\n  input {\n    padding-right: ", ";\n  }\n  margin-bottom: 0;\n"], ["\n  flex: 1;\n  font-weight: 400;\n  input {\n    padding-right: ", ";\n  }\n  margin-bottom: 0;\n"])), space(1.5));
var Status = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 40px;\n  position: absolute;\n  right: ", ";\n  top: 0;\n  display: flex;\n  align-items: center;\n"], ["\n  height: 40px;\n  position: absolute;\n  right: ", ";\n  top: 0;\n  display: flex;\n  align-items: center;\n"])), space(1.5));
var FieldWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: center;\n"], ["\n  position: relative;\n  display: flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventIdField.jsx.map