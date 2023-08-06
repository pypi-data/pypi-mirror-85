import { __extends } from "tslib";
import React from 'react';
import moment from 'moment';
import Modal from 'react-bootstrap/lib/Modal';
import { sprintf } from 'sprintf-js';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import { IconWarning } from 'app/icons';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
var defaultProps = {
    label: t('Ignore this issue until \u2026'),
};
var CustomIgnoreDurationModal = /** @class */ (function (_super) {
    __extends(CustomIgnoreDurationModal, _super);
    function CustomIgnoreDurationModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dateWarning: false,
        };
        _this.snoozeDateInputRef = React.createRef();
        _this.snoozeTimeInputRef = React.createRef();
        _this.selectedIgnoreMinutes = function () {
            var _a, _b;
            var dateStr = (_a = _this.snoozeDateInputRef.current) === null || _a === void 0 ? void 0 : _a.value; // YYYY-MM-DD
            var timeStr = (_b = _this.snoozeTimeInputRef.current) === null || _b === void 0 ? void 0 : _b.value; // HH:MM
            if (dateStr && timeStr) {
                var selectedDate = moment.utc(dateStr + ' ' + timeStr);
                if (selectedDate.isValid()) {
                    var now = moment.utc();
                    return selectedDate.diff(now, 'minutes');
                }
            }
            return 0;
        };
        _this.snoozeClicked = function () {
            var minutes = _this.selectedIgnoreMinutes();
            _this.setState({
                dateWarning: minutes <= 0,
            });
            if (minutes > 0) {
                _this.props.onSelected({ ignoreDuration: minutes });
            }
        };
        return _this;
    }
    CustomIgnoreDurationModal.prototype.render = function () {
        // Give the user a sane starting point to select a date
        // (prettier than the empty date/time inputs):
        var defaultDate = new Date();
        defaultDate.setDate(defaultDate.getDate() + 14);
        defaultDate.setSeconds(0);
        defaultDate.setMilliseconds(0);
        var defaultDateVal = sprintf('%d-%02d-%02d', defaultDate.getUTCFullYear(), defaultDate.getUTCMonth() + 1, defaultDate.getUTCDate());
        var defaultTimeVal = sprintf('%02d:00', defaultDate.getUTCHours());
        var _a = this.props, show = _a.show, onCanceled = _a.onCanceled, label = _a.label;
        return (<Modal show={show} animation={false} onHide={onCanceled}>
        <Modal.Header>
          <h4>{label}</h4>
        </Modal.Header>
        <Modal.Body>
          <form className="form-horizontal">
            <div className="control-group">
              <h6 className="nav-header">{t('Date')}</h6>
              <input className="form-control" type="date" id="snooze-until-date" defaultValue={defaultDateVal} ref={this.snoozeDateInputRef} required style={{ padding: '0 10px' }}/>
            </div>
            <div className="control-group m-b-1">
              <h6 className="nav-header">{t('Time (UTC)')}</h6>
              <input className="form-control" type="time" id="snooze-until-time" defaultValue={defaultTimeVal} ref={this.snoozeTimeInputRef} style={{ padding: '0 10px' }} required/>
            </div>
          </form>
        </Modal.Body>
        {this.state.dateWarning && (<Alert icon={<IconWarning size="md"/>} type="error">
            {t('Please enter a valid date in the future')}
          </Alert>)}
        <Modal.Footer>
          <ButtonBar gap={1}>
            <Button type="button" priority="default" onClick={this.props.onCanceled}>
              {t('Cancel')}
            </Button>
            <Button type="button" priority="primary" onClick={this.snoozeClicked}>
              {t('Ignore')}
            </Button>
          </ButtonBar>
        </Modal.Footer>
      </Modal>);
    };
    CustomIgnoreDurationModal.defaultProps = defaultProps;
    return CustomIgnoreDurationModal;
}(React.Component));
export default CustomIgnoreDurationModal;
//# sourceMappingURL=customIgnoreDurationModal.jsx.map