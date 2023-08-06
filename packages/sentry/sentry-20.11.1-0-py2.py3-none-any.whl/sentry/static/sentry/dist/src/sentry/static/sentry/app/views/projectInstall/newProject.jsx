import { __makeTemplateObject } from "tslib";
import DocumentTitle from 'react-document-title';
import React from 'react';
import styled from '@emotion/styled';
import CreateProject from 'app/views/projectInstall/createProject';
import space from 'app/styles/space';
var NewProject = function () { return (<Container>
    <div className="container">
      <Content>
        <DocumentTitle title="Sentry"/>
        <CreateProject />
      </Content>
    </div>
  </Container>); };
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  background: ", ";\n  margin-bottom: -", "; /* cleans up a bg gap at bottom */\n"], ["\n  flex: 1;\n  background: ", ";\n  margin-bottom: -", "; /* cleans up a bg gap at bottom */\n"])), function (p) { return p.theme.background; }, space(3));
var Content = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(3));
export default NewProject;
var templateObject_1, templateObject_2;
//# sourceMappingURL=newProject.jsx.map