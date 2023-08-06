import React from 'react';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { ThemeProvider } from 'emotion-theming';
import AlertStore from 'app/stores/alertStore';
import theme from 'app/utils/theme';
import AlertMessage from './alertMessage';
var Alerts = createReactClass({
    displayName: 'Alerts',
    mixins: [Reflux.connect(AlertStore, 'alerts')],
    getInitialState: function () {
        return {
            alerts: [],
        };
    },
    render: function () {
        var className = this.props.className;
        var alerts = this.state.alerts;
        return (<ThemeProvider theme={theme}>
        <div className={className}>
          {alerts.map(function (alert, index) { return (<AlertMessage alert={alert} key={alert.id + "-" + index} system/>); })}
        </div>
      </ThemeProvider>);
    },
});
export default Alerts;
//# sourceMappingURL=systemAlerts.jsx.map