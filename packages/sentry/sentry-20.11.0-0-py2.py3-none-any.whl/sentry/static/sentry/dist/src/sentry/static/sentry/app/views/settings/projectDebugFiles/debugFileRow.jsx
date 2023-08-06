import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import Tag from 'app/components/tagDeprecated';
import FileSize from 'app/components/fileSize';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { IconDelete, IconClock, IconDownload } from 'app/icons';
import Access from 'app/components/acl/access';
import Role from 'app/components/acl/role';
import ButtonBar from 'app/components/buttonBar';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import { getFileType, getFeatureTooltip } from './utils';
var DebugFileRow = function (_a) {
    var debugFile = _a.debugFile, showDetails = _a.showDetails, downloadUrl = _a.downloadUrl, downloadRole = _a.downloadRole, onDelete = _a.onDelete;
    var id = debugFile.id, data = debugFile.data, debugId = debugFile.debugId, uuid = debugFile.uuid, size = debugFile.size, dateCreated = debugFile.dateCreated, objectName = debugFile.objectName, cpuName = debugFile.cpuName, symbolType = debugFile.symbolType, codeId = debugFile.codeId;
    var fileType = getFileType(debugFile);
    var features = (data || {}).features;
    return (<React.Fragment>
      <Column>
        <div>
          <DebugId>{debugId || uuid}</DebugId>
        </div>
        <TimeAndSizeWrapper>
          <StyledFileSize bytes={size}/>
          <TimeWrapper>
            <IconClock size="xs"/>
            <TimeSince date={dateCreated}/>
          </TimeWrapper>
        </TimeAndSizeWrapper>
      </Column>
      <Column>
        <Name>
          {symbolType === 'proguard' && objectName === 'proguard-mapping'
        ? '\u2015'
        : objectName}
        </Name>
        <Description>
          {symbolType === 'proguard' && cpuName === 'any'
        ? t('proguard mapping')
        : cpuName + " (" + symbolType + (fileType ? " " + fileType : '') + ")"}

          {features &&
        features.map(function (feature) { return (<Tooltip key={feature} title={getFeatureTooltip(feature)}>
                <Tag inline>{feature}</Tag>
              </Tooltip>); })}
          {showDetails && (<Details>
              
              {codeId && (<DetailsItem>
                  {t('Code ID')}: {codeId}
                </DetailsItem>)}
            </Details>)}
        </Description>
      </Column>
      <RightColumn>
        <ButtonBar gap={0.5}>
          <Role role={downloadRole}>
            {function (_a) {
        var hasRole = _a.hasRole;
        return (<Tooltip disabled={hasRole} title={t('You do not have permission to download debug files.')}>
                <Button size="xsmall" icon={<IconDownload size="xs"/>} href={downloadUrl} disabled={!hasRole}>
                  {t('Download')}
                </Button>
              </Tooltip>);
    }}
          </Role>
          <Access access={['project:write']}>
            {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<Tooltip disabled={hasAccess} title={t('You do not have permission to delete debug files.')}>
                <Confirm confirmText={t('Delete')} message={t('Are you sure you wish to delete this file?')} onConfirm={function () { return onDelete(id); }} disabled={!hasAccess}>
                  <Button priority="danger" icon={<IconDelete size="xs"/>} size="xsmall" disabled={!hasAccess} data-test-id="delete-dif"/>
                </Confirm>
              </Tooltip>);
    }}
          </Access>
        </ButtonBar>
      </RightColumn>
    </React.Fragment>);
};
var Column = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n"])));
var RightColumn = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-start;\n  margin-top: ", ";\n"])), space(1));
var DebugId = styled('code')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var TimeAndSizeWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 100%;\n  display: flex;\n  font-size: ", ";\n  margin-top: ", ";\n  color: ", ";\n  align-items: center;\n"], ["\n  width: 100%;\n  display: flex;\n  font-size: ", ";\n  margin-top: ", ";\n  color: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeSmall; }, space(1), function (p) { return p.theme.subText; });
var StyledFileSize = styled(FileSize)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n  padding-left: ", ";\n"], ["\n  flex: 1;\n  padding-left: ", ";\n"])), space(0.5));
var TimeWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  flex: 2;\n  align-items: center;\n  padding-left: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  flex: 2;\n  align-items: center;\n  padding-left: ", ";\n"])), space(0.5), space(0.5));
var Name = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(1));
var Description = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  @media (max-width: ", ") {\n    line-height: 1.7;\n  }\n"], ["\n  font-size: ", ";\n  color: ", ";\n  @media (max-width: ", ") {\n    line-height: 1.7;\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.breakpoints[2]; });
var Details = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject([""], [""])));
var DetailsItem = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  ", "\n  margin-top: ", "\n"], ["\n  ", "\n  margin-top: ", "\n"])), overflowEllipsis, space(1));
export default DebugFileRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=debugFileRow.jsx.map