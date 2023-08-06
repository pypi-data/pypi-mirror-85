import { __assign, __rest } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import DataExport, { ExportQueryType } from 'app/components/dataExport';
import Button from 'app/components/button';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import { IconDownload, IconStack, IconTag } from 'app/icons';
import Hovercard from 'app/components/hovercard';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { downloadAsCsv } from '../utils';
function handleDownloadAsCsv(title, _a) {
    var organization = _a.organization, eventView = _a.eventView, tableData = _a.tableData;
    trackAnalyticsEvent({
        eventKey: 'discover_v2.results.download_csv',
        eventName: 'Discoverv2: Download CSV',
        organization_id: parseInt(organization.id, 10),
    });
    downloadAsCsv(tableData, eventView.getColumns(), title);
}
function renderDownloadButton(canEdit, props) {
    return (<Feature features={['organizations:discover-query']} renderDisabled={function () { return renderBrowserExportButton(canEdit, props); }}>
      {renderAsyncExportButton(canEdit, props)}
    </Feature>);
}
function renderBrowserExportButton(canEdit, _a) {
    var isLoading = _a.isLoading, props = __rest(_a, ["isLoading"]);
    var disabled = isLoading || canEdit === false;
    var onClick = disabled
        ? undefined
        : function () { return handleDownloadAsCsv(props.title, __assign({ isLoading: isLoading }, props)); };
    return (<Button size="small" disabled={disabled} onClick={onClick} data-test-id="grid-download-csv" icon={<IconDownload size="xs"/>}>
      {t('Export')}
    </Button>);
}
renderBrowserExportButton.propTypes = {
    title: PropTypes.string,
};
function renderAsyncExportButton(canEdit, props) {
    var isLoading = props.isLoading, location = props.location;
    var disabled = isLoading || canEdit === false;
    return (<DataExport payload={{
        queryType: ExportQueryType.Discover,
        queryInfo: location.query,
    }} disabled={disabled} icon={<IconDownload size="xs"/>}>
      {t('Export All')}
    </DataExport>);
}
// Placate eslint proptype checking
renderAsyncExportButton.propTypes = {
    isLoading: PropTypes.bool,
};
function renderEditButton(canEdit, props) {
    var onClick = canEdit ? props.onEdit : undefined;
    return (<Button size="small" disabled={!canEdit} onClick={onClick} data-test-id="grid-edit-enable" icon={<IconStack size="xs"/>}>
      {t('Columns')}
    </Button>);
}
// Placate eslint proptype checking
renderEditButton.propTypes = {
    onEdit: PropTypes.func,
};
function renderSummaryButton(_a) {
    var onChangeShowTags = _a.onChangeShowTags, showTags = _a.showTags;
    return (<Button size="small" onClick={onChangeShowTags} icon={<IconTag size="xs"/>}>
      {showTags ? t('Hide Tags') : t('Show Tags')}
    </Button>);
}
function FeatureWrapper(props) {
    var noEditMessage = t('Requires discover query feature.');
    var editFeatures = ['organizations:discover-query'];
    var renderDisabled = function (p) { return (<Hovercard body={<FeatureDisabled features={p.features} hideHelpToggle message={noEditMessage} featureName={noEditMessage}/>}>
      {p.children(p)}
    </Hovercard>); };
    return (<Feature hookName="feature-disabled:grid-editable-actions" renderDisabled={renderDisabled} features={editFeatures}>
      {function (_a) {
        var hasFeature = _a.hasFeature;
        return props.children(hasFeature, props);
    }}
    </Feature>);
}
function HeaderActions(props) {
    return (<React.Fragment>
      <FeatureWrapper {...props} key="edit">
        {renderEditButton}
      </FeatureWrapper>
      <FeatureWrapper {...props} key="download">
        {renderDownloadButton}
      </FeatureWrapper>
      {renderSummaryButton(props)}
    </React.Fragment>);
}
export default HeaderActions;
//# sourceMappingURL=tableActions.jsx.map