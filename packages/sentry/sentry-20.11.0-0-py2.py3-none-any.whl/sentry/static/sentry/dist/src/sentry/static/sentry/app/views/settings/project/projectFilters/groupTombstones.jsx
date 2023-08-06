import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
import Avatar from 'app/components/avatar';
import EventOrGroupHeader from 'app/components/eventOrGroupHeader';
import LinkWithConfirmation from 'app/components/links/linkWithConfirmation';
import Tooltip from 'app/components/tooltip';
import { IconDelete } from 'app/icons';
import { Panel, PanelItem } from 'app/components/panels';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import space from 'app/styles/space';
function GroupTombstoneRow(_a) {
    var data = _a.data, onUndiscard = _a.onUndiscard;
    var actor = data.actor;
    return (<PanelItem alignItems="center">
      <StyledBox>
        <EventOrGroupHeader includeLink={false} hideIcons className="truncate" size="normal" data={data}/>
      </StyledBox>
      <AvatarContainer>
        {actor && (<Avatar user={actor} hasTooltip tooltip={t('Discarded by %s', actor.name || actor.email)}/>)}
      </AvatarContainer>
      <ActionContainer>
        <Tooltip title={t('Undiscard')}>
          <LinkWithConfirmation title={t('Undiscard')} className="group-remove btn btn-default btn-sm" message={t('Undiscarding this issue means that ' +
        'incoming events that match this will no longer be discarded. ' +
        'New incoming events will count toward your event quota ' +
        'and will display on your issues dashboard. ' +
        'Are you sure you wish to continue?')} onConfirm={function () {
        onUndiscard(data.id);
    }}>
            <IconDelete className="undiscard"/>
          </LinkWithConfirmation>
        </Tooltip>
      </ActionContainer>
    </PanelItem>);
}
var GroupTombstones = /** @class */ (function (_super) {
    __extends(GroupTombstones, _super);
    function GroupTombstones() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUndiscard = function (tombstoneId) {
            var _a = _this.props, orgId = _a.orgId, projectId = _a.projectId;
            var path = "/projects/" + orgId + "/" + projectId + "/tombstones/" + tombstoneId + "/";
            _this.api
                .requestPromise(path, {
                method: 'DELETE',
            })
                .then(function () {
                addSuccessMessage(t('Events similar to these will no longer be filtered'));
                _this.fetchData();
            })
                .catch(function () {
                addErrorMessage(t('We were unable to undiscard this issue'));
                _this.fetchData();
            });
        };
        return _this;
    }
    GroupTombstones.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, projectId = _a.projectId;
        return [['tombstones', "/projects/" + orgId + "/" + projectId + "/tombstones/"]];
    };
    GroupTombstones.prototype.renderEmpty = function () {
        return (<Panel>
        <EmptyMessage>{t('You have no discarded issues')}</EmptyMessage>
      </Panel>);
    };
    GroupTombstones.prototype.renderBody = function () {
        var _this = this;
        var tombstones = this.state.tombstones;
        return tombstones.length ? (<Panel>
        {tombstones.map(function (data) { return (<GroupTombstoneRow key={data.id} data={data} onUndiscard={_this.handleUndiscard}/>); })}
      </Panel>) : (this.renderEmpty());
    };
    return GroupTombstones;
}(AsyncComponent));
var StyledBox = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  align-items: center;\n  min-width: 0; /* keep child content from stretching flex item */\n"], ["\n  flex: 1;\n  align-items: center;\n  min-width: 0; /* keep child content from stretching flex item */\n"])));
var AvatarContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0 ", ";\n  width: ", ";\n"], ["\n  margin: 0 ", ";\n  width: ", ";\n"])), space(4), space(3));
var ActionContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: ", ";\n"], ["\n  width: ", ";\n"])), space(4));
export default GroupTombstones;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=groupTombstones.jsx.map