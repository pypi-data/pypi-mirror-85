/**
 * Copyright (c) AivanF 2020
 *
 * @summary PaiPage utility JS
 * @author AivanF <projects@aivanf.com>
 *
 * Created at 2020-05-18
 */
;const PaiPage = function($) {
	const version = 'PaiPage main.js 2020.05.18';
	console.log(version);

	function debugit(value, label) {
		label = label ? ` "${label}"` : '';
		console.log(`DebugIt${label} of type ${typeof value}:`, value);
	}

	function is_undefined(value) {
		return typeof value === 'undefined';
	}
	function is_nil(value) {
		return is_undefined(value) || (value === null);
	}
	function is_string(value) {
		return (typeof value === 'string' || value instanceof String);
	}
	function is_bool(value) {
		return !!value === value;
	}
	function is_int(value) {
		return Number.isInteger(value);
	}
	function is_float(value) {
		return Number.isFinite(value);
	}
	function is_dict(value) {
		return value.constructor == Object;
	}
	function is_function(value) {
		return typeof value === 'function';
	}

	function escapeHtml(unsafe) {
		return unsafe
			.replace(/&/g, "&amp;")
			.replace(/</g, "&lt;")
			.replace(/>/g, "&gt;")
			.replace(/"/g, "&quot;")
			.replace(/'/g, "&#039;");
	}


	function getUrlArguments() {
		let sURLVariables = window.location.search.substring(1).split('&'), sParameterName, i;
		let res = {};
		for (i = 0; i < sURLVariables.length; i++) {
			sParameterName = sURLVariables[i].split('=');
			res[sParameterName[0]] = sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
		}
		return res;
	}

	const Container = {
		version: version,

		// Basic functions
		debugit: debugit,
		is_undefined: is_undefined,
		is_nil: is_nil,
		is_string: is_string,
		is_bool: is_bool,
		is_int: is_int,
		is_float: is_float,
		is_dict: is_dict,
		is_function: is_function,
		escapeHtml: escapeHtml,

		getUrlArguments: getUrlArguments,
	};
	return Container;
}(jQuery);