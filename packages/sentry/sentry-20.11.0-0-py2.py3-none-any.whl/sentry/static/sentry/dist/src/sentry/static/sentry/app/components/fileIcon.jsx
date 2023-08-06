import React from 'react';
import { IconFile } from 'app/icons';
import theme from 'app/utils/theme';
var FILE_EXTENSION_TO_ICON = {
    jsx: 'react',
    tsx: 'react',
    js: 'javascript',
    ts: 'javascript',
    php: 'php',
    py: 'python',
    vue: 'vue',
    go: 'go',
    java: 'java',
    perl: 'perl',
    rb: 'ruby',
    rs: 'rust',
    rlib: 'rust',
    swift: 'swift',
    h: 'apple',
    m: 'apple',
    mm: 'apple',
    M: 'apple',
    cs: 'csharp',
    ex: 'elixir',
    exs: 'elixir',
};
var FileIcon = function (_a) {
    var _b;
    var fileName = _a.fileName, _c = _a.size, providedSize = _c === void 0 ? 'sm' : _c, className = _a.className;
    var fileExtension = fileName.split('.').pop();
    var iconName = fileExtension ? FILE_EXTENSION_TO_ICON[fileExtension] : null;
    var size = (_b = theme.iconSizes[providedSize]) !== null && _b !== void 0 ? _b : providedSize;
    if (!iconName) {
        return <IconFile size={size} className={className}/>;
    }
    return (<img src={require("platformicons/svg/" + iconName + ".svg")} width={size} height={size} className={className}/>);
};
export default FileIcon;
//# sourceMappingURL=fileIcon.jsx.map