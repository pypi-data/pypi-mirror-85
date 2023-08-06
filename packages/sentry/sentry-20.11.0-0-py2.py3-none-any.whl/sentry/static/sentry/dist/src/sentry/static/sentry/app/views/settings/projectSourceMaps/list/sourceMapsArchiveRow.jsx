import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import { IconDelete } from 'app/icons';
import ButtonBar from 'app/components/buttonBar';
import Version from 'app/components/version';
import Count from 'app/components/count';
import Confirm from 'app/components/confirm';
import DateTime from 'app/components/dateTime';
import Link from 'app/components/links/link';
import TextOverflow from 'app/components/textOverflow';
import space from 'app/styles/space';
import Access from 'app/components/acl/access';
import Tooltip from 'app/components/tooltip';
var SourceMapsArchiveRow = function (_a) {
    var archive = _a.archive, orgId = _a.orgId, projectId = _a.projectId, onDelete = _a.onDelete;
    var name = archive.name, date = archive.date, fileCount = archive.fileCount;
    var archiveLink = "/settings/" + orgId + "/projects/" + projectId + "/source-maps/" + encodeURIComponent(name);
    return (<React.Fragment>
      <Column>
        <TextOverflow>
          <Link to={archiveLink}>
            <Version version={name} anchor={false} tooltipRawVersion truncate/>
          </Link>
        </TextOverflow>
      </Column>
      <ArtifactsColumn>
        <Count value={fileCount}/>
      </ArtifactsColumn>
      <Column>{t('release')}</Column>
      <Column>
        <DateTime date={date}/>
      </Column>
      <ActionsColumn>
        <ButtonBar gap={0.5}>
          <Access access={['project:releases']}>
            {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<Tooltip disabled={hasAccess} title={t('You do not have permission to delete artifacts.')}>
                <Confirm onConfirm={function () { return onDelete(name); }} message={t('Are you sure you want to remove all artifacts in this archive?')} disabled={!hasAccess}>
                  <Button size="small" icon={<IconDelete size="sm"/>} title={t('Remove All Artifacts')} label={t('Remove All Artifacts')} disabled={!hasAccess}/>
                </Confirm>
              </Tooltip>);
    }}
          </Access>
        </ButtonBar>
      </ActionsColumn>
    </React.Fragment>);
};
var Column = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  overflow: hidden;\n"], ["\n  display: flex;\n  align-items: center;\n  overflow: hidden;\n"])));
var ArtifactsColumn = styled(Column)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-right: ", ";\n  text-align: right;\n  justify-content: flex-end;\n"], ["\n  padding-right: ", ";\n  text-align: right;\n  justify-content: flex-end;\n"])), space(4));
var ActionsColumn = styled(Column)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
export default SourceMapsArchiveRow;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sourceMapsArchiveRow.jsx.map