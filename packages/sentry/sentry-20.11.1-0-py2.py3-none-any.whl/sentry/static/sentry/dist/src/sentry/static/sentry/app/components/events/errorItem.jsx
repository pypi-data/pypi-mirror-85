import { __assign, __extends } from "tslib";
import mapKeys from 'lodash/mapKeys';
import moment from 'moment';
import startCase from 'lodash/startCase';
import isEmpty from 'lodash/isEmpty';
import React from 'react';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueList';
import { t } from 'app/locale';
import { EventError } from 'app/sentryTypes';
var keyMapping = {
    image_uuid: 'Debug ID',
    image_name: 'File Name',
    image_path: 'File Path',
};
var EventErrorItem = /** @class */ (function (_super) {
    __extends(EventErrorItem, _super);
    function EventErrorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.toggle = function () {
            _this.setState({ isOpen: !_this.state.isOpen });
        };
        return _this;
    }
    EventErrorItem.prototype.shouldComponentUpdate = function (_nextProps, nextState) {
        return this.state.isOpen !== nextState.isOpen;
    };
    EventErrorItem.prototype.cleanedData = function () {
        var data = __assign({}, this.props.error.data);
        // The name is rendered as path in front of the message
        if (typeof data.name === 'string') {
            delete data.name;
        }
        if (data.message === 'None') {
            // Python ensures a message string, but "None" doesn't make sense here
            delete data.message;
        }
        if (typeof data.image_path === 'string') {
            // Separate the image name for readability
            var separator = /^([a-z]:\\|\\\\)/i.test(data.image_path) ? '\\' : '/';
            var path = data.image_path.split(separator);
            data.image_name = path.splice(-1, 1)[0];
            data.image_path = path.length ? path.join(separator) + separator : '';
        }
        if (typeof data.server_time === 'string' && typeof data.sdk_time === 'string') {
            data.message = t('Adjusted timestamps by %s', moment
                .duration(moment.utc(data.server_time).diff(moment.utc(data.sdk_time)))
                .humanize());
        }
        return mapKeys(data, function (_value, key) { return t(keyMapping[key] || startCase(key)); });
    };
    EventErrorItem.prototype.renderPath = function () {
        var name = (this.props.error.data || {}).name;
        if (!name || typeof name !== 'string') {
            return null;
        }
        return (<React.Fragment>
        <strong>{name}</strong>
        {': '}
      </React.Fragment>);
    };
    EventErrorItem.prototype.render = function () {
        var error = this.props.error;
        var isOpen = this.state.isOpen;
        var data = this.cleanedData();
        return (<li>
        {this.renderPath()}
        {error.message}
        {!isEmpty(data) && (<small>
            {' '}
            <a style={{ marginLeft: 10 }} onClick={this.toggle}>
              {isOpen ? t('Collapse') : t('Expand')}
            </a>
          </small>)}
        {isOpen && <KeyValueList data={data} isContextData/>}
      </li>);
    };
    EventErrorItem.propTypes = {
        error: EventError.isRequired,
    };
    return EventErrorItem;
}(React.Component));
export default EventErrorItem;
//# sourceMappingURL=errorItem.jsx.map