import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { getMeta } from 'app/components/events/meta/metaProxy';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import space from 'app/styles/space';
import TextOverflow from 'app/components/textOverflow';
import ContextSummaryNoSummary from './contextSummaryNoSummary';
import generateClassName from './generateClassName';
import Item from './item';
var ContextSummaryOS = function (_a) {
    var data = _a.data;
    if (Object.keys(data).length === 0 || !data.name) {
        return <ContextSummaryNoSummary title={t('Unknown OS')}/>;
    }
    var renderName = function () {
        var meta = getMeta(data, 'name');
        return <AnnotatedText value={data.name} meta={meta}/>;
    };
    var getVersionElement = function () {
        if (data.version) {
            return {
                subject: t('Version:'),
                value: data.version,
                meta: getMeta(data, 'version'),
            };
        }
        if (data.kernel_version) {
            return {
                subject: t('Kernel:'),
                value: data.kernel_version,
                meta: getMeta(data, 'kernel_version'),
            };
        }
        return {
            subject: t('Version:'),
            value: t('Unknown'),
        };
    };
    var versionElement = getVersionElement();
    var className = generateClassName(data.name);
    return (<Item className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderName()}</h3>
      <TextOverflow isParagraph>
        <Subject>{versionElement.subject}</Subject>
        <AnnotatedText value={versionElement.value} meta={versionElement.meta}/>
      </TextOverflow>
    </Item>);
};
ContextSummaryOS.propTypes = {
    data: PropTypes.object.isRequired,
};
export default ContextSummaryOS;
var Subject = styled('strong')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryOS.jsx.map