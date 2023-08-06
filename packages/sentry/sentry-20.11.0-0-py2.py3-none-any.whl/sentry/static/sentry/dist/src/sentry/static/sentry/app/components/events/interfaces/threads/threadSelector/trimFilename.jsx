function trimFilename(filename) {
    var pieces = filename.split(/\//g);
    return pieces[pieces.length - 1];
}
export default trimFilename;
//# sourceMappingURL=trimFilename.jsx.map