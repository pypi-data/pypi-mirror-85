import { __makeTemplateObject, __read } from "tslib";
import isNil from 'lodash/isNil';
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import DebugFileFeature from 'app/components/debugFileFeature';
import { PanelItem } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { formatAddress, getImageRange } from 'app/components/events/interfaces/utils';
import { t } from 'app/locale';
import { IconSearch, IconCircle, IconCheckmark, IconFlag } from 'app/icons';
import { getFileName, combineStatus } from './utils';
var IMAGE_ADDR_LEN = 12;
function getImageStatusText(status) {
    switch (status) {
        case 'found':
            return t('ok');
        case 'unused':
            return t('unused');
        case 'missing':
            return t('missing');
        case 'malformed':
        case 'fetching_failed':
        case 'timeout':
        case 'other':
            return t('failed');
        default:
            return null;
    }
}
function getImageStatusDetails(status) {
    switch (status) {
        case 'found':
            return t('Debug information for this image was found and successfully processed.');
        case 'unused':
            return t('The image was not required for processing the stack trace.');
        case 'missing':
            return t('No debug information could be found in any of the specified sources.');
        case 'malformed':
            return t('The debug information file for this image failed to process.');
        case 'timeout':
        case 'fetching_failed':
            return t('The debug information file for this image could not be downloaded.');
        case 'other':
            return t('An internal error occurred while handling this image.');
        default:
            return null;
    }
}
var DebugImage = React.memo(function (_a) {
    var image = _a.image, orgId = _a.orgId, projectId = _a.projectId, showDetails = _a.showDetails, style = _a.style;
    var getSettingsLink = function () {
        if (!orgId || !projectId || !image.debug_id) {
            return null;
        }
        return "/settings/" + orgId + "/projects/" + projectId + "/debug-symbols/?query=" + image.debug_id;
    };
    var renderStatus = function (title, status) {
        if (isNil(status)) {
            return null;
        }
        var text = getImageStatusText(status);
        if (!text) {
            return null;
        }
        return (<SymbolicationStatus>
        <Tooltip title={getImageStatusDetails(status)}>
          <span>
            <ImageProp>{title}</ImageProp>: {text}
          </span>
        </Tooltip>
      </SymbolicationStatus>);
    };
    var combinedStatus = combineStatus(image === null || image === void 0 ? void 0 : image.debug_status, image.unwind_status);
    var _b = __read(getImageRange(image), 2), startAddress = _b[0], endAddress = _b[1];
    var renderIconElement = function () {
        switch (combinedStatus) {
            case 'unused':
                return (<IconWrapper>
            <IconCircle />
          </IconWrapper>);
            case 'found':
                return (<IconWrapper>
            <IconCheckmark isCircled color="green300"/>
          </IconWrapper>);
            default:
                return (<IconWrapper>
            <IconFlag color="red300"/>
          </IconWrapper>);
        }
    };
    var codeFile = getFileName(image.code_file);
    var debugFile = image.debug_file && getFileName(image.debug_file);
    // The debug file is only realistically set on Windows. All other platforms
    // either leave it empty or set it to a filename thats equal to the code
    // file name. In this case, do not show it.
    var showDebugFile = debugFile && codeFile !== debugFile;
    // Availability only makes sense if the image is actually referenced.
    // Otherwise, the processing pipeline does not resolve this kind of
    // information and it will always be false.
    var showAvailability = !isNil(image.features) && combinedStatus !== 'unused';
    // The code id is sometimes missing, and sometimes set to the equivalent of
    // the debug id (e.g. for Mach symbols). In this case, it is redundant
    // information and we do not want to show it.
    var showCodeId = !!image.code_id && image.code_id !== image.debug_id;
    // Old versions of the event pipeline did not store the symbolication
    // status. In this case, default to display the debug_id instead of stack
    // unwind information.
    var legacyRender = isNil(image.debug_status);
    var debugIdElement = (<ImageSubtext>
      <ImageProp>{t('Debug ID')}</ImageProp>: <Formatted>{image.debug_id}</Formatted>
    </ImageSubtext>);
    return (<DebugImageItem style={style}>
      <ImageInfoGroup>{renderIconElement()}</ImageInfoGroup>

      <ImageInfoGroup>
        <Formatted>{formatAddress(startAddress, IMAGE_ADDR_LEN)}</Formatted> &ndash;{' '}
        <AddressDivider />
        <Formatted>{formatAddress(endAddress, IMAGE_ADDR_LEN)}</Formatted>
      </ImageInfoGroup>

      <ImageInfoGroup fullWidth>
        <ImageTitle>
          <Tooltip title={image.code_file}>
            <CodeFile>{codeFile}</CodeFile>
          </Tooltip>
          {showDebugFile && <DebugFile> ({debugFile})</DebugFile>}
        </ImageTitle>

        {legacyRender ? (debugIdElement) : (<StatusLine>
            {renderStatus(t('Stack Unwinding'), image.unwind_status)}
            {renderStatus(t('Symbolication'), image.debug_status)}
          </StatusLine>)}

        {showDetails && (<React.Fragment>
            {showAvailability && (<ImageSubtext>
                <ImageProp>{t('Availability')}</ImageProp>:
                <DebugFileFeature feature="symtab" available={image.features.has_symbols}/>
                <DebugFileFeature feature="debug" available={image.features.has_debug_info}/>
                <DebugFileFeature feature="unwind" available={image.features.has_unwind_info}/>
                <DebugFileFeature feature="sources" available={image.features.has_sources}/>
              </ImageSubtext>)}

            {!legacyRender && debugIdElement}

            {showCodeId && (<ImageSubtext>
                <ImageProp>{t('Code ID')}</ImageProp>:{' '}
                <Formatted>{image.code_id}</Formatted>
              </ImageSubtext>)}

            {!!image.arch && (<ImageSubtext>
                <ImageProp>{t('Architecture')}</ImageProp>: {image.arch}
              </ImageSubtext>)}
          </React.Fragment>)}
      </ImageInfoGroup>

      <Access access={['project:releases']}>
        {function (_a) {
        var hasAccess = _a.hasAccess;
        if (!hasAccess) {
            return null;
        }
        var settingsUrl = getSettingsLink();
        if (!settingsUrl) {
            return null;
        }
        return (<ImageActions>
              <Tooltip title={t('Search for debug files in settings')}>
                <Button size="xsmall" icon={<IconSearch size="xs"/>} to={settingsUrl}/>
              </Tooltip>
            </ImageActions>);
    }}
      </Access>
    </DebugImageItem>);
});
export default DebugImage;
var DebugImageItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  @media (max-width: ", ") {\n    display: grid;\n    grid-gap: ", ";\n    position: relative;\n  }\n"], ["\n  font-size: ", ";\n  @media (max-width: ", ") {\n    display: grid;\n    grid-gap: ", ";\n    position: relative;\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.breakpoints[0]; }, space(1));
var Formatted = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var ImageInfoGroup = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: 1em;\n  flex-grow: ", ";\n\n  &:first-child {\n    @media (min-width: ", ") {\n      margin-left: 0;\n    }\n  }\n"], ["\n  margin-left: 1em;\n  flex-grow: ", ";\n\n  &:first-child {\n    @media (min-width: ", ") {\n      margin-left: 0;\n    }\n  }\n"])), function (p) { return (p.fullWidth ? 1 : null); }, function (p) { return p.theme.breakpoints[0]; });
var ImageActions = styled(ImageInfoGroup)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    position: absolute;\n    top: 15px;\n    right: 20px;\n  }\n"], ["\n  @media (max-width: ", ") {\n    position: absolute;\n    top: 15px;\n    right: 20px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ImageTitle = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var CodeFile = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var DebugFile = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var ImageSubtext = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var ImageProp = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var StatusLine = styled(ImageSubtext)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  @media (max-width: ", ") {\n    display: grid;\n  }\n"], ["\n  display: flex;\n  @media (max-width: ", ") {\n    display: grid;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var AddressDivider = styled('br')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var IconWrapper = styled('span')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  display: inline-block;\n  margin-top: ", ";\n  height: 16px;\n\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  display: inline-block;\n  margin-top: ", ";\n  height: 16px;\n\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), space(0.5), function (p) { return p.theme.breakpoints[0]; }, space(0.25));
var SymbolicationStatus = styled('span')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  flex-grow: 1;\n  flex-basis: 0;\n  margin-right: 1em;\n\n  svg {\n    margin-left: 0.66ex;\n  }\n"], ["\n  flex-grow: 1;\n  flex-basis: 0;\n  margin-right: 1em;\n\n  svg {\n    margin-left: 0.66ex;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=debugImage.jsx.map