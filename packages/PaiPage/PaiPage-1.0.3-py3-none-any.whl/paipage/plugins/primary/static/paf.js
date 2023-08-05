/**
 * Copyright (c) AivanF 2020
 *
 * @summary PaiPage Forms JS
 * @author AivanF <projects@aivanf.com>
 *
 * Created at 2020-05-22
 */
;const PAF = function($) {
const version = 'PAF.js 2020.05.29.2';
console.log(version);
/*
Reqired window variables:
	`selectables` for `select` element type.
*/

const Container = {};

Container.Forms = {};
Container.preprocessForm = function(form) {
	form.codes = {};
	let order = [];
	form.elements.forEach(function (element) {
		// Must have:
		if (!(
				element.type && element.code &&
				(element.name || (element.type == 'const'))
			)) {
			console.error('Got bad form element', element);
		}
		if (!form.codes[element.code]) {
			order.push(element.code);
		}
		// May have: desc, hideCreate, hideEdit, allow_clear, subtype, etc.
		form.codes[element.code] = element;
	});
	form.elements = order.map(function (code) {
		return form.codes[code];
	});;
	Container.Forms[form.type] = form;
	return form;
}
Container.toupdate = [];

const SELECT_NULL = '__no__';


function escapeHtml(unsafe) {
	return unsafe
		 .replace(/&/g, "&amp;")
		 .replace(/</g, "&lt;")
		 .replace(/>/g, "&gt;")
		 .replace(/"/g, "&quot;")
		 .replace(/'/g, "&#039;");
 }
function isFunction(value) {
	return typeof value === 'function';
}
function ifFunction(value, arg) {
	if (isFunction(value))
		return value(arg);
	else 
		return value;
}
function isDefined(value) {
	return typeof value !== 'undefined';
}
function ifUndefined(value, other) {
	if (isDefined(value)) {
		return value;
	} else {
		return other;
	}
}
function notNull(value) {
	return value !== null;
}
function exists(value) {
	return isDefined(value) && notNull(value);
}
function ifMany(value, callMany, callSingle) {
	if (Array.isArray(value)) {
		if (value.length === 1) {
			return ifFunction(callSingle, value[0]);
		} else {
			return ifFunction(callMany, value);
		}
	} else {
		return ifFunction(callSingle, value);
	}
}
function isMany(value) {
	return ifMany(value, true, false);
}
function forMany(value, callback) {
	let result = [];
	if (Array.isArray(value)) {
		let len = value.length;
		for (let i = 0; i < len; i++) {
			result.push(callback(value[i]));
		}
	} else {
		result.push(callback(value));
	}
	return result;
}

const get_value_def = (el => Array.isArray(el) ? el[0] : el);
const get_label_def = (el => Array.isArray(el) ? el[1] : el);

function findSelecting(ar, key) {
	let len = ar.length;
	for (let i = 0; i < len; i++) {
		if (key == get_value_def(ar[i]))
			return ar[i];
	}
	return null;
}



const ElementViewHandlers = {};
Container.ElementViewHandlers = ElementViewHandlers;
const SelectablesViewHandlers = {};
Container.SelectablesViewHandlers = SelectablesViewHandlers;

ElementViewHandlers['int'] = function (element, value) {
	return `${value}`;
};
ElementViewHandlers['str'] = function (element, value) {
	// can_copy = true;  // TODO: here!
	if (exists(value)) {
		return value;
	} else {
		return '[ undefined ]'
	}
};
ElementViewHandlers['str2str'] = function (element, value) {
	let result = '';
	Object.keys(value).forEach(function (key) {
		result += `<br><i>${key}:</i> ${value[key]}`;
	});
	return result;
};
ElementViewHandlers['bool'] = function (element, value) {
	const text_on = element.on || 'on';
	const text_off = element.off || 'off';
	return value == 1 ? text_on : text_off;
};
ElementViewHandlers['select'] = function (element, value) {
	if (!selectables[element.subtype]) {
		console.error(`Missing selectables for "${element.subtype}" subtype`);
		return;
	}
	let found = findSelecting(selectables[element.subtype], value);
	if (SelectablesViewHandlers[element.subtype]) {
		return SelectablesViewHandlers[element.subtype](found, value);
	} else {
		let empty_option = element.empty_option || '';
		if (found == null || found == '') {
			return empty_option;
		} else {
			return get_label_def(found);
		}
	}
};
ElementViewHandlers['const'] = function (element, value) {
	return null;
};

Container.buildFormView = function(form, obj) {
	let result = '';
	form.elements.forEach(function(element) {
		if (!ElementViewHandlers[element.type]) {
			console.error(`Missing ElementViewHandlers for "${element.type}" type`);
			return;
		}
		try {
			let value = ElementViewHandlers[element.type](element, obj[element.code]);
			if (exists(value))
				result += `<b>${element.name}:</b> ${value}<br>`;
		} catch (er) {
			console.error('PAF.buildFormView error on', element);
			console.error(er);
		}
	});
	return result;
}



Container.textCounter = function(ind, maxlen) {
	let o = $('#' + ind);
	let rem = maxlen - o.val().length;
	o.attr('title', 'Symbols: ' + rem).tooltip('fixTitle').tooltip('show');
}

function makeSelect(ind, options, settings) {
	// value, multiple, get_value, get_label, error_text, allow_clear, empty_option
	const get_value = settings['get_value'] || get_value_def;
	const get_label = settings['get_label'] || get_label_def;
	const empty_option = settings['empty_option'] || '-';
	let result = '<select class="form-control" id="' + ind + '"';
	if (settings['multiple']) { result += ' multiple="multiple"'; }
	result += '>';
	let s;
	if (settings['allow_clear']) {
		// create fake option
		if (!settings['multiple'] && !notNull(settings['value'])) {
			s = ' selected';
		} else {
			s = '';
		}
		result += `<option value="${SELECT_NULL}" ${s}>${empty_option}</option>`;
	}
	if (options) {
		for (i in options) {
			const cur = options[i];
			s = false;
			if (Array.isArray(settings['value'])) {
				s = settings['value'].includes(get_value(cur));
				if (!s) {
					if (typeof s === 'string') {
						s = settings['value'].includes(+get_value(cur));
					} else {
						s = settings['value'].includes(get_value(cur).toString());
					}
				}
			} else {
				s = get_value(cur) == settings['value'];
			}
			s = s ? ' selected' : '';
			result += '<option value="' + get_value(cur) + '" ' + s + '>' + get_label(cur) + '</option>';
		}
	}
	result += '</select>';
	Container.toupdate.push(function() {
		$('#' + ind).select2({ dropdownAutoWidth: true, width: '100%' });
	});
	if (!settings['allow_clear'] && (!options || options.length < 1)) {
		result += makeAlert(settings['error_text'] || 'Option list not found!');
	}
	return result;
}

function makeAlert(text, ind, style) {
	text = text || 'Unknown problem!';
	let result = '<div class="col-xs-12 alert alert-danger"';
	if (ind) {
		result += ' id="' + ind + '"';
	}
	result += ' style="margin-top: 10px; ';
	if (style) {
		result += style;
	}
	result += '">' + text + '</div>'
	return result;
}



const ElementEditHandlers = {};
Container.ElementEditHandlers = ElementEditHandlers;
const SelectablesOptionsHandlers = {};
Container.SelectablesOptionsHandlers = SelectablesOptionsHandlers;

ElementEditHandlers['str'] = function (ind, element, value) {
	let properties = '';
	let cur_val = '';
	if (typeof value === 'number' || typeof value === 'string') {
		cur_val = value.toString();
	}
	if (cur_val) {
		if (element.max_len) {
			cur_val = cur_val.slice(0, element.max_len);
		}
	}
	let cls = 'form-control edit-element-text';
	if (element.max_len) {
		properties += ' maxlength="' + element.max_len + '"';
		properties += ` onkeyup="PAF.textCounter('${ind}', ${element.max_len});"`;
		properties += ` onfocus="PAF.textCounter('${ind}', ${element.max_len});"`;
		properties += ' data-toggle="tooltip" title="Type a value"';
		cls += ' tooltipped';
	}

	let result = '';
	if (element.long) {
		result += `<textarea id="${ind}">${cur_val}</textarea>`;
	} else {
		if (cur_val) {
			properties += ' value="' + escapeHtml(cur_val) + '"';
		}
		result += `<input type="text" id="${ind}" ${properties} class="${cls}">`;
	}
	return result;
}
ElementEditHandlers['int'] = function (ind, element, value) {
	let cls = 'form-control edit-element-int';
	let properties = 'step="1"';
	if (exists(value))
		properties += ` value="${parseInt(value)}"`;
	else
		properties += ` value="0"`;
	if (isDefined(element.min))
		properties += ` min="${element.min}"`;
	if (isDefined(element.max))
		properties += ` max="${element.max}"`;
	let result = '';
	result += `<input type="number" id="${ind}" ${properties} class="${cls}">`;
	return result;
}
Container.updateSwitch = function (ind, text_on, text_off) {
	const obj = $(`#${ind}`);
	const label = $(`#${ind}-label`);
	if (obj.is(':checked')) {
		label.html(text_on);
	} else {
		label.html(text_off);
	}
}
ElementEditHandlers['bool'] = function (ind, element, value) {
	const text_on = element.on || 'on';
	const text_off = element.off || 'off';
	let cls = 'form-control edit-element-bool';
	let properties = '';
	let text;
	if (value == 1) {
		properties += ' checked';
		text = text_on;
	} else {
		text = text_off;
	}
	properties += ` onchange="PAF.updateSwitch('${ind}', '${text_on}', '${text_off}')"`;
	let result = '';
	result += '<div class="col-xs-2">'
	result += `<input type="checkbox" id="${ind}" ${properties} class="${cls}">`;
	result += '</div><div class="col-xs-8">'
	result += `<span id="${ind}-label">${text}</span></div>`;
	return result;
}
ElementEditHandlers['select'] = function (ind, element, value) {
	// value, multiple, get_value, get_label, error_text, allow_clear
	let options = selectables[element.subtype];
	if (SelectablesOptionsHandlers[element.subtype]) {
		options = SelectablesOptionsHandlers[element.subtype](element, options);
	}
	return makeSelect(ind, options, {
		value: value,
		multiple: false,
		allow_clear: element.allow_clear,
		empty_option: element.empty_option,
	}) + '<br>';
}
ElementEditHandlers['const'] = function (ind, element, value) {
	return null;
};

Container.buildFormEdit = function (form, obj, prefix, is_creation) {
	prefix = prefix || '';
	let result = '';
	form.elements.forEach(function(element) {
		let hide = false;
		if (is_creation)
			hide = ifUndefined(element.hideCreate, false);
		else
			hide = ifUndefined(element.hideEdit, false);
		if (hide) return;
		if (!ElementEditHandlers[element.type]) {
			console.error(`Missing ElementEditHandlers for "${element.type}" type`);
			return;
		}
		try {
			const ind = prefix + element.code;
			const old_value = obj ? obj[element.code] : undefined;
			const editor = ElementEditHandlers[element.type](ind, element, old_value);
			if (exists(editor)) {
				let desc = '';
				if (element.desc) {
					desc = `${element.desc}<br>`;
				}
				result += `
					<div class="form-element">
					<b>${element.name}</b><br>
					${desc}
					${editor}<br>
					${makeAlert('', ind + '-alert', 'display: none;')}
					</div>
				`;
			}
		} catch (er) {
			console.error('PAF.buildFormEdit error on', element);
			console.error(er);
		}
	});
	return result;
}

Container.updateEditor = function () {
	Container.toupdate.forEach(function(el){ el(); });
	Container.toupdate = [];
	$('[data-toggle="tooltip"]').tooltip();
}



const ElementExtractHandlers = {};
Container.ElementExtractHandlers = ElementExtractHandlers;
const SelectablesExtractHandlers = {};
Container.SelectablesExtractHandlers = SelectablesExtractHandlers;

ElementExtractHandlers['int'] = function (ind, element) {
	return parseInt($('#' + ind).val());
}
ElementExtractHandlers['str'] = function (ind, element) {
	return $('#' + ind).val();
}
ElementExtractHandlers['bool'] = function (ind, element) {
	return $('#' + ind).is(':checked');
}
ElementExtractHandlers['select'] = function (ind, element) {
	let value = $('#' + ind).val();
	if (value === SELECT_NULL)
		value = null;
	if (SelectablesExtractHandlers[element.subtype]) {
		return SelectablesExtractHandlers[element.subtype](element, value);
	} else {
		return value;
	}
}
ElementExtractHandlers['const'] = function (ind, element) {
	return ifFunction(element.value);
}

Container.extractForm = function(form, prefix, is_creation) {
	let result = {};
	prefix = prefix || '';
	form.elements.forEach(function(element) {
		let hide = false;
		if (is_creation)
			hide = ifUndefined(element.hideCreate, false);
		else
			hide = ifUndefined(element.hideEdit, false);
		if (hide) return;
		if (!ElementExtractHandlers[element.type]) {
			console.error(`Missing ElementExtractHandlers for "${element.type}" type`);
			return;
		}
		try {
			const ind = prefix + element.code;
			result[element.code] = ElementExtractHandlers[element.type](ind, element);
			if (!isDefined(result[element.code])) {
				throw Error(`Got undefined for "#${ind}"`);
			}
		} catch (er) {
			console.error('PAF.extractForm error on', element);
			console.error(er);
			return null;
		}
	});
	return result;
}



const ElementValidateHandlers = {};
Container.ElementValidateHandlers = ElementValidateHandlers;
const SelectablesValidateHandlers = {};
Container.SelectablesValidateHandlers = SelectablesValidateHandlers;

ElementValidateHandlers['str'] = function (element, value) {
	if (isDefined(element.min_len)) {
		if (value.length < element.min_len) {
			return `Text length is ${value.length}, but min is ${element.min_len}`;
		}
	}
	if (isDefined(element.max_len)) {
		if (value.length > element.max_len) {
			return `Text length is ${value.length}, but max is ${element.max_len}`;
		}
	}
}
ElementValidateHandlers['bool'] = function (element, value) {
	return null;
}
ElementValidateHandlers['select'] = function (element, value) {
	if (!exists(value) && !element.allow_clear)
		return 'Value not selected!';	
	if (SelectablesValidateHandlers[element.subtype]) {
		return SelectablesValidateHandlers[element.subtype](element, value);
	}
}
ElementValidateHandlers['const'] = function (element, value) {
	if (!exists(value) && !element.allow_clear)
		return 'Value not selected!';	
	if (SelectablesValidateHandlers[element.subtype]) {
		return SelectablesValidateHandlers[element.subtype](element, value);
	}
}

Container.validateForm = function(form, prefix, is_creation) {
	let values = Container.extractForm(form, prefix, is_creation);
	if (values == null) {
		return values;
	}
	let fine = true;
	prefix = prefix || '';
	form.elements.forEach(function(element) {
		let hide = false;
		if (is_creation)
			hide = ifUndefined(element.hideCreate, false);
		else
			hide = ifUndefined(element.hideEdit, false);
		if (hide) return;
		if (!ElementValidateHandlers[element.type]) {
			console.error(`Missing ElementValidateHandlers for "${element.type}" type`);
			return;
		}
		try {
			const ind = prefix + element.code;
			const value = values[element.code];
			const comment = ElementValidateHandlers[element.type](element, value);
			const $alert = $('#' + ind + '-alert');
			if (exists(comment)) {
				fine = false;
				$alert.html(comment);
				$alert.show(500);
			} else {
				$alert.hide(500);
			}
		} catch (er) {
			console.error('PAF.validateForm error on', element);
			console.error(er);
		}
	});
	if (fine) {
		return values;
	} else {
		return null;
	}
}

Container.addCustomType = function (type, obj) {
	if (exists(obj.view)) {
		// function (element, value)
		ElementViewHandlers[type] = obj.view;
	}
	if (exists(obj.edit)) {
		// function (ind, element, value)
		ElementEditHandlers[type] = obj.edit;
	}
	if (exists(obj.extract)) {
		// function (ind, element)
		ElementExtractHandlers[type] = obj.extract;
	}
	if (exists(obj.validate)) {
		// function (element, value)
		ElementValidateHandlers[type] = obj.validate;
	}
}
Container.addCustomSelectable = function (subtype, obj) {
	if (exists(obj.view)) {
		// function (found, value)
		SelectablesViewHandlers[subtype] = obj.view;
	}
	if (exists(obj.options)) {
		// function (element, options)
		SelectablesOptionsHandlers[subtype] = obj.options;
	}
	if (exists(obj.extract)) {
		// function (element, value)
		SelectablesExtractHandlers[subtype] = obj.extract;
	}
	if (exists(obj.validate)) {
		// function (element, value)
		SelectablesValidateHandlers[subtype] = obj.validate;
	}
}

// TODO: date types

return Container;
}(jQuery);