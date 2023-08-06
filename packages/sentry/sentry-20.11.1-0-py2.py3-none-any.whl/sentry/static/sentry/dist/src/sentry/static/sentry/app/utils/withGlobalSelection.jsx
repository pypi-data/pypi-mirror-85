import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import GlobalSelectionStore from 'app/stores/globalSelectionStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Higher order component that uses GlobalSelectionStore and provides the
 * active project
 */
var withGlobalSelection = function (WrappedComponent) {
    return createReactClass({
        displayName: "withGlobalSelection(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(GlobalSelectionStore, 'onUpdate')],
        getInitialState: function () {
            return GlobalSelectionStore.get();
        },
        onUpdate: function (selection) {
            if (this.state !== selection) {
                this.setState(selection);
            }
        },
        render: function () {
            var _a = this.state, isReady = _a.isReady, selection = _a.selection;
            return (<WrappedComponent selection={selection} isGlobalSelectionReady={isReady} {...this.props}/>);
        },
    });
};
export default withGlobalSelection;
//# sourceMappingURL=withGlobalSelection.jsx.map