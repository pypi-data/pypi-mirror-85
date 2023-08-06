/**
 * Convert list of individual relay objects into a per-file summary grouped by publicKey
 */
export function getRelaysByPublicKey(relays, relayActivities) {
    return relays.reduce(function (relaysByPublicKey, relay) {
        var name = relay.name, description = relay.description, created = relay.created, publicKey = relay.publicKey;
        if (!relaysByPublicKey.hasOwnProperty(publicKey)) {
            relaysByPublicKey[publicKey] = { name: name, description: description, created: created, activities: [] };
        }
        if (!relaysByPublicKey[publicKey].activities.length) {
            relaysByPublicKey[publicKey].activities = relayActivities.filter(function (activity) { return activity.publicKey === publicKey; });
        }
        return relaysByPublicKey;
    }, {});
}
/**
 * Returns a short publicKey with only 20 characters
 */
export function getShortPublicKey(publicKey) {
    return publicKey.substring(0, 20);
}
//# sourceMappingURL=utils.jsx.map