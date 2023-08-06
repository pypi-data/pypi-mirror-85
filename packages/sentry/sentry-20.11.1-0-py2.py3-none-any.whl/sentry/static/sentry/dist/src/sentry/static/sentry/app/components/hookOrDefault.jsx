import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import HookStore from 'app/stores/hookStore';
/**
 * Use this instead of the usual ternery operator when using getsentry hooks.
 * So in lieu of:
 *
 *  HookStore.get('component:org-auth-view').length
 *   ? HookStore.get('component:org-auth-view')[0]()
 *   : OrganizationAuth
 *
 * do this instead:
 *
 *   const HookedOrganizationAuth = HookOrDefault({
 *     hookName:'component:org-auth-view',
 *     defaultComponent: OrganizationAuth,
 *   })
 *
 * Note, you will need to add the hookstore function in getsentry [0] first and
 * then register tye types [2] and validHookName [1] in sentry.
 *
 * [0] /getsentry/static/getsentry/gsApp/registerHooks.jsx
 * [1] /sentry/app/stores/hookStore.tsx
 * [2] /sentry/app/types/hooks.ts
 */
function HookOrDefault(_a) {
    var hookName = _a.hookName, defaultComponent = _a.defaultComponent, defaultComponentPromise = _a.defaultComponentPromise, params = _a.params;
    return createReactClass({
        displayName: "HookOrDefaultComponent(" + hookName + ")",
        mixins: [Reflux.listenTo(HookStore, 'handleHooks')],
        getInitialState: function () {
            return { hooks: HookStore.get(hookName) };
        },
        handleHooks: function (hookNameFromStore, hooks) {
            // Make sure that the incoming hook update matches this component's hook name
            if (hookName !== hookNameFromStore) {
                return;
            }
            this.setState({ hooks: hooks });
        },
        getDefaultComponent: function () {
            // If `defaultComponentPromise` is passed, then return a Suspended component
            if (defaultComponentPromise) {
                var Component_1 = React.lazy(defaultComponentPromise);
                return function (props) { return (<React.Suspense fallback={null}>
            <Component_1 {...props}/>
          </React.Suspense>); };
            }
            return defaultComponent;
        },
        render: function () {
            var hookExists = this.state.hooks && this.state.hooks.length;
            var HookComponent = hookExists && this.state.hooks[0]({ params: params })
                ? this.state.hooks[0]({ params: params })
                : this.getDefaultComponent();
            return <HookComponent {...this.props}/>;
        },
    });
}
export default HookOrDefault;
//# sourceMappingURL=hookOrDefault.jsx.map