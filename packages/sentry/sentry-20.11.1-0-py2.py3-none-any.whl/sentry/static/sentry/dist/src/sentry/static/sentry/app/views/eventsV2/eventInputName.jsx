import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import { addErrorMessage } from 'app/actionCreators/indicator';
import InlineInput from 'app/components/inputInline';
import EventView from 'app/utils/discover/eventView';
import { Title } from 'app/components/layouts/thirds';
import { handleUpdateQueryName } from './savedQuery/utils';
var NAME_DEFAULT = t('Untitled query');
/**
 * Allows user to edit the name of the query. Upon blurring from it, it will
 * save the name change immediately (but not changes in the query)
 */
var EventInputName = /** @class */ (function (_super) {
    __extends(EventInputName, _super);
    function EventInputName() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.refInput = React.createRef();
        _this.onBlur = function (event) {
            var _a = _this.props, api = _a.api, organization = _a.organization, savedQuery = _a.savedQuery, eventView = _a.eventView;
            var nextQueryName = (event.target.value || '').trim();
            // Do not update automatically if
            // 1) New name is empty
            // 2) It is a new query
            // 3) The new name is same as the old name
            if (!nextQueryName) {
                addErrorMessage(t('Please set a name for this query'));
                // Help our users re-focus so they cannot run away from this problem
                if (_this.refInput.current) {
                    _this.refInput.current.focus();
                }
                return;
            }
            if (!savedQuery || savedQuery.name === nextQueryName) {
                return;
            }
            // This ensures that we are updating SavedQuery.name only.
            // Changes on QueryBuilder table will not be saved.
            var nextEventView = EventView.fromSavedQuery(__assign(__assign({}, savedQuery), { name: nextQueryName }));
            handleUpdateQueryName(api, organization, nextEventView).then(function (_updatedQuery) {
                // The current eventview may have changes that are not explicitly saved.
                // So, we just preserve them and change its name
                var renamedEventView = eventView.clone();
                renamedEventView.name = nextQueryName;
                browserHistory.push(renamedEventView.getResultsViewUrlTarget(organization.slug));
            });
        };
        return _this;
    }
    EventInputName.prototype.render = function () {
        var eventView = this.props.eventView;
        return (<Title>
        <InlineInput ref={this.refInput} name="discover2-query-name" disabled={!eventView.id} value={eventView.name || NAME_DEFAULT} onBlur={this.onBlur}/>
      </Title>);
    };
    return EventInputName;
}(React.Component));
export default withApi(EventInputName);
//# sourceMappingURL=eventInputName.jsx.map