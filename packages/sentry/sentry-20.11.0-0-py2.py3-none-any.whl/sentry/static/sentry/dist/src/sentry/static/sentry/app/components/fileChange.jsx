import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import { ListGroupItem } from 'app/components/listGroup';
import space from 'app/styles/space';
import AvatarList from 'app/components/avatar/avatarList';
import FileIcon from 'app/components/fileIcon';
import TextOverflow from 'app/components/textOverflow';
var FileChange = function (_a) {
    var filename = _a.filename, authors = _a.authors, className = _a.className;
    return (<FileItem className={className}>
    <Filename>
      <StyledFileIcon fileName={filename}/>
      <TextOverflow>{filename}</TextOverflow>
    </Filename>
    <div>
      <AvatarList users={authors} avatarSize={25} typeMembers="authors"/>
    </div>
  </FileItem>);
};
FileChange.propTypes = {
    filename: PropTypes.string.isRequired,
    authors: PropTypes.array.isRequired,
};
var FileItem = styled(ListGroupItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var Filename = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  margin-right: ", ";\n  align-items: center;\n  grid-template-columns: max-content 1fr;\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  margin-right: ", ";\n  align-items: center;\n  grid-template-columns: max-content 1fr;\n"])), function (p) { return p.theme.fontSizeMedium; }, space(1), space(3));
var StyledFileIcon = styled(FileIcon)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  border-radius: 3px;\n"], ["\n  color: ", ";\n  border-radius: 3px;\n"])), function (p) { return p.theme.gray200; });
export default FileChange;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=fileChange.jsx.map