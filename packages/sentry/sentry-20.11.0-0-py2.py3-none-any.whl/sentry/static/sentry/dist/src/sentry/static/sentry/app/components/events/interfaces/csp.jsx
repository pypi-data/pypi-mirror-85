import { __assign, __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import ButtonBar from 'app/components/buttonBar';
import Button from 'app/components/button';
import EventDataSection from 'app/components/events/eventDataSection';
import CSPContent from 'app/components/events/interfaces/cspContent';
import CSPHelp from 'app/components/events/interfaces/cspHelp';
import { t } from 'app/locale';
function getView(view, data) {
    switch (view) {
        case 'report':
            return <CSPContent data={data}/>;
        case 'raw':
            return <pre>{JSON.stringify({ 'csp-report': data }, null, 2)}</pre>;
        case 'help':
            return <CSPHelp data={data}/>;
        default:
            throw new TypeError("Invalid view: " + view);
    }
}
var CspInterface = /** @class */ (function (_super) {
    __extends(CspInterface, _super);
    function CspInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { view: 'report' };
        _this.toggleView = function (value) {
            _this.setState({
                view: value,
            });
        };
        return _this;
    }
    CspInterface.prototype.render = function () {
        var view = this.state.view;
        var data = this.props.data;
        var cleanData = data.original_policy !== 'string'
            ? data
            : __assign(__assign({}, data), { 
                // Hide the report-uri since this is redundant and silly
                original_policy: data.original_policy.replace(/(;\s+)?report-uri [^;]+/, '') });
        var actions = (<ButtonBar merged active={view}>
        <Button barId="report" size="xsmall" onClick={this.toggleView.bind(this, 'report')}>
          {t('Report')}
        </Button>
        <Button barId="raw" size="xsmall" onClick={this.toggleView.bind(this, 'raw')}>
          {t('Raw')}
        </Button>
        <Button barId="help" size="xsmall" onClick={this.toggleView.bind(this, 'help')}>
          {t('Help')}
        </Button>
      </ButtonBar>);
        var children = getView(view, cleanData);
        return (<EventDataSection type="csp" title={<h3>{t('CSP Report')}</h3>} actions={actions} wrapTitle={false}>
        {children}
      </EventDataSection>);
    };
    CspInterface.propTypes = {
        data: PropTypes.object.isRequired,
    };
    return CspInterface;
}(React.Component));
export default CspInterface;
//# sourceMappingURL=csp.jsx.map