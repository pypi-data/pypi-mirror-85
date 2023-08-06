import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import CreateSampleEventButton from 'app/views/onboarding/createSampleEventButton';
import Panel from 'app/components/panels/panel';
import PanelBody from 'app/components/panels/panelBody';
import getDynamicText from 'app/utils/getDynamicText';
import space from 'app/styles/space';
import Alert from 'app/components/alert';
var LEARN_MORE_VIDEO = 'https://player.vimeo.com/video/319554213';
var learnMoveVideo = getDynamicText({
    fixed: 'Video Demo Placeholder',
    value: (<iframe src={LEARN_MORE_VIDEO} frameBorder="0" allow="autoplay; fullscreen" allowFullScreen/>),
});
var LearnMore = function (_a) {
    var project = _a.project;
    return (<React.Fragment>
    <DemoVideo>{learnMoveVideo}</DemoVideo>
    {project ? (<Panel>
        <SampleEventPanelBody withPadding>
          {tct("Want to see more of what Sentry can do before integrating into your\n           application? Create a [strong:Sample Error Event] and poke around to\n           get a better feel for the Sentry workflow.", { strong: <strong /> })}
          <CreateSampleEventButton project={project} source="onboarding_setup" priority="primary">
            {t('Create A Sample Event')}
          </CreateSampleEventButton>
        </SampleEventPanelBody>
      </Panel>) : (<Alert type="info">{t('Create a project to view a sample event!')}</Alert>)}
  </React.Fragment>);
};
var DemoVideo = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  overflow: hidden;\n  margin-bottom: ", ";\n\n  /* 16:9 aspect ratio */\n  position: relative;\n  padding-top: 56.2%;\n\n  iframe {\n    position: absolute;\n    top: 0;\n    width: 100%;\n    height: 100%;\n  }\n"], ["\n  display: flex;\n  justify-content: center;\n  overflow: hidden;\n  margin-bottom: ", ";\n\n  /* 16:9 aspect ratio */\n  position: relative;\n  padding-top: 56.2%;\n\n  iframe {\n    position: absolute;\n    top: 0;\n    width: 100%;\n    height: 100%;\n  }\n"])), space(2));
var SampleEventPanelBody = styled(PanelBody)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(2));
export default LearnMore;
var templateObject_1, templateObject_2;
//# sourceMappingURL=learnMore.jsx.map