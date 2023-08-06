import { __assign, __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { assignToUser, assignToActor } from 'app/actionCreators/group';
import withApi from 'app/utils/withApi';
import withCommitters from 'app/utils/withCommitters';
import withOrganization from 'app/utils/withOrganization';
import Access from 'app/components/acl/access';
import { findMatchedRules } from './findMatchedRules';
import { SuggestedAssignees } from './suggestedAssignees';
import { OwnershipRules } from './ownershipRules';
var SuggestedOwners = /** @class */ (function (_super) {
    __extends(SuggestedOwners, _super);
    function SuggestedOwners() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            rules: null,
            owners: [],
        };
        _this.fetchOwners = function (eventId) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, project, organization, data, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, project = _a.project, organization = _a.organization;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/events/" + eventId + "/owners/")];
                    case 2:
                        data = _c.sent();
                        this.setState({
                            rules: data.rules,
                            owners: data.owners,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState({
                            rules: null,
                            owners: [],
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleAssign = function (actor) { return function () {
            if (actor.id === undefined) {
                return;
            }
            var event = _this.props.event;
            if (actor.type === 'user') {
                // TODO(ts): `event` here may not be 100% correct
                // in this case groupID should always exist on event
                // since this is only used in Issue Details
                assignToUser({ id: event.groupID, user: actor });
            }
            if (actor.type === 'team') {
                assignToActor({ id: event.groupID, actor: actor });
            }
        }; };
        return _this;
    }
    SuggestedOwners.prototype.componentDidMount = function () {
        this.fetchData(this.props.event);
    };
    SuggestedOwners.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.event && prevProps.event) {
            if (this.props.event.id !== prevProps.event.id) {
                //two events, with different IDs
                this.fetchData(this.props.event);
            }
            return;
        }
        if (this.props.event) {
            //going from having no event to having an event
            this.fetchData(this.props.event);
        }
    };
    SuggestedOwners.prototype.fetchData = function (event) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.fetchOwners(event.id);
                return [2 /*return*/];
            });
        });
    };
    /**
     * Combine the commiter and ownership data into a single array, merging
     * users who are both owners based on having commits, and owners matching
     * project ownership rules into one array.
     *
     * The return array will include objects of the format:
     *
     * {
     *   actor: <
     *    type,              # Either user or team
     *    SentryTypes.User,  # API expanded user object
     *    {email, id, name}  # Sentry user which is *not* expanded
     *    {email, name}      # Unidentified user (from commits)
     *    {id, name},        # Sentry team (check `type`)
     *   >,
     *
     *   # One or both of commits and rules will be present
     *
     *   commits: [...]  # List of commits made by this owner
     *   rules:   [...]  # Project rules matched for this owner
     * }
     */
    SuggestedOwners.prototype.getOwnerList = function () {
        var _this = this;
        var owners = this.props.committers.map(function (commiter) { return ({
            actor: __assign(__assign({}, commiter.author), { type: 'user' }),
            commits: commiter.commits,
        }); });
        this.state.owners.forEach(function (owner) {
            var normalizedOwner = {
                actor: owner,
                rules: findMatchedRules(_this.state.rules || [], owner),
            };
            var existingIdx = owners.findIndex(function (o) { return o.actor.email === owner.email; });
            if (existingIdx > -1) {
                owners[existingIdx] = __assign(__assign({}, normalizedOwner), owners[existingIdx]);
                return;
            }
            owners.push(normalizedOwner);
        });
        return owners;
    };
    SuggestedOwners.prototype.render = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, group = _a.group;
        var owners = this.getOwnerList();
        return (<React.Fragment>
        {owners.length > 0 && (<SuggestedAssignees owners={owners} onAssign={this.handleAssign}/>)}
        <Access access={['project:write']}>
          <OwnershipRules issueId={group.id} project={project} organization={organization}/>
        </Access>
      </React.Fragment>);
    };
    return SuggestedOwners;
}(React.Component));
export default withApi(withOrganization(withCommitters(SuggestedOwners)));
//# sourceMappingURL=suggestedOwners.jsx.map