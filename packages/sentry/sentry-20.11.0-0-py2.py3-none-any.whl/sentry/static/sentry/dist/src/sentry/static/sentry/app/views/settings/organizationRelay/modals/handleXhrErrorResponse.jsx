import { t } from 'app/locale';
function handleError(error) {
    var _a;
    var errorMessage = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.trustedRelays[0];
    if (!errorMessage) {
        return {
            type: 'unknown',
            message: t('An unknown error occurred while saving Relay public key.'),
        };
    }
    if (errorMessage === 'Bad structure received for Trusted Relays') {
        return {
            type: 'bad-structure',
            message: t('An invalid structure was sent.'),
        };
    }
    if (errorMessage === 'Relay key info with missing name in Trusted Relays') {
        return {
            type: 'missing-name',
            message: t('Field Required'),
        };
    }
    if (errorMessage === 'Relay key info with empty name in Trusted Relays') {
        return {
            type: 'empty-name',
            message: t('Invalid Field'),
        };
    }
    if (errorMessage.startsWith('Missing public key for Relay key info with name:')) {
        return {
            type: 'missing-key',
            message: t('Field Required'),
        };
    }
    if (errorMessage.startsWith('Invalid public key for relay key info with name:')) {
        return {
            type: 'invalid-key',
            message: t('Invalid Relay key'),
        };
    }
    if (errorMessage.startsWith('Duplicated key in Trusted Relays:')) {
        return {
            type: 'duplicated-key',
            message: t('Relay key already taken'),
        };
    }
    return {
        type: 'unknown',
        message: t('An unknown error occurred while saving Relay public key.'),
    };
}
export default handleError;
//# sourceMappingURL=handleXhrErrorResponse.jsx.map