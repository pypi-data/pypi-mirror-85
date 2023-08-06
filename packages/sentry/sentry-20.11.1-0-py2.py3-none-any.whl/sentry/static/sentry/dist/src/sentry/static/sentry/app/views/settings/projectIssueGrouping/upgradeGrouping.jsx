import { __awaiter, __generator } from "tslib";
import React from 'react';
import Alert from 'app/components/alert';
import { t, tct } from 'app/locale';
import TextBlock from 'app/views/settings/components/text/textBlock';
import ProjectActions from 'app/actions/projectActions';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import marked from 'app/utils/marked';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import Field from 'app/views/settings/components/forms/field';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import handleXhrErrorResponse from 'app/utils/handleXhrErrorResponse';
import { getGroupingChanges, getGroupingRisk } from './utils';
function UpgradeGrouping(_a) {
    var _this = this;
    var groupingConfigs = _a.groupingConfigs, groupingEnhancementBases = _a.groupingEnhancementBases, organization = _a.organization, projectId = _a.projectId, project = _a.project, onUpgrade = _a.onUpgrade, api = _a.api;
    var hasAccess = organization.access.includes('project:write');
    var _b = getGroupingChanges(project, groupingConfigs, groupingEnhancementBases), updateNotes = _b.updateNotes, riskLevel = _b.riskLevel, latestGroupingConfig = _b.latestGroupingConfig, latestEnhancementsBase = _b.latestEnhancementsBase;
    var _c = getGroupingRisk(riskLevel), riskNote = _c.riskNote, alertType = _c.alertType;
    var noUpdates = !latestGroupingConfig && !latestEnhancementsBase;
    var newData = {};
    if (latestGroupingConfig) {
        newData.groupingConfig = latestGroupingConfig.id;
    }
    if (latestEnhancementsBase) {
        newData.groupingEnhancementsBase = latestEnhancementsBase.id;
    }
    var handleUpgrade = function () { return __awaiter(_this, void 0, void 0, function () {
        var response, _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    addLoadingMessage(t('Changing grouping\u2026'));
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectId + "/", {
                            method: 'PUT',
                            data: newData,
                        })];
                case 2:
                    response = _b.sent();
                    clearIndicators();
                    ProjectActions.updateSuccess(response);
                    onUpgrade();
                    return [3 /*break*/, 4];
                case 3:
                    _a = _b.sent();
                    handleXhrErrorResponse(t('Unable to upgrade config'));
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    }); };
    if (!groupingConfigs || !groupingEnhancementBases) {
        return null;
    }
    function getModalMessage() {
        return (<React.Fragment>
        <TextBlock>
          <strong>{t('Upgrade Grouping Strategy')}</strong>
        </TextBlock>
        <TextBlock>
          {t('You can upgrade the grouping strategy to the latest but this is an irreversible operation.')}
        </TextBlock>
        <TextBlock>
          <strong>{t('New Behavior')}</strong>
          <div dangerouslySetInnerHTML={{ __html: marked(updateNotes) }}/>
        </TextBlock>
        <TextBlock>
          <Alert type={alertType}>{riskNote}</Alert>
        </TextBlock>
      </React.Fragment>);
    }
    function getButtonTitle() {
        if (!hasAccess) {
            return t('You do not have sufficient permissions to do this');
        }
        if (noUpdates) {
            return t('You are already on the latest version');
        }
        return undefined;
    }
    return (<Panel id="upgrade-grouping">
      <PanelHeader>{t('Upgrade Grouping')}</PanelHeader>
      <PanelBody>
        <Field label={t('Upgrade Grouping Strategy')} help={tct('If the project uses an old grouping strategy an update is possible.[linebreak]Doing so will cause new events to group differently.', {
        linebreak: <br />,
    })} disabled>
          <Confirm disabled={noUpdates} onConfirm={handleUpgrade} priority={riskLevel >= 2 ? 'danger' : 'primary'} confirmText={t('Upgrade')} message={getModalMessage()}>
            <div>
              <Button disabled={!hasAccess || noUpdates} title={getButtonTitle()} type="button" priority={riskLevel >= 2 ? 'danger' : 'primary'}>
                {t('Upgrade Grouping Strategy')}
              </Button>
            </div>
          </Confirm>
        </Field>
      </PanelBody>
    </Panel>);
}
export default UpgradeGrouping;
//# sourceMappingURL=upgradeGrouping.jsx.map