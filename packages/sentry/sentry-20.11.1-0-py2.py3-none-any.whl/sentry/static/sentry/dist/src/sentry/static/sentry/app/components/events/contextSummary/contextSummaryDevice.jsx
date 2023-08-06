import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import { getMeta } from 'app/components/events/meta/metaProxy';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import DeviceName from 'app/components/deviceName';
import space from 'app/styles/space';
import TextOverflow from 'app/components/textOverflow';
import generateClassName from './generateClassName';
import ContextSummaryNoSummary from './contextSummaryNoSummary';
import Item from './item';
var ContextSummaryDevice = function (_a) {
    var data = _a.data;
    if (Object.keys(data).length === 0) {
        return <ContextSummaryNoSummary title={t('Unknown Device')}/>;
    }
    var renderName = function () {
        if (!data.model) {
            return t('Unknown Device');
        }
        var meta = getMeta(data, 'model');
        return (<DeviceName value={data.model}>
        {function (deviceName) {
            return <AnnotatedText value={deviceName} meta={meta}/>;
        }}
      </DeviceName>);
    };
    var getSubTitle = function () {
        if (data.arch) {
            return {
                subject: t('Arch:'),
                value: data.arch,
                meta: getMeta(data, 'arch'),
            };
        }
        if (data.model_id) {
            return {
                subject: t('Model:'),
                value: data.model_id,
                meta: getMeta(data, 'model_id'),
            };
        }
        return null;
    };
    // TODO(dcramer): we need a better way to parse it
    var className = generateClassName(data.model);
    var subTitle = getSubTitle();
    return (<Item className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderName()}</h3>
      {subTitle && (<TextOverflow isParagraph>
          <Subject>{subTitle.subject}</Subject>
          <AnnotatedText value={subTitle.value} meta={subTitle.meta}/>
        </TextOverflow>)}
    </Item>);
};
ContextSummaryDevice.propTypes = {
    data: PropTypes.object.isRequired,
};
export default ContextSummaryDevice;
var Subject = styled('strong')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryDevice.jsx.map