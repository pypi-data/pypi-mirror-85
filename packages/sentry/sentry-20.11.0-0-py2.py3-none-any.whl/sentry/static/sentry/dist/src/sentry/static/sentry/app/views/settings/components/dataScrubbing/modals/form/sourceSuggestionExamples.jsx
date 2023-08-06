import { __extends, __makeTemplateObject } from "tslib";
import Modal from 'react-bootstrap/lib/Modal';
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t } from 'app/locale';
import Button from 'app/components/button';
var SourceSuggestionExamples = /** @class */ (function (_super) {
    __extends(SourceSuggestionExamples, _super);
    function SourceSuggestionExamples() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { isOpen: false };
        _this.toggleModal = function () {
            _this.setState({ isOpen: !_this.state.isOpen });
        };
        _this.stopPropagation = function (e) {
            // Necessary to stop propagation of click events from modal that we can't
            // catch otherwise.
            e.stopPropagation();
        };
        return _this;
    }
    SourceSuggestionExamples.prototype.render = function () {
        var isOpen = this.state.isOpen;
        var _a = this.props, examples = _a.examples, sourceName = _a.sourceName;
        return (<Wrapper onClick={this.stopPropagation}>
        <Button size="xsmall" onClick={this.toggleModal}>
          {t('examples')}
        </Button>
        {isOpen && (<StyledModal show onHide={this.toggleModal}>
            <Modal.Header closeButton>
              {t('Examples for %s in current event', <code>{sourceName}</code>)}
            </Modal.Header>
            <Modal.Body>
              {examples.map(function (example) { return (<pre key={example}>{example}</pre>); })}
            </Modal.Body>
          </StyledModal>)}
      </Wrapper>);
    };
    return SourceSuggestionExamples;
}(React.Component));
export default SourceSuggestionExamples;
var StyledModal = styled(Modal)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .modal-dialog {\n    position: absolute;\n    top: 50%;\n    left: 50%;\n    transform: translate(-50%, -50%) !important;\n    margin: 0;\n    z-index: 1003;\n    @media (max-width: ", ") {\n      width: 100%;\n    }\n  }\n\n  .modal-body {\n    max-height: 500px;\n    overflow-y: auto;\n    padding: ", " ", ";\n    margin: -", " -", ";\n  }\n\n  .close {\n    outline: none;\n  }\n"], ["\n  .modal-dialog {\n    position: absolute;\n    top: 50%;\n    left: 50%;\n    transform: translate(-50%, -50%) !important;\n    margin: 0;\n    z-index: 1003;\n    @media (max-width: ", ") {\n      width: 100%;\n    }\n  }\n\n  .modal-body {\n    max-height: 500px;\n    overflow-y: auto;\n    padding: ", " ", ";\n    margin: -", " -", ";\n  }\n\n  .close {\n    outline: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(3), space(4), space(3), space(4));
var Wrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 3/3;\n"], ["\n  grid-column: 3/3;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=sourceSuggestionExamples.jsx.map