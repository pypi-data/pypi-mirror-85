import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import uniqBy from 'lodash/uniqBy';
import flatMap from 'lodash/flatMap';
import styled from '@emotion/styled';
import CommitRow from 'app/components/commitRow';
import { IconAdd, IconSubtract } from 'app/icons';
import { Panel } from 'app/components/panels';
import { DataSection, CauseHeader } from 'app/components/events/styles';
import withApi from 'app/utils/withApi';
import withCommitters from 'app/utils/withCommitters';
import space from 'app/styles/space';
import { t } from 'app/locale';
var EventCause = /** @class */ (function (_super) {
    __extends(EventCause, _super);
    function EventCause() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            expanded: false,
        };
        return _this;
    }
    EventCause.prototype.getUniqueCommitsWithAuthors = function () {
        var committers = this.props.committers;
        // Get a list of commits with author information attached
        var commitsWithAuthors = flatMap(committers, function (_a) {
            var commits = _a.commits, author = _a.author;
            return commits.map(function (commit) { return (__assign(__assign({}, commit), { author: author })); });
        });
        // Remove duplicate commits
        var uniqueCommitsWithAuthors = uniqBy(commitsWithAuthors, function (commit) { return commit.id; });
        return uniqueCommitsWithAuthors;
    };
    EventCause.prototype.render = function () {
        var _this = this;
        var committers = this.props.committers;
        var expanded = this.state.expanded;
        if (!(committers && committers.length)) {
            return null;
        }
        var commits = this.getUniqueCommitsWithAuthors();
        return (<DataSection>
        <CauseHeader>
          <h3>
            {t('Suspect Commits')} ({commits.length})
          </h3>
          {commits.length > 1 && (<ExpandButton onClick={function () { return _this.setState({ expanded: !expanded }); }}>
              {expanded ? (<React.Fragment>
                  {t('Show less')} <IconSubtract isCircled size="md"/>
                </React.Fragment>) : (<React.Fragment>
                  {t('Show more')} <IconAdd isCircled size="md"/>
                </React.Fragment>)}
            </ExpandButton>)}
        </CauseHeader>
        <Panel>
          {commits.slice(0, expanded ? 100 : 1).map(function (commit) { return (<CommitRow key={commit.id} commit={commit}/>); })}
        </Panel>
      </DataSection>);
    };
    return EventCause;
}(React.Component));
var ExpandButton = styled('button')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  & > svg {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  & > svg {\n    margin-left: ", ";\n  }\n"])), space(0.5));
export default withApi(withCommitters(EventCause));
var templateObject_1;
//# sourceMappingURL=eventCause.jsx.map