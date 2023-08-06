import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import ButtonBar from 'app/components/buttonBar';
import Button from 'app/components/button';
import EventDataSection from 'app/components/events/eventDataSection';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueList';
import { t } from 'app/locale';
function getView(view, data) {
    switch (view) {
        case 'report':
            return <KeyValueList data={Object.entries(data)} isContextData/>;
        case 'raw':
            return <pre>{JSON.stringify({ 'csp-report': data }, null, 2)}</pre>;
        default:
            throw new TypeError("Invalid view: " + view);
    }
}
var GenericInterface = /** @class */ (function (_super) {
    __extends(GenericInterface, _super);
    function GenericInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            view: 'report',
            data: _this.props.data,
        };
        _this.toggleView = function (value) {
            _this.setState({
                view: value,
            });
        };
        return _this;
    }
    GenericInterface.prototype.render = function () {
        var _a = this.state, view = _a.view, data = _a.data;
        var type = this.props.type;
        var title = (<div>
        <ButtonBar merged active={view}>
          <Button barId="report" size="xsmall" onClick={this.toggleView.bind(this, 'report')}>
            {t('Report')}
          </Button>
          <Button barId="raw" size="xsmall" onClick={this.toggleView.bind(this, 'raw')}>
            {t('Raw')}
          </Button>
        </ButtonBar>
        <h3>{t('Report')}</h3>
      </div>);
        var children = getView(view, data);
        return (<EventDataSection type={type} title={title} wrapTitle={false}>
        {children}
      </EventDataSection>);
    };
    GenericInterface.propTypes = {
        type: PropTypes.string.isRequired,
        data: PropTypes.object.isRequired,
    };
    return GenericInterface;
}(Component));
export default GenericInterface;
//# sourceMappingURL=generic.jsx.map