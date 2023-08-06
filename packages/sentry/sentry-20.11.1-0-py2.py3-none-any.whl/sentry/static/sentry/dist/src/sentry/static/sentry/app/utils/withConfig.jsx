import { __assign, __rest } from "tslib";
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import ConfigStore from 'app/stores/configStore';
/**
 * Higher order component that passes the config object to the wrapped component
 */
var withConfig = function (WrappedComponent) {
    return createReactClass({
        displayName: "withConfig(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(ConfigStore, 'onUpdate')],
        getInitialState: function () {
            return { config: ConfigStore.getConfig() };
        },
        onUpdate: function () {
            this.setState({ config: ConfigStore.getConfig() });
        },
        render: function () {
            var _a = this.props, config = _a.config, props = __rest(_a, ["config"]);
            return (<WrappedComponent {...__assign({ config: config !== null && config !== void 0 ? config : this.state.config }, props)}/>);
        },
    });
};
export default withConfig;
//# sourceMappingURL=withConfig.jsx.map