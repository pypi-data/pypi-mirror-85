import Registry from 'app/plugins/registry';
import BasePlugin from 'app/plugins/basePlugin';
import DefaultIssuePlugin from 'app/plugins/defaultIssuePlugin';
import SessionStackPlugin from './sessionstack';
import SessionStackContextType from './sessionstack/contexts/sessionstack';
import Jira from './jira';
var contexts = {};
var registry = new Registry();
// Register legacy plugins
// Sessionstack
registry.add('sessionstack', SessionStackPlugin);
contexts.sessionstack = SessionStackContextType;
// Jira
registry.add('jira', Jira);
export { BasePlugin, registry, DefaultIssuePlugin };
var add = registry.add.bind(registry);
var get = registry.get.bind(registry);
var isLoaded = registry.isLoaded.bind(registry);
var load = registry.load.bind(registry);
export default {
    BasePlugin: BasePlugin,
    DefaultIssuePlugin: DefaultIssuePlugin,
    add: add,
    addContext: function (id, component) {
        contexts[id] = component;
    },
    contexts: contexts,
    get: get,
    isLoaded: isLoaded,
    load: load,
};
//# sourceMappingURL=index.jsx.map