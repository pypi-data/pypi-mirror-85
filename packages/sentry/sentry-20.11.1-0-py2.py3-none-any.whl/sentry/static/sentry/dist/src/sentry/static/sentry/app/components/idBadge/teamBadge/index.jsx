import isEqual from 'lodash/isEqual';
import createReactClass from 'create-react-class';
import React from 'react';
import Reflux from 'reflux';
import SentryTypes from 'app/sentryTypes';
import TeamStore from 'app/stores/teamStore';
import Badge from './badge';
var TeamBadgeContainer = createReactClass({
    displayName: 'TeamBadgeContainer',
    propTypes: {
        team: SentryTypes.Team.isRequired,
    },
    mixins: [Reflux.listenTo(TeamStore, 'onTeamStoreUpdate')],
    getInitialState: function () {
        return {
            team: this.props.team,
        };
    },
    componentWillReceiveProps: function (nextProps) {
        if (this.state.team === nextProps.team) {
            return;
        }
        if (isEqual(this.state.team, nextProps.team)) {
            return;
        }
        this.setState({ team: nextProps.team });
    },
    onTeamStoreUpdate: function (updatedTeam) {
        if (!updatedTeam.has(this.state.team.id)) {
            return;
        }
        var team = TeamStore.getById(this.state.team.id);
        if (!team || isEqual(team.avatar, this.state.team.avatar)) {
            return;
        }
        this.setState({ team: team });
    },
    render: function () {
        return <Badge {...this.props} team={this.state.team}/>;
    },
});
export default TeamBadgeContainer;
//# sourceMappingURL=index.jsx.map