/* eslint-disable react/prop-types */
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import ProjectsStore from 'app/stores/projectsStore';
/**
 * Higher order component that takes specificProjectSlugs and provides list of that projects from ProjectsStore
 */
var withProjectsSpecified = function (WrappedComponent) {
    return createReactClass({
        displayName: "withProjectsSpecified(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(ProjectsStore, 'onProjectUpdate')],
        getInitialState: function () {
            return ProjectsStore.getState(this.props.specificProjectSlugs);
        },
        onProjectUpdate: function () {
            this.setState(ProjectsStore.getState(this.props.specificProjectSlugs));
        },
        render: function () {
            return (<WrappedComponent {...this.props} projects={this.state.projects} loadingProjects={this.state.loading}/>);
        },
    });
};
export default withProjectsSpecified;
//# sourceMappingURL=withProjectsSpecified.jsx.map