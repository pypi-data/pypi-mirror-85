import { __assign, __rest } from "tslib";
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import SentryAppComponentsStore from 'app/stores/sentryAppComponentsStore';
var withSentryAppComponents = function (WrappedComponent, _a) {
    var componentType = (_a === void 0 ? {} : _a).componentType;
    return createReactClass({
        displayName: "withSentryAppComponents(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.connect(SentryAppComponentsStore, 'components')],
        render: function () {
            var _a = this.props, components = _a.components, props = __rest(_a, ["components"]);
            return (<WrappedComponent {...__assign({ components: components !== null && components !== void 0 ? components : SentryAppComponentsStore.getComponentByType(componentType) }, props)}/>);
        },
    });
};
export default withSentryAppComponents;
//# sourceMappingURL=withSentryAppComponents.jsx.map