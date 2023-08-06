import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import Modal from 'react-bootstrap/lib/Modal';
import { t } from 'app/locale';
var SnoozeTimes;
(function (SnoozeTimes) {
    // all values in minutes
    SnoozeTimes[SnoozeTimes["THIRTY_MINUTES"] = 30] = "THIRTY_MINUTES";
    SnoozeTimes[SnoozeTimes["TWO_HOURS"] = 120] = "TWO_HOURS";
    SnoozeTimes[SnoozeTimes["TWENTY_FOUR_HOURS"] = 1440] = "TWENTY_FOUR_HOURS";
})(SnoozeTimes || (SnoozeTimes = {}));
var SnoozeAction = /** @class */ (function (_super) {
    __extends(SnoozeAction, _super);
    function SnoozeAction() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isModalOpen: false,
        };
        _this.toggleModal = function () {
            if (_this.props.disabled) {
                return;
            }
            _this.setState({
                isModalOpen: !_this.state.isModalOpen,
            });
        };
        _this.closeModal = function () {
            _this.setState({ isModalOpen: false });
        };
        _this.onSnooze = function (duration) {
            _this.props.onSnooze(duration);
            _this.closeModal();
        };
        return _this;
    }
    SnoozeAction.prototype.render = function () {
        return (<React.Fragment>
        <a title={this.props.tooltip} className={this.props.className} onClick={this.toggleModal}>
          <span>{t('zZz')}</span>
        </a>
        <Modal show={this.state.isModalOpen} title={t('Please confirm')} animation={false} onHide={this.closeModal} bsSize="sm">
          <div className="modal-body">
            <h5>{t('How long should we ignore this issue?')}</h5>
            <ul className="nav nav-stacked nav-pills">
              <li>
                <a onClick={this.onSnooze.bind(this, SnoozeTimes.THIRTY_MINUTES)}>
                  {t('30 minutes')}
                </a>
              </li>
              <li>
                <a onClick={this.onSnooze.bind(this, SnoozeTimes.TWO_HOURS)}>
                  {t('2 hours')}
                </a>
              </li>
              <li>
                <a onClick={this.onSnooze.bind(this, SnoozeTimes.TWENTY_FOUR_HOURS)}>
                  {t('24 hours')}
                </a>
              </li>
              
              <li>
                <a onClick={this.onSnooze.bind(this, undefined)}>{t('Forever')}</a>
              </li>
            </ul>
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-default" onClick={this.closeModal}>
              {t('Cancel')}
            </button>
          </div>
        </Modal>
      </React.Fragment>);
    };
    SnoozeAction.propTypes = {
        disabled: PropTypes.bool,
        onSnooze: PropTypes.func.isRequired,
        tooltip: PropTypes.string,
    };
    return SnoozeAction;
}(React.Component));
export default SnoozeAction;
//# sourceMappingURL=snoozeAction.jsx.map