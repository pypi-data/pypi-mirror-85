import React from 'react';
import PropTypes from 'prop-types';
import { tct } from 'app/locale';
import ScoreBar from 'app/components/scoreBar';
import Tooltip from 'app/components/tooltip';
import theme from 'app/utils/theme';
function UserMisery(props) {
    var bars = props.bars, barHeight = props.barHeight, miserableUsers = props.miserableUsers, miseryLimit = props.miseryLimit, totalUsers = props.totalUsers;
    var palette = new Array(bars).fill(theme.purple300);
    var rawScore = Math.floor((miserableUsers / Math.max(totalUsers, 1)) * palette.length);
    var adjustedScore = rawScore > 0 ? rawScore : miserableUsers > 0 ? 1 : 0;
    var miseryPercentage = ((100 * miserableUsers) / Math.max(totalUsers, 1)).toFixed(2);
    var title = tct('[affectedUsers] out of [totalUsers] ([miseryPercentage]%) unique users waited more than [duration]ms', {
        affectedUsers: miserableUsers,
        totalUsers: totalUsers,
        miseryPercentage: miseryPercentage,
        duration: 4 * miseryLimit,
    });
    return (<Tooltip title={title} containerDisplayMode="block">
      <ScoreBar size={barHeight} score={adjustedScore} palette={palette} radius={0}/>
    </Tooltip>);
}
UserMisery.propTypes = {
    bars: PropTypes.number,
    miserableUsers: PropTypes.number,
    totalUsers: PropTypes.number,
    miseryLimit: PropTypes.number,
};
export default UserMisery;
//# sourceMappingURL=userMisery.jsx.map