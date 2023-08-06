import React from 'react';
import { t } from 'app/locale';
import { IconQuestion, IconWarning } from 'app/icons';
import { SymbolicatorStatus } from 'app/components/events/interfaces/types';
export function trimPackage(pkg) {
    var pieces = pkg.split(/^([a-z]:\\|\\\\)/i.test(pkg) ? '\\' : '/');
    var filename = pieces[pieces.length - 1] || pieces[pieces.length - 2] || pkg;
    return filename.replace(/\.(dylib|so|a|dll|exe)$/, '');
}
export function getPlatform(dataPlatform, platform) {
    // prioritize the frame platform but fall back to the platform
    // of the stack trace / exception
    return dataPlatform || platform;
}
export function getFrameHint(frame) {
    // returning [hintText, hintIcon]
    var symbolicatorStatus = frame.symbolicatorStatus;
    var func = frame.function || '<unknown>';
    // Custom color used to match adjacent text.
    var warningIcon = <IconQuestion size="xs" color={'#2c45a8'}/>;
    var errorIcon = <IconWarning size="xs" color="red300"/>;
    if (func.match(/^@objc\s/)) {
        return [t('Objective-C -> Swift shim frame'), warningIcon];
    }
    if (func.match(/^__?hidden#\d+/)) {
        return [t('Hidden function from bitcode build'), errorIcon];
    }
    if (!symbolicatorStatus && func === '<unknown>') {
        // Only render this if the event was not symbolicated.
        return [t('No function name was supplied by the client SDK.'), warningIcon];
    }
    if (func === '<unknown>' ||
        (func === '<redacted>' && symbolicatorStatus === SymbolicatorStatus.MISSING_SYMBOL)) {
        switch (symbolicatorStatus) {
            case SymbolicatorStatus.MISSING_SYMBOL:
                return [t('The symbol was not found within the debug file.'), warningIcon];
            case SymbolicatorStatus.UNKNOWN_IMAGE:
                return [t('No image is specified for the address of the frame.'), warningIcon];
            case SymbolicatorStatus.MISSING:
                return [
                    t('The debug file could not be retrieved from any of the sources.'),
                    errorIcon,
                ];
            case SymbolicatorStatus.MALFORMED:
                return [t('The retrieved debug file could not be processed.'), errorIcon];
            default:
        }
    }
    if (func === '<redacted>') {
        return [t('Unknown system frame. Usually from beta SDKs'), warningIcon];
    }
    return [null, null];
}
//# sourceMappingURL=utils.jsx.map