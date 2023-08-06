import { __extends } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import UserAvatar from 'app/components/avatar/userAvatar';
import TimeSince from 'app/components/timeSince';
import { t } from 'app/locale';
var unknownUser = {
    id: '',
    name: '',
    username: '??',
    email: '',
    avatarUrl: '',
    avatar: {
        avatarUuid: '',
        avatarType: 'letter_avatar',
    },
    ip_address: '',
};
var LastCommit = /** @class */ (function (_super) {
    __extends(LastCommit, _super);
    function LastCommit() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LastCommit.prototype.renderMessage = function (message) {
        if (!message) {
            return t('No message provided');
        }
        var firstLine = message.split(/\n/)[0];
        if (firstLine.length > 100) {
            var truncated = firstLine.substr(0, 90);
            var words = truncated.split(/ /);
            // try to not have elipsis mid-word
            if (words.length > 1) {
                words.pop();
                truncated = words.join(' ');
            }
            return truncated + '...';
        }
        return firstLine;
    };
    LastCommit.prototype.render = function () {
        var _a = this.props, commit = _a.commit, headerClass = _a.headerClass;
        var commitAuthor = commit && commit.author;
        return (<div>
        <h6 className={headerClass}>Last commit</h6>
        <div className="commit">
          <div className="commit-avatar">
            <UserAvatar user={commitAuthor || unknownUser}/>
          </div>
          <div className="commit-message truncate">
            {this.renderMessage(commit.message)}
          </div>
          <div className="commit-meta">
            <strong>{(commitAuthor && commitAuthor.name) || t('Unknown Author')}</strong>
            &nbsp;
            <TimeSince date={commit.dateCreated}/>
          </div>
        </div>
      </div>);
    };
    LastCommit.propTypes = {
        commit: PropTypes.object.isRequired,
        headerClass: PropTypes.string,
    };
    return LastCommit;
}(React.Component));
export default LastCommit;
//# sourceMappingURL=lastCommit.jsx.map