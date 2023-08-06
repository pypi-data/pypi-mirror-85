import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import getDisplayName from 'app/utils/getDisplayName';
import TeamStore from 'app/stores/teamStore';
/**
 * Higher order component that uses TeamStore and provides a list of teams
 */
var withTeams = function (WrappedComponent) {
    return createReactClass({
        displayName: "withTeams(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(TeamStore, 'onTeamUpdate')],
        getInitialState: function () {
            return {
                teams: TeamStore.getAll(),
            };
        },
        onTeamUpdate: function () {
            this.setState({
                teams: TeamStore.getAll(),
            });
        },
        render: function () {
            return (<WrappedComponent {...this.props} teams={this.state.teams}/>);
        },
    });
};
export default withTeams;
//# sourceMappingURL=withTeams.jsx.map