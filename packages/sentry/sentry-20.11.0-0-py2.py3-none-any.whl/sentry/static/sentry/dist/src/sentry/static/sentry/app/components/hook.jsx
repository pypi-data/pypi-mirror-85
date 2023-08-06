import { __rest } from "tslib";
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import HookStore from 'app/stores/hookStore';
/**
 * Instead of accessing the HookStore directly, use this.
 *
 * If the hook slot needs to perform anything w/ the hooks, you can pass a
 * function as a child and you will receive an object with a `hooks` key
 *
 * Example:
 *
 *   <Hook name="my-hook">
 *     {({hooks}) => hooks.map(hook => (
 *       <Wrapper>{hook}</Wrapper>
 *     ))}
 *   </Hook>
 */
function Hook(_a) {
    var name = _a.name, props = __rest(_a, ["name"]);
    var HookComponent = createReactClass({
        displayName: "Hook(" + name + ")",
        mixins: [Reflux.listenTo(HookStore, 'handleHooks')],
        getInitialState: function () {
            return { hooks: HookStore.get(name).map(function (cb) { return cb(props); }) };
        },
        handleHooks: function (hookName, hooks) {
            // Make sure that the incoming hook update matches this component's hook name
            if (hookName !== name) {
                return;
            }
            this.setState({ hooks: hooks.map(function (cb) { return cb(props); }) });
        },
        render: function () {
            var children = props.children;
            if (!this.state.hooks || !this.state.hooks.length) {
                return null;
            }
            if (typeof children === 'function') {
                return children({ hooks: this.state.hooks });
            }
            return this.state.hooks;
        },
    });
    return <HookComponent />;
}
export default Hook;
//# sourceMappingURL=hook.jsx.map