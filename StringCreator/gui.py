"""NiceGUI desktop front-end for StringCreator.

A thin GUI layer over the existing StringCreator core. Run with:

    python gui.py

By default it opens a native desktop window (requires pywebview). Set the
environment variable STRINGCREATOR_GUI_NATIVE=0 to open in a browser tab instead.
"""
import os

from nicegui import ui

import StringCreator as sc

BRAND_OPTIONS = {'random': 'Random brand', **{b: b.capitalize() for b in sc.CREDIT_CARD_BRANDS}}
ENCODING_OPTIONS = {'none': 'None (plain text)', 'base64': 'Base64', 'url': 'URL',
                    'hex': 'Hex', 'html': 'HTML entities'}
VALIDATE_KINDS = {'personnummer': 'Swedish personnummer', 'luhn': 'Luhn checksum',
                  'creditcard': 'Credit card', 'password': 'Password strength'}
STRENGTH_TYPES = {1, 2, 9}


def _generate_values(type_num, length, use_all, brand, batch, unique, encoding):
    """Produce a list of generated strings using the shared core functions."""
    if use_all:
        return [sc.generate_string(0, type_num, True)]

    results, seen = [], set()
    attempts = 0
    max_attempts = max(batch * 50, 100)
    while len(results) < batch:
        if type_num == 19:
            value = sc.generate_credit_card(None if brand == 'random' else brand)
        else:
            value = sc.generate_string(length, type_num, False)

        if encoding and encoding != 'none':
            value = sc.encode_string(value, encoding)

        if unique and value in seen:
            attempts += 1
            if attempts > max_attempts:
                ui.notify(f'Only produced {len(results)} unique value(s) of {batch} requested',
                          type='warning')
                break
            continue

        seen.add(value)
        results.append(value)
    return results


def build_ui():
    ui.label('StringCreator').classes('text-2xl font-bold')
    ui.label('Advanced string generator & security testing tool').classes('text-sm text-gray-500')

    with ui.tabs().classes('w-full') as tabs:
        generate_tab = ui.tab('Generate')
        validate_tab = ui.tab('Validate')
        history_tab = ui.tab('History')

    with ui.tab_panels(tabs, value=generate_tab).classes('w-full'):
        # ---- Generate ----
        with ui.tab_panel(generate_tab):
            type_select = ui.select(
                options={num: f'{num}. {label}' for num, label in sc.TYPE_LABELS.items()},
                value=1, label='Type').classes('w-full')

            with ui.row().classes('w-full items-center'):
                length_input = ui.number('Length (bytes)', value=16, min=1, precision=0).classes('w-40')
                batch_input = ui.number('Batch count', value=1, min=1, precision=0).classes('w-40')
                unique_switch = ui.switch('Unique')

            with ui.row().classes('w-full items-center'):
                all_switch = ui.switch('All payloads')
                brand_select = ui.select(options=BRAND_OPTIONS, value='random',
                                         label='Card brand').classes('w-48')
                encoding_select = ui.select(options=ENCODING_OPTIONS, value='none',
                                            label='Encoding').classes('w-48')

            output_area = ui.textarea(label='Output').props('readonly outlined').classes('w-full')
            info_label = ui.label('').classes('text-sm text-gray-600')

            def refresh_controls():
                t = type_select.value
                is_payload = t in sc.PAYLOAD_TYPES
                is_fixed = t in sc.NO_LENGTH_TYPES
                use_all = is_payload and all_switch.value
                all_switch.set_visibility(is_payload)
                brand_select.set_visibility(t == 19)
                length_input.set_visibility(not is_fixed and not use_all)
                batch_input.set_visibility(not use_all)
                unique_switch.set_visibility(not use_all and (batch_input.value or 1) > 1)
                encoding_select.set_visibility(not use_all)

            def do_generate():
                t = type_select.value
                use_all = t in sc.PAYLOAD_TYPES and all_switch.value
                length = int(length_input.value or 0)
                batch = max(int(batch_input.value or 1), 1)
                if not use_all and t not in sc.NO_LENGTH_TYPES and t not in sc.PAYLOAD_TYPES and length <= 0:
                    ui.notify('Length must be > 0 for this type', type='negative')
                    return

                results = _generate_values(t, length, use_all, brand_select.value,
                                           batch, unique_switch.value, encoding_select.value)
                if not results:
                    return
                final = '\n'.join(results) if len(results) != 1 else results[0]
                output_area.value = final

                parts = [f'{len(final.encode("utf-8"))} bytes']
                if len(results) > 1:
                    parts.append(f'{len(results)} values')
                if t in STRENGTH_TYPES and len(results) == 1:
                    strength, score, _ = sc.check_password_strength(final)
                    parts.append(f'Strength: {strength} ({score}/6)')
                info_label.text = '  |  '.join(parts)

                sc.save_to_history(final, t, length)

            def do_copy():
                if not output_area.value:
                    ui.notify('Nothing to copy', type='warning')
                    return
                if sc.copy_to_clipboard(output_area.value):
                    ui.notify('Copied to clipboard', type='positive')
                else:
                    ui.notify('Clipboard unavailable', type='negative')

            type_select.on_value_change(refresh_controls)
            all_switch.on_value_change(refresh_controls)
            batch_input.on_value_change(refresh_controls)

            with ui.row():
                ui.button('Generate', on_click=do_generate).props('color=primary')
                ui.button('Copy', on_click=do_copy).props('outline')

            # ---- Export ----
            with ui.expansion('Export to file').classes('w-full'):
                filename_input = ui.input('Filename', value='output.txt').classes('w-64')
                format_select = ui.select({'text': 'Text', 'json': 'JSON', 'csv': 'CSV'},
                                          value='text', label='Format').classes('w-40')

                def do_save():
                    if not output_area.value:
                        ui.notify('Generate something first', type='warning')
                        return
                    results = output_area.value.split('\n')
                    try:
                        sc.save_output(filename_input.value, results, format_select.value,
                                       type_select.value, int(length_input.value or 0))
                        ui.notify(f'Saved to {filename_input.value}', type='positive')
                    except OSError as e:
                        ui.notify(f'Error saving: {e}', type='negative')

                ui.button('Save', on_click=do_save).props('outline')

            refresh_controls()

        # ---- Validate ----
        with ui.tab_panel(validate_tab):
            kind_select = ui.select(options=VALIDATE_KINDS, value='personnummer',
                                    label='Validate').classes('w-64')
            value_input = ui.input('Value').classes('w-full')
            result_label = ui.label('').classes('text-lg font-semibold')

            def do_validate():
                kind, value = kind_select.value, value_input.value or ''
                if kind == 'personnummer':
                    ok = sc.validate_personnummer(value)
                    result_label.text = f'{"✓ VALID" if ok else "✗ INVALID"} personnummer'
                    result_label.classes(replace='text-lg font-semibold '
                                         + ('text-green-600' if ok else 'text-red-600'))
                elif kind in ('luhn', 'creditcard'):
                    digits = ''.join(c for c in value if c.isdigit())
                    ok = bool(digits) and sc.luhn_is_valid(digits)
                    label = 'credit card' if kind == 'creditcard' else 'Luhn checksum'
                    result_label.text = f'{"✓ VALID" if ok else "✗ INVALID"} {label}'
                    result_label.classes(replace='text-lg font-semibold '
                                         + ('text-green-600' if ok else 'text-red-600'))
                else:  # password
                    strength, score, feedback = sc.check_password_strength(value)
                    msg = f'Strength: {strength} ({score}/6)'
                    if feedback:
                        msg += ' — ' + ', '.join(feedback)
                    result_label.text = msg
                    result_label.classes(replace='text-lg font-semibold text-gray-700')

            ui.button('Validate', on_click=do_validate).props('color=primary')

        # ---- History ----
        with ui.tab_panel(history_tab):
            history_columns = [
                {'name': 'timestamp', 'label': 'Timestamp', 'field': 'timestamp', 'align': 'left'},
                {'name': 'type', 'label': 'Type', 'field': 'type'},
                {'name': 'length', 'label': 'Length', 'field': 'length'},
                {'name': 'byte_size', 'label': 'Bytes', 'field': 'byte_size'},
                {'name': 'string', 'label': 'Value', 'field': 'string', 'align': 'left'},
            ]
            history_table = ui.table(columns=history_columns, rows=[], row_key='timestamp').classes('w-full')

            def refresh_history():
                history_table.rows = list(reversed(sc.load_history()))

            ui.button('Refresh history', on_click=refresh_history).props('outline')
            refresh_history()


build_ui()

if __name__ in {'__main__', '__mp_main__'}:
    native = os.environ.get('STRINGCREATOR_GUI_NATIVE', '1') != '0'
    ui.run(title='StringCreator', native=native, reload=False)
