document.addEventListener('DOMContentLoaded', function() {
var converseCfg = {
        view_mode: "embedded",
	anonymous: true,
	jid: "glaceon.live",
	auto_login: true,
	allow_logout: false,
	auto_reconnect: true,
	play_sounds: false,
	keepalive: true,
	show_controlbox_by_default: true,
	hide_muc_server: true,
	allow_muc_invitations: false,
	allow_contact_requests: false,
	muc_show_join_leave: false,
	use_system_emojis: false,
	synchronize_availability: false,
	authentication: "anonymous",
	auto_join_rooms: [ {jid:streamer+"@muc.glaceon.live"}],
	blacklisted_plugins: [
		"converse-notification",
		"converse-fullscreen",
	]
};
if (window.location.hash !== "#bosh") {
	converseCfg.websocket_url = "wss://glaceon.live/xmpp/websocket";
}
converseCfg.bosh_service_url = "https://glaceon.live/xmpp/bosh";
converse.initialize(converseCfg);
});
