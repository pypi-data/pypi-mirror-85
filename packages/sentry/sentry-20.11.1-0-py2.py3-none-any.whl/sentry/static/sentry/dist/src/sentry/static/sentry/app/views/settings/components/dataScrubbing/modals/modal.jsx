import React from 'react';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
var Modal = function (_a) {
    var title = _a.title, onSave = _a.onSave, content = _a.content, disabled = _a.disabled, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, closeModal = _a.closeModal;
    return (<React.Fragment>
    <Header closeButton>
      <span data-test-id="modal-title">{title}</span>
    </Header>
    <Body>{content}</Body>
    <Footer>
      <ButtonBar gap={1.5}>
        <Button onClick={closeModal}>{t('Cancel')}</Button>
        <Button onClick={onSave} disabled={disabled} priority="primary">
          {t('Save Rule')}
        </Button>
      </ButtonBar>
    </Footer>
  </React.Fragment>);
};
export default Modal;
//# sourceMappingURL=modal.jsx.map